from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import torch
import xarray as xr

from .utils import map_year_to_tnorm


@dataclass
class GlacierDataset:
    ds: xr.Dataset
    start_year: int
    train_end_year: int
    end_year: int
    normalize_targets: bool = True

    def __post_init__(self) -> None:
        assert "H_obs" in self.ds, "Dataset must contain H_obs(time,y,x)"
        assert "bed" in self.ds, "Dataset must contain bed(y,x)"
        assert "accum" in self.ds, "Dataset must contain accum(time,y,x)"
        # extract arrays
        self.x = self.ds["x"].values
        self.y = self.ds["y"].values
        self.time_years = self.ds["time"].values.astype(float)
        # tensors for bed and accum
        bed = torch.from_numpy(self.ds["bed"].values).float()  # [Ny, Nx]
        Ny, Nx = bed.shape
        self.bed = bed.view(1, 1, Ny, Nx).contiguous()

        accum = torch.from_numpy(self.ds["accum"].values).float()  # [Nt, Ny, Nx]
        Nt = accum.shape[0]
        self.accum = accum.view(Nt, 1, Ny, Nx).contiguous()

        # observed H for 1980–2020 only
        mask_train = (self.time_years >= self.start_year) & (self.time_years <= self.train_end_year)
        H = torch.from_numpy(self.ds["H_obs"].values[mask_train]).float()  # [Nt_train, Ny, Nx]
        self.H_obs = H  # not normalized by default; normalization handled externally

        # means for normalization
        if self.normalize_targets:
            self.H_mean = torch.mean(self.H_obs)
            self.H_std = torch.std(self.H_obs) + 1e-6
        else:
            self.H_mean = torch.tensor(0.0)
            self.H_std = torch.tensor(1.0)

        # precompute normalized time for each training time index
        self.tnorm_train = (
            (self.time_years[mask_train] - self.start_year)
            / (self.end_year - self.start_year)
        ).astype(np.float32)

    @property
    def grid_shape(self) -> Tuple[int, int]:
        return int(self.bed.shape[-2]), int(self.bed.shape[-1])

    @property
    def num_train_times(self) -> int:
        return len(self.tnorm_train)


class CollocationSampler:
    def __init__(self, dataset: GlacierDataset, device: torch.device) -> None:
        self.dataset = dataset
        self.device = device
        Ny, Nx = dataset.grid_shape
        self.Ny = Ny
        self.Nx = Nx

    def sample_collocation(self, n: int) -> torch.Tensor:
        xy = torch.rand(n, 2, device=self.device)
        t = torch.rand(n, 1, device=self.device)
        return torch.cat([xy, t], dim=1)

    def sample_initial(self, n: int) -> Tuple[torch.Tensor, torch.Tensor]:
        # t=0 corresponds to start_year
        xy = torch.rand(n, 2, device=self.device)
        t0 = torch.zeros(n, 1, device=self.device)
        xyt = torch.cat([xy, t0], dim=1)
        # sample H0 from first train time slice
        H0 = self.dataset.H_obs[0]  # [Ny, Nx]
        H0 = H0.view(1, 1, self.Ny, self.Nx)
        # sample targets with grid_sample
        grid = (xy * 2 - 1).view(1, -1, 1, 2)
        H_samples = torch.nn.functional.grid_sample(H0, grid, align_corners=True).view(-1)
        return xyt, H_samples

    def sample_data_points(self, n: int) -> Tuple[torch.Tensor, torch.Tensor]:
        # sample random times from train set and random xy
        idx_t = torch.randint(0, self.dataset.num_train_times, (n,), device=self.device)
        tnorm = torch.from_numpy(self.dataset.tnorm_train).to(self.device)[idx_t].view(-1, 1)
        xy = torch.rand(n, 2, device=self.device)
        xyt = torch.cat([xy, tnorm], dim=1)

        # gather H_obs slice
        H_slice = self.dataset.H_obs[idx_t].view(n, 1, self.Ny, self.Nx)
        grid = (xy * 2 - 1).view(n, 1, 1, 2)
        # per-sample grid_sample
        H_samples = torch.nn.functional.grid_sample(H_slice, grid, align_corners=True)
        H_samples = H_samples.view(-1)
        return xyt, H_samples

    def sample_boundary(self, n: int) -> torch.Tensor:
        # edges
        n_per_edge = max(1, n // 4)
        t = torch.rand(n_per_edge, 1, device=self.device)
        left = torch.cat([torch.zeros_like(t), t], dim=1)
        right = torch.cat([torch.ones_like(t), t], dim=1)
        bottom = torch.cat([t, torch.zeros_like(t)], dim=1)
        top = torch.cat([t, torch.ones_like(t)], dim=1)
        xy = torch.cat([left, right, bottom, top], dim=0)
        # random t in [0,1]
        tt = torch.rand(xy.shape[0], 1, device=self.device)
        pts = torch.cat([xy, tt], dim=1)
        idx = torch.randperm(pts.shape[0], device=self.device)[:n]
        return pts[idx]
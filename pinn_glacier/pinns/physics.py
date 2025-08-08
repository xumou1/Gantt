from dataclasses import dataclass
from typing import Literal, Tuple

import torch
import torch.nn.functional as F

from .models import gradients


@dataclass
class SIAParams:
    rho: float = 917.0
    g: float = 9.81
    n: float = 3.0
    A: float = 1.0e-24


class ShallowIceResidual:
    """
    Implements the SIA PDE residual for glacier thickness H(x,y,t):

        dH/dt + div(q) = a

    where q = -Gamma * H^{n+2} * |grad(s)|^{n-1} * grad(s), s = b + H
    and Gamma = 2 A (rho g)^n / (n + 2).

    We operate in a normalized domain (x,y,t) in [0,1]^3. Bed b(x,y) and
    accumulation a(x,y,t) are sampled from gridded tensors using grid_sample.
    """

    def __init__(
        self,
        sia_params: SIAParams,
        bed: torch.Tensor,  # [1, 1, Ny, Nx]
        accum: torch.Tensor,  # [Nt, 1, Ny, Nx] for t in [1980,2100]
        bc_type: Literal["zero_flux"] = "zero_flux",
        device: str = "cpu",
    ) -> None:
        self.params = sia_params
        self.device = device
        self.bc_type = bc_type
        self.Gamma = 2.0 * sia_params.A * (sia_params.rho * sia_params.g) ** sia_params.n / (
            sia_params.n + 2.0
        )
        self.bed = bed.to(device)
        self.accum = accum.to(device)
        self.Nt = accum.shape[0]

    @staticmethod
    def _to_grid(coords: torch.Tensor) -> torch.Tensor:
        """Map [0,1] coords to grid_sample coords [-1,1]."""
        return coords * 2.0 - 1.0

    def sample_bed(self, xy: torch.Tensor) -> torch.Tensor:
        # xy: [N,2] in [0,1]
        grid = self._to_grid(xy).view(1, -1, 1, 2)
        # grid_sample expects [N, C, H, W] input and grid [N, H_out, W_out, 2]
        with torch.no_grad():
            bed = F.grid_sample(self.bed, grid, align_corners=True)
        return bed.view(-1).detach()

    def sample_accum(self, xyt: torch.Tensor) -> torch.Tensor:
        # xyt: [N,3] with t in [0,1] mapping to Nt indices
        N = xyt.shape[0]
        xy = xyt[:, :2]
        t = xyt[:, 2:3]
        t_idx = torch.clamp(t * (self.Nt - 1), 0, self.Nt - 1)
        # linear interpolate between floor and ceil timesteps
        t0 = torch.floor(t_idx).long().squeeze(-1)
        t1 = torch.clamp(t0 + 1, 0, self.Nt - 1)
        w1 = (t_idx - t0.unsqueeze(-1).float()).view(-1)
        w0 = 1.0 - w1
        xy_grid = self._to_grid(xy).view(N, 1, 1, 2)
        with torch.no_grad():
            a0 = F.grid_sample(self.accum[t0], xy_grid, align_corners=True).view(-1)
            a1 = F.grid_sample(self.accum[t1], xy_grid, align_corners=True).view(-1)
            a = w0 * a0 + w1 * a1
        return a.detach()

    def compute_residual(self, model, xyt: torch.Tensor) -> torch.Tensor:
        xyt = xyt.requires_grad_(True)
        H = model(xyt).view(-1)  # [N]
        xy = xyt[:, :2]
        t = xyt[:, 2:3]
        b = self.sample_bed(xy)
        s = b + H

        # grads
        ds_dxy = gradients(s, xyt)[:, :2]  # [N,2]
        dH_dt = gradients(H, xyt)[:, 2:3].view(-1)
        grad_s_norm = torch.norm(ds_dxy, dim=1) + 1e-8

        n = self.params.n
        Gamma = self.Gamma
        H_pos = torch.clamp(H, min=0.0)  # avoid negative thickness

        # flux q = -Gamma * H^{n+2} * |grad s|^{n-1} * grad s
        scale = -Gamma * (H_pos ** (n + 2)) * (grad_s_norm ** (n - 1))
        q = scale.unsqueeze(1) * ds_dxy  # [N,2]

        # divergence: dqxdx + dqydy
        qx = q[:, 0]
        qy = q[:, 1]
        dqxdx = gradients(qx, xyt)[:, 0]
        dqydy = gradients(qy, xyt)[:, 1]
        div_q = dqxdx + dqydy

        a = self.sample_accum(xyt)
        residual = dH_dt + div_q - a
        return residual

    def boundary_loss(self, model, boundary_points: torch.Tensor) -> torch.Tensor:
        if self.bc_type != "zero_flux":
            return torch.tensor(0.0, device=self.device)
        boundary_points = boundary_points.requires_grad_(True)
        H = model(boundary_points).view(-1)
        xy = boundary_points[:, :2]
        b = self.sample_bed(xy)
        s = b + H
        ds_dxy = gradients(s, boundary_points)[:, :2]

        n = self.params.n
        Gamma = self.Gamma
        H_pos = torch.clamp(H, min=0.0)
        grad_s_norm = torch.norm(ds_dxy, dim=1) + 1e-8
        scale = -Gamma * (H_pos ** (n + 2)) * (grad_s_norm ** (n - 1))
        q = scale.unsqueeze(1) * ds_dxy  # [N,2]

        # normals for unit square boundaries
        normals = torch.zeros_like(q)
        x = boundary_points[:, 0]
        y = boundary_points[:, 1]
        eps = 1e-6
        left = (x < eps).float().unsqueeze(1)
        right = (x > 1 - eps).float().unsqueeze(1)
        bottom = (y < eps).float().unsqueeze(1)
        top = (y > 1 - eps).float().unsqueeze(1)
        normals += left * torch.tensor([-1.0, 0.0], device=self.device)
        normals += right * torch.tensor([1.0, 0.0], device=self.device)
        normals += bottom * torch.tensor([0.0, -1.0], device=self.device)
        normals += top * torch.tensor([0.0, 1.0], device=self.device)
        qn = torch.sum(q * normals, dim=1)
        return torch.mean(qn ** 2)
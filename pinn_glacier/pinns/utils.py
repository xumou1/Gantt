import os
import random
from typing import Tuple

import numpy as np
import torch


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_device(cfg_device: str = "auto") -> torch.device:
    if cfg_device == "cpu":
        return torch.device("cpu")
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def map_year_to_tnorm(year: float, y0: float, y1: float) -> float:
    return (year - y0) / (y1 - y0)


def map_tnorm_to_year(t: float, y0: float, y1: float) -> float:
    return y0 + t * (y1 - y0)


def normalize_tensor(x: torch.Tensor, mean: torch.Tensor, std: torch.Tensor) -> torch.Tensor:
    return (x - mean) / (std + 1e-8)


def denormalize_tensor(x: torch.Tensor, mean: torch.Tensor, std: torch.Tensor) -> torch.Tensor:
    return x * (std + 1e-8) + mean


def sample_unit_square(n: int, device: torch.device) -> torch.Tensor:
    return torch.rand(n, 2, device=device)


def sample_unit_time(n: int, device: torch.device) -> torch.Tensor:
    return torch.rand(n, 1, device=device)


def sample_boundary(n: int, device: torch.device) -> torch.Tensor:
    # Randomly sample edges on unit square
    n_per_edge = max(1, n // 4)
    t = torch.rand(n_per_edge, 1, device=device)
    left = torch.cat([torch.zeros_like(t), t], dim=1)
    right = torch.cat([torch.ones_like(t), t], dim=1)
    bottom = torch.cat([t, torch.zeros_like(t)], dim=1)
    top = torch.cat([t, torch.ones_like(t)], dim=1)
    pts = torch.cat([left, right, bottom, top], dim=0)
    idx = torch.randperm(pts.shape[0], device=device)[:n]
    return pts[idx]
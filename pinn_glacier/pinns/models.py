import math
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


class Sine(nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sin(x)


def build_activation(name: str) -> nn.Module:
    name = (name or "tanh").lower()
    if name == "sine":
        return Sine()
    if name == "gelu":
        return nn.GELU()
    return nn.Tanh()


class FourierFeatures(nn.Module):
    def __init__(self, in_dim: int, num_features: int, sigma: float = 10.0):
        super().__init__()
        B = torch.randn(in_dim, num_features) * sigma
        self.register_buffer("B", B)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [N, in_dim], return [N, 2*num_features]
        proj = 2.0 * math.pi * x @ self.B  # [N, num_features]
        return torch.cat([torch.sin(proj), torch.cos(proj)], dim=-1)


class FourierFeatureMLP(nn.Module):
    def __init__(
        self,
        input_dim: int = 3,
        hidden_dim: int = 256,
        num_hidden_layers: int = 6,
        activation: str = "sine",
        use_fourier_features: bool = True,
        fourier_features: int = 64,
        fourier_sigma: float = 10.0,
        output_dim: int = 1,
    ) -> None:
        super().__init__()
        self.use_fourier_features = use_fourier_features
        self.activation = build_activation(activation)

        if use_fourier_features:
            self.ff = FourierFeatures(input_dim, fourier_features, sigma=fourier_sigma)
            first_in = 2 * fourier_features
        else:
            self.ff = nn.Identity()
            first_in = input_dim

        layers = []
        last_dim = first_in
        for _ in range(num_hidden_layers):
            layers.append(nn.Linear(last_dim, hidden_dim))
            layers.append(self.activation)
            last_dim = hidden_dim
        layers.append(nn.Linear(last_dim, output_dim))
        self.net = nn.Sequential(*layers)

        # Xavier init for linear layers
        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, xyt: torch.Tensor) -> torch.Tensor:
        features = self.ff(xyt)
        out = self.net(features)
        return out


def gradients(y: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    """Compute dy/dx for batched y scalar and x vector with create_graph True."""
    grad = torch.autograd.grad(
        y, x, grad_outputs=torch.ones_like(y), create_graph=True, retain_graph=True
    )[0]
    return grad


def jacobian(y: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    """Compute Jacobian J_{ij} = dy_i/dx_j for vector y and vector x."""
    assert y.ndim == 2 and x.ndim == 2
    jac_rows = []
    for i in range(y.shape[1]):
        grad_i = torch.autograd.grad(
            y[:, i], x, grad_outputs=torch.ones_like(y[:, i]), create_graph=True, retain_graph=True
        )[0]
        jac_rows.append(grad_i.unsqueeze(1))
    return torch.cat(jac_rows, dim=1)
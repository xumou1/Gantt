import argparse
import os
from typing import Dict

import torch
import torch.nn as nn
import torch.optim as optim
import xarray as xr
import yaml
from tqdm import tqdm

from pinns import (
    FourierFeatureMLP,
    ShallowIceResidual,
    GlacierDataset,
    CollocationSampler,
)
from pinns.physics import SIAParams
from pinns.utils import set_seed, get_device


def load_config(path: str) -> Dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="/workspace/pinn_glacier/config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    set_seed(cfg["train"]["seed"]) 
    device = get_device(cfg["train"]["device"]).type

    # Data
    ds = xr.open_dataset(cfg["data"]["dataset_path"])
    dataset = GlacierDataset(
        ds=ds,
        start_year=cfg["data"]["start_year"],
        train_end_year=cfg["data"]["train_end_year"],
        end_year=cfg["data"]["end_year"],
        normalize_targets=cfg["data"]["normalize_targets"],
    )

    # Model
    model_cfg = cfg["model"]
    model = FourierFeatureMLP(
        input_dim=model_cfg["input_dim"],
        hidden_dim=model_cfg["hidden_dim"],
        num_hidden_layers=model_cfg["num_hidden_layers"],
        activation=model_cfg["activation"],
        use_fourier_features=model_cfg["use_fourier_features"],
        fourier_features=model_cfg["fourier_features"],
        fourier_sigma=model_cfg["fourier_sigma"],
    ).to(device)

    # Physics residual
    sia_params = SIAParams(
        rho=cfg["physics"]["rho"],
        g=cfg["physics"]["g"],
        n=cfg["physics"]["n"],
        A=cfg["physics"]["A"],
    )
    physics = ShallowIceResidual(
        sia_params=sia_params,
        bed=dataset.bed.to(device),
        accum=dataset.accum.to(device),
        bc_type=cfg["physics"]["bc"],
        device=device,
    )

    # Sampler
    sampler = CollocationSampler(dataset, device=device)

    # Optimizer
    optimizer = optim.Adam(model.parameters(), lr=cfg["train"]["lr"], weight_decay=cfg["train"]["weight_decay"])
    scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=cfg["train"]["scheduler_gamma"])

    mse = nn.MSELoss()

    output_dir = cfg["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    steps_per_epoch = cfg["train"]["steps_per_epoch"]
    for epoch in range(cfg["train"]["epochs"]):
        pbar = tqdm(range(steps_per_epoch), disable=False)
        for _ in pbar:
            # sample batches
            xyt_pde = sampler.sample_collocation(cfg["train"]["batch"]["num_collocation"])  # [N,3]
            xyt_data, H_data = sampler.sample_data_points(cfg["train"]["batch"]["num_data"])  # [N,3], [N]
            xyt_ic, H_ic = sampler.sample_initial(cfg["train"]["batch"]["num_initial"])  # [N,3], [N]
            xyt_bc = sampler.sample_boundary(cfg["train"]["batch"]["num_boundary"])  # [N,3]

            # losses
            residual = physics.compute_residual(model, xyt_pde)
            loss_pde = torch.mean(residual ** 2)

            pred_data = model(xyt_data).view(-1)
            loss_data = mse(pred_data, H_data)

            pred_ic = model(xyt_ic).view(-1)
            loss_ic = mse(pred_ic, H_ic)

            loss_bc = physics.boundary_loss(model, xyt_bc)

            lw = cfg["train"]["loss_weights"]
            loss = (
                lw["pde"] * loss_pde
                + lw["data"] * loss_data
                + lw["ic"] * loss_ic
                + lw["bc"] * loss_bc
            )

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            pbar.set_description(
                f"E{epoch} L={loss.item():.3e} pde={loss_pde.item():.2e} data={loss_data.item():.2e} ic={loss_ic.item():.2e} bc={loss_bc.item():.2e}"
            )
        scheduler.step()

        if (epoch + 1) % 1000 == 0 or epoch == cfg["train"]["epochs"] - 1:
            ckpt_path = cfg["checkpoint_path"]
            os.makedirs(os.path.dirname(ckpt_path), exist_ok=True)
            torch.save({"model": model.state_dict(), "epoch": epoch}, ckpt_path)


if __name__ == "__main__":
    main()
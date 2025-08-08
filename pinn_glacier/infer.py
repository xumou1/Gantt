import argparse
import os
from typing import Dict

import numpy as np
import torch
import xarray as xr
import yaml

from pinns import FourierFeatureMLP, GlacierDataset
from pinns.utils import get_device, map_year_to_tnorm


def load_config(path: str) -> Dict:
    import yaml
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="/workspace/pinn_glacier/config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
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
    Ny, Nx = dataset.grid_shape

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
    ckpt = torch.load(cfg["checkpoint_path"], map_location=device)
    model.load_state_dict(ckpt["model"])  
    model.eval()

    # Inference times
    years = cfg["infer"]["years"]
    if cfg["infer"].get("write_full_timeseries", False):
        years = list(range(cfg["data"]["train_end_year"], cfg["data"]["end_year"] + 1))

    xs = np.linspace(0, 1, Nx, dtype=np.float32)
    ys = np.linspace(0, 1, Ny, dtype=np.float32)
    X, Y = np.meshgrid(xs, ys)
    X = torch.from_numpy(X).to(device)
    Y = torch.from_numpy(Y).to(device)

    H_pred_list = []
    for y in years:
        tnorm = map_year_to_tnorm(y, cfg["data"]["start_year"], cfg["data"]["end_year"])
        T = torch.full_like(X, float(tnorm))
        xyt = torch.stack([X, Y, T], dim=-1).view(-1, 3)
        with torch.no_grad():
            H = model(xyt).view(Ny, Nx)
        H_pred_list.append(H.cpu().numpy())

    H_pred = np.stack(H_pred_list, axis=0)  # [Nt, Ny, Nx]

    out_dir = cfg["infer"]["output_dir"]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "qtp_glacier_future.nc")

    ds_out = xr.Dataset(
        {
            "H_pred": (("time", "y", "x"), H_pred),
        },
        coords={
            "time": np.array(years, dtype=np.int32),
            "y": dataset.y,
            "x": dataset.x,
        },
        attrs={"description": "PINNs predicted glacier thickness"},
    )
    ds_out.to_netcdf(out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
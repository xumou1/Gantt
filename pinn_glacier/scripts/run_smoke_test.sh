#!/usr/bin/env bash
set -euo pipefail

ROOT=/workspace/pinn_glacier
mkdir -p $ROOT/data $ROOT/outputs/smoke_test

# Install deps locally for this user; fallback to break-system-packages when needed
python3 -m pip install -q --user -r $ROOT/requirements.txt || python3 -m pip install -q --break-system-packages -r $ROOT/requirements.txt

python3 - << 'PY'
import os
import numpy as np
import xarray as xr

root = "/workspace/pinn_glacier"
path = os.path.join(root, "data", "qtp_glacier.nc")
Ny, Nx = 32, 32
years = np.arange(1980, 2101)
Nt = len(years)
x = np.linspace(0, 100e3, Nx)
y = np.linspace(0, 100e3, Ny)
X, Y = np.meshgrid(x, y)

# synthetic bed (bowl)
bed = 3000 - 0.00002 * ((X-50e3)**2 + (Y-50e3)**2)**0.5

# synthetic accumulation (sinusoidal pattern over time, spatial gradient)
accum = np.zeros((Nt, Ny, Nx), dtype=np.float32)
for i in range(Nt):
    t = i / (Nt - 1)
    accum[i] = 0.5 + 0.2*np.sin(2*np.pi*t) + 0.000001*(X - 50e3)

# synthetic H: thicker in center, slight temporal decline after 2000
H = np.zeros((Nt, Ny, Nx), dtype=np.float32)
R = ((X-50e3)**2 + (Y-50e3)**2)**0.5
H0 = np.clip(500 - 0.004*R, 0, None)
for i in range(Nt):
    year = years[i]
    trend = 1.0 - 0.002*max(0, year-2000)
    H[i] = np.clip(H0 * trend, 0, None)

# observed only until 2020 -> store full time with NaN after 2020
H_obs = H.copy()
H_obs[years > 2020] = np.nan

ds = xr.Dataset(
    {
        "H_obs": (("time", "y", "x"), H_obs.astype(np.float32)),
        "bed": (("y", "x"), bed.astype(np.float32)),
        "accum": (("time", "y", "x"), accum.astype(np.float32)),
    },
    coords={
        "time": years.astype(np.int32),
        "y": y.astype(np.float32),
        "x": x.astype(np.float32),
    },
)

os.makedirs(os.path.dirname(path), exist_ok=True)
ds.to_netcdf(path)
print("Wrote", path)
PY

# shorten training for smoke test
python3 - << 'PY'
import yaml
p = "/workspace/pinn_glacier/config.yaml"
cfg = yaml.safe_load(open(p))
cfg["output_dir"] = "/workspace/pinn_glacier/outputs/smoke_test"
cfg["checkpoint_path"] = "/workspace/pinn_glacier/outputs/smoke_test/model.pt"
cfg["train"]["epochs"] = 5
cfg["train"]["steps_per_epoch"] = 1
cfg["train"]["batch"]["num_collocation"] = 1024
cfg["train"]["batch"]["num_data"] = 512
cfg["train"]["batch"]["num_boundary"] = 256
cfg["train"]["batch"]["num_initial"] = 512
with open(p, "w") as f:
    yaml.safe_dump(cfg, f)
print("Wrote updated config for smoke test")
PY

python3 /workspace/pinn_glacier/train.py --config /workspace/pinn_glacier/config.yaml
python3 /workspace/pinn_glacier/infer.py --config /workspace/pinn_glacier/config.yaml

echo "Smoke test complete. Outputs in $ROOT/outputs/smoke_test"
# PINNs Glacier Evolution (QTP)

This project implements a Physics-Informed Neural Network (PINNs) to simulate glacier thickness evolution on the Qinghai–Tibetan Plateau (QTP) using the shallow-ice approximation (SIA) and observed data from 1980–2020, then predict 2020–2100.

## Quickstart (Synthetic Smoke Test)

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Generate synthetic data and run a short training + inference:

```
bash scripts/run_smoke_test.sh
```

Outputs are written to `outputs/smoke_test/`.

## Real Data Training

- Place a NetCDF at `data/qtp_glacier.nc` with variables:
  - `H_obs(time, y, x)` glacier thickness (meters) from 1980–2020
  - `bed(y, x)` bedrock elevation (meters)
  - `accum(time, y, x)` surface mass balance (m ice eq. per year)
  - Coordinates: `time` as years, `x`, `y` as meters or km (monotonic)

- Configure `config.yaml` paths, then run:

```
python train.py --config config.yaml
python infer.py --config config.yaml
```

Inference writes NetCDF to `outputs/qtp_future/` with predicted 2020–2100 thickness.
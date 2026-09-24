# 1. Forcing and observational downloads

Run downloads on **`scp.chpc.ac.za`** or **`dtn.chpc.ac.za`** (outbound internet). Do **not** saturate `lengau` login nodes with CDS traffic.

## 1.1 CDS credentials

`~/.cdsapirc`:

```text
url: https://cds.climate.copernicus.eu/api
key: <UID>:<API-KEY>
```

Use a conda env that has `cdsapi` (analysis env may only have xarray).

## 1.2 ERA5 pressure levels (model forcing + verification)

**Dataset:** `reanalysis-era5-pressure-levels`  
**Product type:** `reanalysis`  
**Times:** `00:00`, `06:00`, `12:00`, `18:00`  
**Area (N, W, S, E)** used in this project: `[-10, 5, -40, 45]`  
**Format:** NetCDF

### Required variables

| Stream | Variables | Purpose |
|---|---|---|
| Dynamics | `u_component_of_wind`, `v_component_of_wind`, **`vertical_velocity`**, `geopotential` | Circulation, ω→w, height |
| Moisture | `specific_humidity` (+ others if needed) | IVT / VIMFC / 850 flux |

**Always request `vertical_velocity`.** Omitting it forces a continuity-based fallback that is weaker than native ERA5 ω (this happened for Nov 2022 until re-downloaded).

### Pressure levels

Prefer a **common** list across months:

```text
1000, 925, 850, 700, 500, 250, 200
```

(Some archived months used `300` instead of `250`; keep files self-consistent when merging.)

### Event months

| Month | Role |
|---|---|
| 2019-02 | Feb 2019 case |
| 2020-01 | Jan 2020 case |
| 2022-11 | Nov 2022 cases |

### Staging names (as used on Lustre)

```text
Obs_data/ERA5_Data/
  era5_pressure_levels_southern_africa_dynamics_YYYY_MM.nc
  era5_pressure_levels_southern_africa_moisture_YYYY_MM.nc
  ERA5_precip_southern_africa_YYYY_MM.nc
```

Example script: [`scripts/download_era5_pressure_levels_example.py`](../scripts/download_era5_pressure_levels_example.py).

## 1.3 ERA5 for MPAS initialisation

Separately from the regional verification cubes above, prepare **global** (or init-domain) ERA5 fields for `init_atmosphere` so that intermediate files `PRES:YYYY-MM-DD_HH` and SST updates exist for the full forecast window. Follow the MPAS-Atmosphere user’s guide for the required variables and vertical levels for your `init_atmosphere` namelist.

## 1.4 Observational rainfall

| Product | Notes |
|---|---|
| **CHIRPS v2.0** daily 0.05° | Primary skill reference |
| **GPCP** daily ~1° | Independent coarse estimate |
| **SAWS** gauges | Station max (SAWS box) vs station mean (analysis box) — not interchangeable |

## 1.5 Quality checks after download

```bash
# On any node with xarray / ncdump
ncdump -h era5_pressure_levels_southern_africa_dynamics_2022_11.nc | grep -E 'w |float w'
```

Confirm:

1. `w` present with units `Pa s**-1`
2. Time coverage covers the event window
3. Lat/lon orientation matches other months (southern Africa box)

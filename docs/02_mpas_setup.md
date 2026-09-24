# 2. MPAS setup (mesh, statics, physics, init)

## 2.1 Model version

- **MPAS-Atmosphere 8.2.2** (build tree e.g. `~/MPAS-Model-8.2.2`)
- Run on **CHPC Lengau** with site MPI/NetCDF libraries linked at build time

## 2.2 Mesh

| Property | Value |
|---|---|
| Mesh name | `x20.835586` |
| Cells | 835 586 |
| Spacing | ≈ 2.3–60 km (\(R_E\sqrt{A_{\mathrm{cell}}}\)); ~3 km over southern Africa |
| Domain | **Global** (`config_apply_lbcs = false`) |
| Mixing length | `config_len_disp = 3000` m |

Required files (linked into each run directory):

- `x20.835586.grid.nc`
- `x20.835586.graph.info` (+ `.part.N` for the chosen core count)
- `x20.835586.static.nc` (after static generation)
- `x20.835586.init.nc` (after meteorological init)
- optional `x20.835586.sfc_update.nc`

## 2.3 Vertical grid and time step

| Setting | Value |
|---|---|
| Vertical levels | 70 (`nVertLevels`) |
| Rayleigh damping start | `config_zd = 22000` m |
| Time step | `config_dt = 15` s |

## 2.4 Physics suite

```fortran
&physics
    config_physics_suite = 'mesoscale_reference'
    config_sst_update = true
    config_sstdiurn_update = true
    config_radtlw_interval = '00:30:00'
    config_radtsw_interval = '00:30:00'
/
```

Suite defaults (do not override unless intentional):

| Process | Scheme |
|---|---|
| Convection | New Tiedtke |
| Microphysics | WSM6 |
| PBL | YSU |
| Surface layer | Revised Monin–Obukhov |
| Land surface | Noah |
| Radiation | RRTMG LW/SW |
| Cloud fraction | Xu–Randall |
| Orographic GWD | YSU |

At ~3 km refined spacing this is a **grey-zone** configuration: deep convection remains parameterised.

## 2.5 Initial and surface forcing

1. Run **`init_atmosphere`** with ERA5 intermediate files → `PRES:…`, SST streams.
2. SST updated every **6 hours** during the forecast (`config_sst_update = true`).
3. No lateral BCs (global mesh).

## 2.6 Ensemble design

- **10 members:** `ENSB01` … `ENSB10`
- Production trees named `*_tpert` → **temperature perturbations** of the initial state
- Document amplitude / vertical structure in the run README when known (still a manuscript placeholder if not transcribed from setup scripts)

## 2.7 Suggested directory layout per member

```text
…/ensemble_<event>_tpert/auto_mpas_<tag>_ENSB##/6003km_outputs/
  mpas_init/     # init_atmosphere, PRES/SST intermediates, grid
  mpas_atmos/    # namelist.atmosphere, streams, tables, diag/history
```

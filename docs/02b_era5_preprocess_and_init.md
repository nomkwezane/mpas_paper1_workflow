# 2b. ERA5 preprocessing and `init_atmosphere`

This step sits **between** CDS/forcing downloads and the atmosphere ensemble
runs. It turns ERA5 fields into MPAS intermediate files and then into
`x20.835586.init.nc` (plus optional surface updates).

---

## Goals

1. Produce meteorological intermediate files `PRES:YYYY-MM-DD_HH` covering every
   init time and every SST-update time in the forecast window.
2. Build (once) static fields → `x20.835586.static.nc`.
3. Run `init_atmosphere` → `x20.835586.init.nc` (and `sfc_update` if used).
4. Hand the init file to the perturbation step ([02c](02c_ensemble_perturbation.md)).

---

## Conceptual pipeline

```text
ERA5 (grib/netCDF, global or large domain)
        │
        ▼
  ungrib / MPAS-compatible intermediate writer
        │
        ▼
  PRES:YYYY-MM-DD_HH   (+ SST / surface streams)
        │
        ▼
  init_atmosphere_model   (namelist.init_atmosphere)
        │
        ├── x20.835586.static.nc   (config_init_case for statics; once)
        └── x20.835586.init.nc     (meteorological init per event / member)
```

Follow the **MPAS-Atmosphere User’s Guide** for the exact variable list and
vertical levels required by your `namelist.init_atmosphere`. Paper 1 used ERA5
pressure-level atmospheric state and ERA5 SST updated every **6 hours**.

---

## Static fields (once per mesh)

Generate terrain, land-use, soil category and monthly vegetation fraction from
the **standard MPAS static datasets** shipped with the release (or the CHPC
mirror of those tarballs). Output: `x20.835586.static.nc`.

Record in your site notes:

- static dataset names / versions
- paths to the download tarballs on Lustre

(These names were still listed as “to be transcribed” in the internal methods
appendix at the time of writing.)

---

## Meteorological initialisation (per event)

| Event peak | Init (00 UTC) | Forecast window (analysis) |
|---|---|---|
| 11 Feb 2019 | 9 Feb 2019 | through 13 Feb 2019 |
| 9 Jan 2020 | 7 Jan 2020 | through 11 Jan 2020 |
| 7 & 11 Nov 2022 | 1 Nov 2022 | through 13 Nov 2022 |

Checklist:

1. Stage ERA5 for the full window at 6-hourly cadence.
2. Create `PRES:…` intermediates for every required time.
3. Run `init_atmosphere` with the production `namelist.init_atmosphere`.
4. Confirm `x20.835586.init.nc` exists and matches the mesh.
5. Enable SST updates for the atmosphere run
   (`config_sst_update = true`, diurnal update on).

Global mesh → **no LBCs** (`config_apply_lbcs = false`).

---

## Directory layout (per member / event)

```text
…/ensemble_<event>_tpert/auto_mpas_<tag>_ENSB##/6003km_outputs/
  mpas_init/     # PRES intermediates, static, init.nc, namelist.init_atmosphere
  mpas_atmos/    # namelist.atmosphere, streams, tables, diag/history
```

---

## Quality checks

```bash
ncdump -h x20.835586.init.nc | head
# confirm nCells matches mesh (835586), nVertLevels = 70
ls PRES:* | head
```

After successful init, proceed to **ensemble perturbation** before launching
`atmosphere_model` for members ENSB01–ENSB10.

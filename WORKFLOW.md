# Paper 1 — cleaned end-to-end workflow

Use this as a linear checklist. Details for each step are in `docs/`.

---

## 0. Prerequisites

- [ ] CHPC Lengau account; Lustre under `/home/$USER/lustre/`
- [ ] SSH to `lengau.chpc.ac.za` (compute) and `scp.chpc.ac.za` / `dtn.chpc.ac.za` (internet)
- [ ] CDS API key in `~/.cdsapirc` (for ERA5)
- [ ] Conda env with analysis stack (`python_env`: xarray, netCDF4, cartopy, matplotlib, …)
- [ ] Separate env with `cdsapi` if needed (`cdsapi_env`)
- [ ] MPAS-A **8.2.2** build + libraries; `convert_mpas` binary
- [ ] Modules: CDO 1.9.10 (and compilers as required by your MPAS build)

---

## 1. Download forcing and observational data

**Do this on `scp.chpc.ac.za` (or DTN), not the login node.**

1. Download **ERA5 pressure-level** fields for each event month (see [01_forcing_downloads.md](docs/01_forcing_downloads.md)):
   - Dynamics: `u`, `v`, **`w` (ω)**, `z` — **always include `vertical_velocity`**
   - Moisture: `q` (and related fields as needed)
   - Domain example used here: lat −10…−40°, lon 5…45°, 0.25°, 6-hourly
   - Levels: 1000, 925, 850, 700, 500, 250 or 300, 200 hPa
2. Download **ERA5 total precipitation** (hourly → later accumulate to daily).
3. Obtain **CHIRPS** daily `precip`, **GPCP** daily, **SAWS** gauge CSV.
4. Stage under:

```text
…/postprocessing/Obs_data/
  ERA5_Data/
  CHIRPS_Data/   (or as configured)
  GPCP_Data/
  SAWS_Data/
```

5. Spot-check NetCDF variables (`ncdump -h` / xarray). Confirm Nov dynamics has `w`.

---

## 2. Prepare MPAS mesh, statics, and initial conditions

1. Use (or generate) the variable-resolution mesh **`x20.835586`** (~835 586 cells; ~3 km over southern Africa → ~60 km global).
2. Build **static** fields with `init_atmosphere` (terrain, land use, soil, monthly veg).
3. Interpolate **ERA5** → mesh intermediate files `PRES:YYYY-MM-DD_HH` (and SST updates every 6 h).
4. Create `x20.835586.init.nc` (and `sfc_update` if used).
5. Confirm graph partition files for the intended core count (e.g. `x20.835586.graph.info.part.*`).

Details: [02_mpas_setup.md](docs/02_mpas_setup.md).

---

## 3. Configure and run the ensemble

For **each event** and **each member** `ENSB01`–`ENSB10`:

1. Copy a clean `mpas_atmos` run directory (namelist, streams, tables, mesh links).
2. Set `namelist.atmosphere`:
   - `config_physics_suite = 'mesoscale_reference'`
   - `config_dt = 15.0`, `config_len_disp = 3000.0`
   - `config_apply_lbcs = false` (global mesh)
   - `config_sst_update = true`
   - `config_start_time` / `config_run_duration` for that event
3. Apply the **temperature perturbation** that distinguishes the member (`*_tpert` ensembles).
4. Submit atmosphere jobs via PBS (`run_mpas_atmos.qsub` / site wrapper).
5. Archive `diag.*` / `history.*` / restarts under the member’s `6003km_outputs/mpas_atmos/`.

Event starts used in analysis:

| Event peak | Simulation start (00 UTC) |
|---|---|
| 11 Feb 2019 | 9 Feb 2019 |
| 9 Jan 2020 | 7 Jan 2020 |
| 7 & 11 Nov 2022 | 1 Nov 2022 |

Details: [03_running_simulations.md](docs/03_running_simulations.md).

---

## 4. Post-process native output → analysis NetCDF

For each year/member under `YYYY_ensemble_postprocessed_data/ENSB##/`:

1. Record provenance: `SOURCE_SIMULATION_DIR.txt`, `diag_sources_used.log`.
2. Run **`convert_mpas`** (native → lon–lat + pressure levels) → `latlon.nc`.
3. Run **CDO** scripts to split variables into six-hourly series:

```text
ua_hrs_mpas*_YYYY.nc   va_hrs_…   td_hrs_…   wa_hrs_…
hg/gz_hrs_…            ta_hrs_…   cape_hrs_… prc_hrs_…
```

4. If multilevel dynamics are missing or wrong, re-run:

```bash
cd …/publication_figures
qsub revised_dynstat/run_repost.pbs
# or: bash revised_dynstat/repostprocess_member.sh YEAR ENSB01
```

5. Audit:

```bash
qsub revised_dynstat/run_audit.pbs
```

Details: [04_postprocessing.md](docs/04_postprocessing.md).

---

## 5. Produce publication figures

Working directory:

```text
…/postprocessing/publication_figures/
```

| Product | Driver | Typical PBS |
|---|---|---|
| Manuscript Figs 1–6, 2b | `paper_draft_figures/run_all.py` | `run_paper_figures.pbs`, `run_fig0N.pbs` |
| Revised A–D (+ IVT E) | `revised_dynstat/run_all.py`, `fig_*.py` | `revised_dynstat/run.pbs`, `run_fig*.pbs` |
| Diagnostics Diag01–06 | `paper_draft_figures/diagnostics/run_diagnostics.py` | `run_diagnostics.pbs` |

**Vertical motion rule:** convert ERA5 ω → kinematic \(w\) before any MPAS `wa` comparison (`revised_dynstat/helpers.py` → `omega_to_w`).

Details: [05_publication_figures.md](docs/05_publication_figures.md).

---

## 6. Methods write-up

Manuscript-ready text and internal notes:

- `paper1_analysis/methodology/Methods_for_publication.md` (+ `.docx`/`.pdf`)
- `paper1_analysis/methodology/MPAS_methodology.md` (+ `.docx`/`.pdf`)

---

## 7. Definition of done

- [ ] All 10 members × 3 years have pressure-level `ua`/`va`/`wa`/`hg` (audit clean)
- [ ] ERA5 dynamics include `w` for **every** event month
- [ ] Figs 1–6 / A–D / Diag01–06 regenerated after any unit/loader fix
- [ ] Methods text matches code (ω→w, boxes, bootstrap, mesh/physics)

# Paper 1 — cleaned end-to-end workflow

Linear checklist. Details for each step are in `docs/`.  
**Read [REPRODUCIBILITY.md](REPRODUCIBILITY.md) first** for what is / is not
reproducible from this repository alone.

---

## 0. Prerequisites and software

- [ ] CHPC Lengau account; Lustre under `/home/$USER/lustre/`
- [ ] SSH to `lengau.chpc.ac.za` (compute) and `scp.chpc.ac.za` / `dtn.chpc.ac.za` (internet)
- [ ] CDS API key in `~/.cdsapirc`
- [ ] Conda env `python_env` (analysis) and optionally `cdsapi_env`
- [ ] MPAS-A **8.2.2** build + `init_atmosphere` + `convert_mpas`
- [ ] CDO **1.9.10**

Details: [00_software_stack.md](docs/00_software_stack.md).

---

## 1. Download forcing and observational data

**On `scp.chpc.ac.za` or `dtn.chpc.ac.za`, not the login node.**

1. ERA5 pressure-level **dynamics** (`u`,`v`,**`w`**,`z`) and **moisture** (`q`) for event months.
2. ERA5 total precipitation (hourly → daily later).
3. **Global / init-domain ERA5** for `init_atmosphere` (separate from regional verification cubes).
4. CHIRPS daily, GPCP daily, SAWS gauges.
5. Stage under `…/postprocessing/Obs_data/…`.
6. Spot-check: Nov dynamics must contain `w` (ω).

Details: [01_forcing_downloads.md](docs/01_forcing_downloads.md).

---

## 2. Preprocess ERA5 → statics and initial conditions

1. Build `x20.835586.static.nc` from MPAS static datasets.
2. Write `PRES:YYYY-MM-DD_HH` intermediates (+ SST streams) for each event window.
3. Run `init_atmosphere` → `x20.835586.init.nc` (and `sfc_update` if used).
4. Confirm `nCells = 835586`, `nVertLevels = 70`.

Details: [02b_era5_preprocess_and_init.md](docs/02b_era5_preprocess_and_init.md),
[02_mpas_setup.md](docs/02_mpas_setup.md).

---

## 3. Perturb the initial state (10 members)

1. Apply the production perturbation recipe inside **24–32°E, 28–24°S**:
   - \(T\): +0.2 K ≤850 hPa; −0.4 K >600 hPa; unchanged 600–850 hPa
   - \(u\) −0.6 m s⁻¹; \(v\) −0.5 m s⁻¹; \(q\) +6 % ≤850 hPa; Φ −20 m² s⁻² >600 hPa
   - Member jitter with seed `1000+i`
2. Driver on Lengau: `auto_mpas.era5.ens/bash_auto_perturb_parallel.sh`
3. Produce member trees `ENSB01`…`ENSB10` under `*_tpert` ensembles.

Details: [02c_ensemble_perturbation.md](docs/02c_ensemble_perturbation.md).

---

## 4. Configure and run the atmosphere model

For **each event** and **each member**:

1. Clean `mpas_atmos` directory (namelist, streams, tables, mesh links).
2. Set `namelist.atmosphere`:
   - `config_physics_suite = 'mesoscale_reference'`
   - `config_dt = 15.0`, `config_len_disp = 3000.0`
   - `config_apply_lbcs = false`, `config_sst_update = true`
   - event `config_start_time` / `config_run_duration`
3. Submit PBS atmosphere job.
4. Archive `diag.*` / `history.*` under `6003km_outputs/mpas_atmos/`.

| Event peak | Simulation start (00 UTC) |
|---|---|
| 11 Feb 2019 | 9 Feb 2019 |
| 9 Jan 2020 | 7 Jan 2020 |
| 7 & 11 Nov 2022 | 1 Nov 2022 |

Details: [03_running_simulations.md](docs/03_running_simulations.md).

---

## 5. Post-process native output → analysis NetCDF

For each year/member under `YYYY_ensemble_postprocessed_data/ENSB##/`:

1. Write provenance: `SOURCE_SIMULATION_DIR.txt`, `diag_sources_used.log`.
2. `convert_mpas` → `latlon.nc` (0.027° target domain).
3. CDO split → `ua|va|td|wa|hg|ta|cape|prc_hrs_*.nc` on seven pressure levels.
4. Re-post if multilevel dynamics are incomplete:
   `bash revised_dynstat/repostprocess_member.sh YEAR ENSB##`
5. Audit: `qsub revised_dynstat/run_audit.pbs`

Details: [04_postprocessing.md](docs/04_postprocessing.md).

---

## 6. Data analysis and publication figures

Working directory: `…/postprocessing/publication_figures/`

| Product | Driver / PBS |
|---|---|
| Figs 1–6, 2b | `paper_draft_figures/run_paper_figures.pbs` |
| Figures A–E | `revised_dynstat/run.pbs` |
| Diag01–06 | `paper_draft_figures/run_diagnostics.pbs` |

**Vertical motion rule:** convert ERA5 ω → kinematic \(w\) before any MPAS `wa`
comparison (`revised_dynstat/helpers.py` → `omega_to_w`).

Details: [05_publication_figures.md](docs/05_publication_figures.md),
[06_analysis_software.md](docs/06_analysis_software.md).

---

## 7. Methods write-up

- `paper1_analysis/methodology/Methods_for_publication.md` (+ docx/pdf)
- `paper1_analysis/methodology/MPAS_methodology.md` (+ docx/pdf)

---

## 8. Definition of done

- [ ] All 10 members × 3 years have pressure-level `ua`/`va`/`wa`/`hg` (audit clean)
- [ ] ERA5 dynamics include `w` for **every** event month
- [ ] Perturbation recipe matches [02c](docs/02c_ensemble_perturbation.md)
- [ ] Figs 1–6 / A–E / Diag01–06 regenerated after any unit/loader fix
- [ ] Methods text matches code (ω→w, boxes, bootstrap, mesh/physics)
- [ ] [REPRODUCIBILITY.md](REPRODUCIBILITY.md) gaps reviewed for archival freeze

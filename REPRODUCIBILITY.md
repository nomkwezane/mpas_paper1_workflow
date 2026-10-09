# Reproducibility audit

**Verdict (current state of this repository):** the workflow is **documented at a
level that supports scientific understanding and guided re-runs on CHPC Lengau**,
but it is **not yet sufficient for fully independent, bit-for-bit reproduction
from this GitHub tree alone**.

Use this page as the single source of truth for what is locked, what lives only
on Lustre, and what still blocks a cold start by a third party.

---

## Pipeline coverage

| Stage | Documented here? | Reproducible from this repo alone? | What is still needed |
|---|---|---|---|
| 1. Download forcing / obs | Yes — [01](docs/01_forcing_downloads.md) | **Partial** | Exact CDS request JSONs for *global* init ERA5; CHIRPS/GPCP/SAWS access paths; SAWS licence |
| 2. ERA5 → `PRES:` / SST preprocess | Yes — [02b](docs/02b_era5_preprocess_and_init.md) | **Partial** | Retained `ungrib`/WPS-style intermediate recipes and site paths |
| 3. Mesh, statics, `init_atmosphere` | Yes — [02](docs/02_mpas_setup.md) | **Partial** | Mesh binary (`x20.835586.*`), static dataset tarballs, full `namelist.init_atmosphere` |
| 4. Ensemble perturbation | Yes — [02c](docs/02c_ensemble_perturbation.md) | **Yes (recipe)** / **No (init files)** | Perturbation recipe is transcribed from `bash_auto_perturb_parallel.sh`; original `init.nc` no longer on disk |
| 5. Atmosphere run (PBS) | Yes — [03](docs/03_running_simulations.md) | **Partial** | Site core count, exact `streams.atmosphere`, full namelist dumps per event |
| 6. Post-process (`convert_mpas` + CDO) | Yes — [04](docs/04_postprocessing.md) | **Partial** | `target_domain_6003km.txt`, `cdompaszaxis.txt`, production CDO scripts on Lustre |
| 7. Completeness audit | Yes — [04](docs/04_postprocessing.md) | **Yes if code present** | Needs analysis tree on Lengau |
| 8. Figures / diagnostics | Yes — [05](docs/05_publication_figures.md) | **Yes if code + data present** | Analysis Python tree is *not* vendored in this repo |
| 9. Analysis software stack | Yes — [00](docs/00_software_stack.md) | **Partial** | Frozen `conda list --explicit` / `environment.yml` not yet archived here |

---

## What this repo *does* enable today

1. A **linear checklist** from download → figures ([WORKFLOW.md](WORKFLOW.md)).
2. Fixed scientific choices: MPAS-A **8.2.2**, mesh `x20.835586`, suite
   `mesoscale_reference`, 10-member perturbations, event dates, analysis boxes,
   ω→w conversion rule.
3. An **executable perturbation specification** (box, amplitudes, seeds) so the
   ensemble design can be re-implemented even without the original `init.nc`.
4. Operational CHPC rules (use `scp`/`dtn` for CDS; avoid `#PBS -V`; Lustre paths).
5. Pointers to the production figure drivers and PBS job names used for the paper.

---

## What blocks cold-start reproducibility

These items live on Lengau Lustre (or are licensed third-party data) and are
**not** in this GitHub repository:

| Asset | Typical location / note |
|---|---|
| Variable-resolution mesh + graph partitions | `x20.835586.grid.nc`, `.graph.info.part.*` |
| Static / init NetCDF and `PRES:` intermediates | Event `mpas_init/` trees (many TB historically) |
| Native `diag.*` / `history.*` | Member `mpas_atmos/` directories |
| Post-processed `*_hrs_*.nc` | `YYYY_ensemble_postprocessed_data/ENSB##/` |
| Observational cubes | `postprocessing/Obs_data/` |
| Analysis + figure code | `…/publication_figures/` (also mirrored locally as `paper1_analysis`) |
| Perturbation driver script | `auto_mpas.era5.ens/bash_auto_perturb_parallel.sh` |
| `convert_mpas` build + target domain file | `postprocessing/build_convert_mpas/`, `target_domain_6003km.txt` |

Without those assets, a reader can **understand and re-implement** the workflow,
but cannot regenerate the published NetCDF or figures from this repo alone.

---

## Recommended path to *full* reproducibility

Work remaining (ordered):

1. **Archive** (Zenodo / institutional store, not GitHub LFS for multi-TB):
   sample member `init`+`diag` for one event, post-processed ENSB01 packs, obs cubes used in figures.
2. **Vendor or submodule** the analysis code (`paper_draft_figures/`, `revised_dynstat/`) with a pinned commit.
3. Commit a frozen **`environment.yml`** (or `conda list --explicit`) and a Lengau **module list**.
4. Commit sanitized copies of **`namelist.atmosphere`**, **`streams.atmosphere`**,
   **`namelist.init_atmosphere`**, and `target_domain_6003km.txt`.
5. Commit the **perturbation shell script** (or a Python reimplementation matching [02c](docs/02c_ensemble_perturbation.md)).
6. Publish DOIs / download URLs for CHIRPS, ERA5, GPCP, and the SAWS data-use statement.

Until steps 1–5 are done, cite this repository as a **workflow and methods
companion**, not as a standalone reproduction package.

---

## Definition of “reproduced” for Paper 1

A successful reproduction means:

- [ ] Same mesh name / cell count and physics suite
- [ ] Same init times and run lengths for the three event years
- [ ] Same perturbation box and amplitudes (or documented justified variant)
- [ ] Post-processed fields on the seven pressure levels at 6-hourly cadence
- [ ] Completeness audit clean for 10 × 3 members
- [ ] Figures regenerate with the same ω→w rule, boxes, and bootstrap settings
- [ ] Methods text matches code (rainfall product roles; SAWS max ≠ mean ≠ CHIRPS)

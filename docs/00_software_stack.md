# 0. Software stack and compute environment

This page lists the tools used from download through figure production on
**CHPC Lengau**. Pin exact module / conda builds when you archive a frozen
reproduction package (`conda list --explicit` is preferred).

---

## 0.1 Hosts

| Host | Role |
|---|---|
| `lengau.chpc.ac.za` | Login, `qsub`, light checks |
| `scp.chpc.ac.za` | Outbound internet (CDS downloads), file transfer |
| `dtn.chpc.ac.za` | Large transfers / Globus; also usable for CDS |
| Lustre | All model I/O and post-processed data (`/home/$USER/lustre/…`) |

Do **not** run multi-GB CDS downloads on the shared login node.

---

## 0.2 Model build

| Component | Version / note |
|---|---|
| MPAS-Atmosphere | **8.2.2** |
| MPI / NetCDF / PIO | Site libraries linked at CHPC build time |
| `init_atmosphere_model` | From the same MPAS release |
| `atmosphere_model` | Production forecast binary |
| `convert_mpas` | Built separately under `postprocessing/build_convert_mpas/` |

Record the Lengau module stack used to **compile** MPAS in your site notes
(compiler, MPI, NetCDF, ParallelIO). Rebuilds with a different stack may change
bit-level output even with identical namelists.

---

## 0.3 Runtime modules (typical analysis / CDO)

Used during post-processing and figure jobs (exact names may differ by CHPC
modulefile revision):

| Tool | Version used in Paper 1 |
|---|---|
| CDO | **1.9.10** |
| ncdump / NCO | as available on Lengau |
| PBS Pro | site scheduler |

Prefer **explicit** `module load …` inside PBS scripts. Avoid `#PBS -V` when the
login environment is polluted.

---

## 0.4 Python analysis environment

Production figures use a conda env conventionally named **`python_env`**:

```text
~/.conda/envs/python_env/
```

Core packages (minimum):

| Package | Role |
|---|---|
| Python 3.x | Drivers |
| xarray, netCDF4 | NetCDF I/O |
| numpy, scipy, pandas | Numerics / tables |
| matplotlib | Plotting (`MPLBACKEND=Agg` on PBS) |
| cartopy, geopandas, shapely | Maps / polygons |
| pyproj / PROJ data | Cartopy CRS (`PROJ_DATA` / `PROJ_LIB` must be set on PBS) |

CDS downloads may use a separate env (e.g. **`cdsapi_env`**) with `cdsapi` only.

### Freeze for archival (run on Lengau)

```bash
conda activate python_env
conda env export --no-builds > environment_python_env.yml
conda list --explicit > environment_python_env.explicit.txt
```

Commit those files into this repository when preparing a public freeze.
They are **not yet** checked in (see [REPRODUCIBILITY.md](../REPRODUCIBILITY.md)).

---

## 0.5 PBS hygiene for figure / post-process jobs

```bash
#PBS -l select=1:ncpus=4:mpiprocs=4:mem=32gb
# explicit modules and exports — do not rely on interactive login state

export PYTHONUNBUFFERED=1
export MPLBACKEND=Agg
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export PYTHONPATH=/home/$USER/lustre/MPAS/2025/era_runs/postprocessing/publication_figures
export PROJ_DATA=/home/$USER/.conda/envs/python_env/share/proj
export PROJ_LIB=$PROJ_DATA
```

Template: [`templates/lengau_job.pbs.example`](../templates/lengau_job.pbs.example).

---

## 0.6 Companion code locations

| Tree | Contents |
|---|---|
| This repo (`mpas_paper1_workflow`) | Workflow documentation + example download / namelist snippets |
| Lengau `…/publication_figures/` | Production Python (`paper_draft_figures/`, `revised_dynstat/`) + PBS |
| Local `paper1_analysis` | Working copy / sync of analysis + `methodology/` |
| Lengau `auto_mpas.era5.ens/` | Ensemble automation, including `bash_auto_perturb_parallel.sh` |

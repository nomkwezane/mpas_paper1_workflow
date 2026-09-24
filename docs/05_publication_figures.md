# 5. Publication figures and diagnostics

Working root on Lengau:

```text
/home/$USER/lustre/MPAS/2025/era_runs/postprocessing/publication_figures/
```

Requires `PYTHONPATH` to include that directory and the analysis conda env (`python_env`).

---

## 5.1 Analysis domains (config)

Defined in `paper_draft_figures/config.py`:

| Name | Box | Use |
|---|---|---|
| `ANALYSIS_BOX` | 26.5–25.5°S, 27.5–28.5°E | Area means, skill vs CHIRPS |
| `SAWS_BOX` | 27.0–25.0°S, 26.5–29.0°E | Station **maximum** time series |
| `RSA_BOX` / `SA_BOX` | RSA / southern Africa | Spatial maps |

**Do not** compare SAWS station max directly to MPAS grid-box means for skill scores.

---

## 5.2 Vertical velocity convention

| Source | Field | Units | Sign |
|---|---|---|---|
| MPAS | `wa` | m s⁻¹ | ascent **> 0** |
| ERA5 | `w` | Pa s⁻¹ (ω) | ascent **< 0** |

Convert before comparison:

\[
w = -\frac{\omega}{\rho g},\quad \rho = \frac{p}{R_d T}
\]

Implemented in `revised_dynstat/helpers.py` (`omega_to_w`).  
Difference maps: \(\Delta w = w_{\mathrm{ERA5}} - w_{\mathrm{MPAS}}\).

---

## 5.3 Manuscript figures (`paper_draft_figures/`)

| Fig | Script entry | Typical PBS |
|---|---|---|
| 1 Context map | `figures.plot_fig01` | `run_fig01.pbs` |
| 2 Daily series | `plot_fig02` | `run_fig02.pbs` |
| 2b Event totals | `plot_fig02b` (+ SAWS variant) | `run_fig02b.pbs` |
| 3 Accumulation | `plot_fig03` | `run_fig03.pbs` |
| 4 Skill | `plot_fig04` | `run_fig04.pbs` |
| 5 Peak-day rain diffs | `plot_fig05` | `run_fig05.pbs` |
| 6 Moisture flux | `plot_fig06` | `run_fig06.pbs` |

Batch:

```bash
qsub paper_draft_figures/run_paper_figures.pbs
# or
python -u paper_draft_figures/run_all.py --only 2 2b 4
```

Outputs: `figures/paper_draft_regen/`, tables under `tables/paper_draft_regen/`.

---

## 5.4 Revised dynamics–statistics figures (`revised_dynstat/`)

| Fig | Content | Key modules |
|---|---|---|
| A | IVT / VIMFC / 850 moisture flux | `fig_a.py` |
| B | Vertical motion profiles + maps | `fig_b.py` |
| C | Object / FSS / CSI | `fig_c.py` |
| D | Process attribution Δflux / Δw maps | `fig_d.py` |
| E | IVT peak-day panels | `fig_ivt_panels.py` |
| D supp. | Geopotential / wind diffs | `fig_d_geopot.py` |

```bash
qsub revised_dynstat/run.pbs
qsub revised_dynstat/run_figBD_wfix.pbs   # B + D after ω→w fixes
qsub revised_dynstat/run_fig_ivt_panels.pbs
```

Outputs: `figures/revised_dynstat/`, `tables/revised_dynstat/`.

---

## 5.5 Diagnostics Diag01–06

Driver: `paper_draft_figures/diagnostics/run_diagnostics.py`

| ID | Content |
|---|---|
| Diag01 | VIMFC / IVT timeseries |
| Diag02 | FSS + contingency |
| Diag03 | Rainfall QQ |
| Diag04 | Skill summary + bootstrap CIs |
| Diag05 | CAPE; \(w\) profiles; combined `Diag05_cape_and_w_profiles` |
| Diag06 | November split-event attribution |

```bash
qsub paper_draft_figures/run_diagnostics.pbs
qsub paper_draft_figures/run_diag05_combo.pbs
```

Bootstrap (skill CIs): IID paired-day resample, `n_boot=500`, 95% percentile CI.

---

## 5.6 PBS hygiene (Lengau)

Prefer:

```bash
#PBS -l select=1:ncpus=4:mpiprocs=4:mem=32gb
# explicit env exports — avoid #PBS -V when login env is polluted
```

Set:

```bash
export MPLBACKEND=Agg
export PYTHONUNBUFFERED=1
export PYTHONPATH=…/publication_figures
export PROJ_DATA=…/conda/envs/python_env/share/proj
```

---

## 5.7 After any loader/unit change

1. Re-run affected figure PBS jobs  
2. Copy PNG/PDF from Lustre to the local `figures/` tree if needed  
3. Confirm Methods text still matches the code

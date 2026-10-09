# 6. Data-analysis software and figure drivers

The scientific analysis is **Python-based** and lives primarily on Lengau under:

```text
/home/$USER/lustre/MPAS/2025/era_runs/postprocessing/publication_figures/
```

A working copy is often synced locally as `paper1_analysis`. **This workflow
repository documents the drivers; it does not currently vendor the full Python
tree** (see [REPRODUCIBILITY.md](../REPRODUCIBILITY.md)).

---

## 6.1 Package layout

| Package / directory | Role |
|---|---|
| `paper_draft_figures/` | Manuscript Figs 1–6 (+ 2b), config, data loaders |
| `paper_draft_figures/diagnostics/` | Diag01–06 |
| `revised_dynstat/` | Figures A–E, audit, re-post helpers |
| `figures/`, `tables/` | PNG/PDF and CSV outputs |
| `methodology/` (local tree) | Methods markdown / docx / pdf |

---

## 6.2 Key modules (by concern)

| Concern | Where |
|---|---|
| Event dates, boxes, paths | `paper_draft_figures/config.py` |
| NetCDF loaders, time-axis fallback | `paper_draft_figures/data.py` |
| ω → kinematic \(w\) | `revised_dynstat/helpers.py` → `omega_to_w` |
| Skill / bootstrap | Diag04 / Fig04 code (`n_boot=500`, 95 % percentile CI) |
| Completeness audit | `revised_dynstat/` + `run_audit.pbs` |
| Member re-post | `revised_dynstat/repostprocess_member.sh` |

---

## 6.3 Recommended run order (analysis only)

Assuming post-processed MPAS + obs are already on Lustre:

```bash
cd …/postprocessing/publication_figures

qsub revised_dynstat/run_audit.pbs          # 1. data complete?
qsub paper_draft_figures/run_paper_figures.pbs
qsub revised_dynstat/run.pbs
qsub paper_draft_figures/run_diagnostics.pbs
```

Details: [05_publication_figures.md](05_publication_figures.md).

---

## 6.4 Non-negotiable analysis conventions

1. **Vertical motion:** ERA5 `w` is ω (Pa s⁻¹); convert before comparing to MPAS `wa`.
2. **Rainfall products are not interchangeable:**
   SAWS station max ≠ SAWS box mean ≠ CHIRPS ≠ MPAS box mean.
3. **Skill reference:** CHIRPS for continuous / spatial scores.
4. **Time axis:** do not trust all CF units; use provenance + fallback inits.
5. **Precipitation:** treat `prc` as increments; negatives / fill → missing.

---

## 6.5 Methods documents

| File | Use |
|---|---|
| `methodology/Methods_for_publication.md` | Manuscript-oriented methods |
| `methodology/MPAS_methodology.md` | Extended methods + internal appendices |

Keep those texts synchronized with this workflow after any loader or unit fix.

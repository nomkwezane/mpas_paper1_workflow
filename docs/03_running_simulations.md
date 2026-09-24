# 3. Running the simulations

## 3.1 Events and windows

| Peak day | Init (00 UTC) | Typical post-processed window |
|---|---|---|
| 11 Feb 2019 | 9 Feb 2019 | 9–13 Feb 2019 |
| 9 Jan 2020 | 7 Jan 2020 | 7–11 Jan 2020 (analysis) |
| 7 Nov 2022 | 1 Nov 2022 | 1–13 Nov 2022 |
| 11 Nov 2022 | (same Nov run) | verified separately |

Lead times to peaks ≈ 48 h (2019), 48 h (2020), 144 h (7 Nov), 240 h (11 Nov).

## 3.2 Per-member checklist

1. Fresh `mpas_atmos` directory with correct mesh links and physics tables.
2. Edit `namelist.atmosphere`:
   - start time / run duration for the event
   - physics suite / SST flags (see setup doc)
   - decomposition prefix matching available `.part.*` files
3. Apply member-specific **temperature perturbation** (ensemble generation step).
4. Configure `streams.atmosphere` for the desired `diag` / `history` cadence (analysis uses **6-hourly** post-processed fields).
5. Submit PBS job (site wrapper / `run_mpas_atmos.qsub`). Prefer clean PBS (explicit modules, memory request; avoid inheriting a polluted login environment with `-V` unless you know it is safe).
6. After completion, verify `diag.*` / `history.*` cover the event window.

## 3.3 Provenance for post-processing

Write (or retain) for each post-processed member:

- `SOURCE_SIMULATION_DIR.txt` → path to `mpas_atmos`
- `diag_sources_used.log` → list of `diag.*.nc` files ingested
- optional `SOURCE_GRID_FILE.txt`

These files are required by `repostprocess_member.sh` and by time-axis reconstruction in the figure loaders.

## 3.4 Operational tips (Lengau)

- Do **not** stage large downloads on login nodes → use **scp** / **dtn**.
- Keep run directories on **Lustre**, not `$HOME`.
- After crashes, restart from `restart.*` only if namelist/streams are consistent; otherwise re-init carefully and document.

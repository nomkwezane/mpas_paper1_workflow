# 4. Post-processing

Goal: turn native unstructured MPAS output into regular lon–lat, pressure-level, six-hourly NetCDF series consumed by the figure codes.

## 4.1 Tools

| Tool | Role |
|---|---|
| `convert_mpas` | Native mesh → lon–lat; height → pressure levels |
| CDO 1.9.10 | Split / calendar / de-accumulate precipitation |
| `cdompaszaxis.txt` | Target pressure axis |

Typical pressure levels archived:

```text
1000, 925, 850, 700, 500, 250, 200 hPa
```

## 4.2 Output products per member

Directory pattern:

```text
postprocessing/YYYY_ensemble_postprocessed_data/ENSB##/
  ua_hrs_mpas##_YYYY.nc
  va_hrs_mpas##_YYYY.nc
  td_hrs_mpas##_YYYY.nc
  wa_hrs_mpas##_YYYY.nc    # kinematic w [m s-1]
  hg_hrs_… / gz_hrs_…
  ta_hrs_…
  cape_hrs_…
  prc_hrs_…                # increment per output interval [mm]
  SOURCE_SIMULATION_DIR.txt
  diag_sources_used.log
```

## 4.3 Standard pipeline (conceptual)

```text
diag/history (native)
        │
        ▼
   convert_mpas  →  latlon.nc
        │
        ▼
   CDO split     →  <var>_hrs_mpas<prefix>_<year>.nc
```

Driver used when re-building missing multilevel fields:

```bash
cd …/publication_figures
bash revised_dynstat/repostprocess_member.sh YEAR MEMBER
# batch:
qsub revised_dynstat/run_repost.pbs
```

## 4.4 Time-axis caveats (important)

Figure loaders **do not trust** all CF time units. They reconstruct valid times as hours since a known init (`FALLBACK_START` in `paper_draft_figures/data.py`):

| Year | Fallback init |
|---|---|
| 2019 | 2019-02-09 00:00 |
| 2020 | 2020-01-07 00:00 |
| 2022 | 2022-11-01 00:00 |

Corrupt units (e.g. `%Y%m%d` templates, wrong reference year) are rejected. CDO padding with negative times is discarded.

## 4.5 Precipitation treatment

- Treat `prc` as an **increment**, not a running accumulation.
- Non-finite, fill-value, and negative increments → missing (zeros when forming totals).

## 4.6 Completeness audit

```bash
qsub revised_dynstat/run_audit.pbs
```

Writes:

- `tables/revised_dynstat/data_completeness.csv`
- `tables/revised_dynstat/data_completeness_summary.csv`

Confirm every member has a **`lev`** dimension on dynamical fields before interpreting “ensemble mean” panels.

# Paths and conventions

## Lustre layout (Paper 1)

```text
/home/$USER/lustre/MPAS/2025/era_runs/
├── auto_mpas.era5.ens/          # mesh utils, some shared assets
├── ensemble_*_tpert/            # event ensembles (members)
└── postprocessing/
    ├── Obs_data/                # ERA5, CHIRPS, GPCP, SAWS
    ├── YYYY_ensemble_postprocessed_data/ENSB##/
    ├── shape_files/
    ├── postprocs_scripts/
    ├── build_convert_mpas/
    └── publication_figures/     # Python analysis + PBS + figure outputs
        ├── paper_draft_figures/
        ├── revised_dynstat/
        ├── figures/
        └── tables/
```

## Events

| id | label | peak | year |
|---|---|---|---|
| 2019-02-11 | 11 Feb 2019 | 2019-02-11 | 2019 |
| 2020-01-09 | 9 Jan 2020 | 2020-01-09 | 2020 |
| 2022-11-07 | 7 Nov 2022 | 2022-11-07 | 2022 |
| 2022-11-11 | 11 Nov 2022 | 2022-11-11 | 2022 |

## Rainfall product roles

| Product | Role |
|---|---|
| SAWS station **max** (`SAWS_BOX`) | Daily time series; ≥20 mm event definition |
| SAWS station **mean** (`ANALYSIS_BOX`) | Event-total bars |
| CHIRPS | Continuous + spatial skill reference |
| MPAS ens / single box mean | Verified against CHIRPS |

## Hosts

| Host | Use |
|---|---|
| `lengau.chpc.ac.za` | Login, `qsub`, light checks |
| `scp.chpc.ac.za` | File transfer + **internet downloads** |
| `dtn.chpc.ac.za` | Globus / large transfers (+ internet) |

## Related methodology documents

In the analysis tree (not necessarily this workflow repo):

- `methodology/Methods_for_publication.md`
- `methodology/MPAS_methodology.md`

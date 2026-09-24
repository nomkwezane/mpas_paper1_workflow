# Example scripts

| Script | Purpose |
|---|---|
| `download_era5_pressure_levels_example.py` | CDS download of ERA5 pressure-level dynamics (include `vertical_velocity`) |

Run CDS downloads on **`scp.chpc.ac.za`** or **`dtn.chpc.ac.za`**, not the Lengau login node.

```bash
# on scp/dtn
conda activate cdsapi_env   # or any env with cdsapi
python download_era5_pressure_levels_example.py
```

Figure generation and post-processing live in the analysis tree on Lustre:

```text
…/postprocessing/publication_figures/
```

See [docs/05_publication_figures.md](../docs/05_publication_figures.md).

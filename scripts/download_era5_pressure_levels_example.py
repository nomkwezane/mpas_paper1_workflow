#!/usr/bin/env python3
"""Example: download ERA5 pressure-level dynamics for one month (CDS).

Run on scp.chpc.ac.za or dtn.chpc.ac.za (internet), not the Lengau login node.

Requires ~/.cdsapirc and:  pip/conda install cdsapi
"""
from __future__ import annotations

from pathlib import Path

import cdsapi

# --- edit these ---
YEAR = "2022"
MONTH = "11"
OUT = Path(f"era5_pressure_levels_southern_africa_dynamics_{YEAR}_{MONTH}.nc")
AREA = [-10, 5, -40, 45]  # N, W, S, E
LEVELS = ["1000", "925", "850", "700", "500", "250", "200"]
TIMES = ["00:00", "06:00", "12:00", "18:00"]
DAYS = [f"{d:02d}" for d in range(1, 32)]
# ------------------


def main() -> None:
    client = cdsapi.Client()
    request = {
        "product_type": "reanalysis",
        "variable": [
            "u_component_of_wind",
            "v_component_of_wind",
            "vertical_velocity",  # required — do not omit
            "geopotential",
        ],
        "pressure_level": LEVELS,
        "year": YEAR,
        "month": MONTH,
        "day": DAYS,
        "time": TIMES,
        "area": AREA,
        "data_format": "netcdf",
        "download_format": "unarchived",
    }
    print("Retrieving →", OUT.resolve())
    print(request)
    client.retrieve("reanalysis-era5-pressure-levels", request, str(OUT))
    print("Done:", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()

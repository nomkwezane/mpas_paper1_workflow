# 2c. Ensemble perturbation (temperature / wind / humidity / geopotential)

Paper 1 uses a **10-member** ensemble (`ENSB01`–`ENSB10`) generated from a
common ERA5-based initial state. Production trees are named `*_tpert`.

**Primary driver (Lengau):**  
`era_runs/auto_mpas.era5.ens/bash_auto_perturb_parallel.sh`

The original perturbed `init.nc` files are **no longer on disk**. Amplitudes
below are those written in the retained generation script (also transcribed into
`methodology/Methods_for_publication.md` / `MPAS_methodology.md`). They were
**not** re-measured from archived initial conditions.

---

## Spatial box

Perturbations are applied inside:

| Bound | Value |
|---|---|
| Longitude | 24°E – 32°E |
| Latitude | 28°S – 24°S |

(Outside this box the initial state is left unchanged by the script.)

---

## Base amplitudes (all members)

| Field | Rule |
|---|---|
| Temperature | **+0.2 K** at and **below 850 hPa**; **−0.4 K** **above 600 hPa**; **unchanged** between 600 and 850 hPa |
| Zonal wind \(u\) | **−0.6 m s⁻¹** |
| Meridional wind \(v\) | **−0.5 m s⁻¹** |
| Specific humidity \(q\) | **+6 %** at and **below 850 hPa** |
| Geopotential | **−20 m² s⁻²** **above 600 hPa** |

---

## Member jitter (member index \(i = 1\ldots10\))

| Field | Max jitter | Seed |
|---|---|---|
| Temperature | ≤ **0.05 K** | `1000 + i` |
| Wind components | ≤ **0.1 m s⁻¹** | same seeded sequence family |
| Humidity factor | ≤ **0.01** (absolute on the multiplicative factor) | same |
| Geopotential | ≤ **4 m² s⁻²** | same |

The script records **one amplitude set** and **one seed sequence** for all ten
members. Re-implementations should match these values and the box exactly if the
goal is to regenerate an equivalent ensemble design.

---

## Operational checklist

1. Build the unperturbed `x20.835586.init.nc` for the event
   ([02b](02b_era5_preprocess_and_init.md)).
2. Run (or reimplement) `bash_auto_perturb_parallel.sh` → 10 member inits.
3. Place each member under its `ENSB##` run tree with matching
   `namelist.atmosphere` / `streams.atmosphere`.
4. Submit atmosphere jobs ([03](03_running_simulations.md)).
5. Keep a copy of the perturbation script and a checksum log of each
   `init.nc` (recommended for future archives — not available for the original
   Paper 1 inits).

---

## Interpretation note

The ensemble mean is treated as the component of the forecast that is robust to
this initial-state uncertainty. Derived diagnostics (IVT, VIMFC, …) are computed
**per member then averaged**, not from the ensemble-mean state.

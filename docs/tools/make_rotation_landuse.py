#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_rotation_landuse.py — template for a transient crop-rotation land-use
file for eCLM_FYM_fixes, consumed via the `transient_landuse_file` namelist
entry together with `use_covercropping = .true.` (and `use_fruittree =
.true.`, which this branch requires alongside it).

Design choice, deliberate: crop names are resolved to CFT indices by reading
`pftname` from the parameter file the case actually uses, rather than from a
hardcoded index table. Hardcoded PFT/CFT indices have twice caused real bugs
in this branch's history (an out-of-bounds literal index in the base
pftconMod.F90, and a near-miss in a migration script's own crop-to-index
table) — do not reintroduce that pattern here, including when customizing
this file.

Typical use:
    # 1. Find the exact crop names in your parameter file:
    python3 make_rotation_landuse.py --paramfile <params>.nc --list-crops

    # 2. Edit the ROTATION and DOMAIN blocks below using those exact names.

    # 3. Build the file:
    python3 make_rotation_landuse.py --paramfile <params>.nc -o <rotation>.nc

`<params>.nc` must be the SAME file passed as both `paramfile` and
`covercrop_paramfile` in the case's lnd_in — the CFT ordering has to match
what the running executable actually reads.
"""
import argparse
import sys

import numpy as np
import netCDF4 as nc


# =============================================================================
# 1. ROTATION — edit this. One entry per simulated year.
#
#    year    : calendar year. Per this branch's convention, "year N is the
#              crop harvested in year N" — a winter crop entered for 2015 is
#              sown in autumn 2014, not 2015.
#    main    : the main (current-year) crop, harvested that year.
#    winter  : optional winter cover crop sown in autumn of that year, or
#              None to leave the winter slot empty (bare overwinter, or a
#              spring crop sown directly in the following year).
#
#    Names must match `pftname` entries in --paramfile exactly (case and
#    spacing included) — run with --list-crops first to get them right.
# =============================================================================
ROTATION = [
    # year,  main crop,                  winter cover crop
    (2011,   "irrigated_winter_wheat",   None),
    (2012,   "winter_barley",            "covercrop_1"),
    (2013,   "sugarbeet",                None),
    (2014,   "winter_wheat",             "covercrop_2"),
    (2015,   "winter_rye",               None),
]

# =============================================================================
# 2. DOMAIN — edit this to match your case's domain/surface file.
#    One (lon, lat) pair per gridcell; a 1x1 point case has exactly one.
# =============================================================================
LON = [6.30]     # degrees east
LAT = [50.87]    # degrees north
# =============================================================================


def resolve_cft_index(pftnames_clean, crop_name):
    """Resolve a crop name to its CFT index (PFT index - 15) by looking it up
    in the parameter file's own pftname array. Never hardcode this mapping —
    it is not stable across parameter files."""
    try:
        pft_idx = pftnames_clean.index(crop_name)
    except ValueError:
        raise SystemExit(
            f"'{crop_name}' not found in pftname.\n"
            f"Run with --list-crops to see the exact names available in "
            f"this parameter file."
        )
    cft_idx = pft_idx - 15
    if cft_idx < 0:
        raise SystemExit(
            f"'{crop_name}' resolved to PFT index {pft_idx}, which is not a "
            f"crop PFT (CFT indices start at PFT 15). Check the name — this "
            f"looks like a non-crop PFT."
        )
    return pft_idx, cft_idx


def load_pftnames(paramfile):
    with nc.Dataset(paramfile) as p:
        if "pftname" not in p.variables:
            raise SystemExit(f"'pftname' not found in {paramfile} — is this "
                              f"a CLM5/eCLM parameter file?")
        raw = nc.chartostring(p["pftname"][:])
    return [str(n).strip() for n in raw]


def list_crops(paramfile):
    names = load_pftnames(paramfile)
    print(f"{'PFT idx':>7}  {'CFT idx':>7}  name")
    for pft_idx, name in enumerate(names):
        if not name:
            continue
        cft_idx = pft_idx - 15
        tag = f"{cft_idx:7d}" if cft_idx >= 0 else "      -"
        print(f"{pft_idx:7d}  {tag}  {name}")


def build(paramfile, out_path):
    pftnames = load_pftnames(paramfile)
    n_cft = len(pftnames) - 15  # CFTs occupy PFT indices 15..mxpft
    if n_cft <= 0:
        raise SystemExit(f"{paramfile}: fewer than 16 PFT entries — does "
                          f"not look like a crop-enabled parameter file.")

    years = [r[0] for r in ROTATION]
    if len(set(years)) != len(years):
        raise SystemExit("ROTATION has duplicate years — one entry per year.")
    n_time = len(years)
    n_grid = len(LON)
    if len(LAT) != n_grid:
        raise SystemExit("LON and LAT must be the same length.")

    pct_cft = np.zeros((n_time, n_cft, n_grid), dtype="f8")
    pct_cft_winter = np.zeros((n_time, n_cft, n_grid), dtype="f8")
    have_winter = np.zeros(n_time, dtype=bool)

    print("Resolving rotation against", paramfile)
    for t, (year, main_crop, winter_crop) in enumerate(ROTATION):
        main_pft, main_cft = resolve_cft_index(pftnames, main_crop)
        pct_cft[t, main_cft, :] = 100.0
        line = f"  {year}: {main_crop} (PFT {main_pft} -> CFT {main_cft})"
        if winter_crop is not None:
            win_pft, win_cft = resolve_cft_index(pftnames, winter_crop)
            pct_cft_winter[t, win_cft, :] = 100.0
            have_winter[t] = True
            line += f"  + {winter_crop} (PFT {win_pft} -> CFT {win_cft})"
        print(line)

    with nc.Dataset(out_path, "w", format="NETCDF4_CLASSIC") as d:
        d.createDimension("time", n_time)
        d.createDimension("cft", n_cft)
        d.createDimension("lndgrid", n_grid)

        v_year = d.createVariable("YEAR", "i4", ("time",))
        v_year[:] = years
        v_year.long_name = "calendar year of each time slice"

        # LONGXY/LATIXY follow the conventional landuse.timeseries layout;
        # drop them if your surface/domain-matching pathway doesn't expect
        # them on this file.
        v_lon = d.createVariable("LONGXY", "f8", ("lndgrid",))
        v_lon[:] = LON
        v_lon.units = "degrees_east"

        v_lat = d.createVariable("LATIXY", "f8", ("lndgrid",))
        v_lat[:] = LAT
        v_lat.units = "degrees_north"

        v_main = d.createVariable("PCT_CFT", "f8", ("time", "cft", "lndgrid"))
        v_main[:] = pct_cft
        v_main.long_name = "percent crop functional type, main crop"
        v_main.units = "percent of the crop landunit"

        if have_winter.any():
            v_win = d.createVariable("PCT_CFT_WINTER", "f8",
                                      ("time", "cft", "lndgrid"))
            v_win[:] = pct_cft_winter
            v_win.long_name = "percent crop functional type, winter cover crop"
            v_win.units = "percent of the crop landunit"
        else:
            print("  (no winter cover crops in ROTATION - PCT_CFT_WINTER "
                  "omitted)")

        d.history = ("Generated by make_rotation_landuse.py for "
                      "eCLM_FYM_fixes; CFT indices resolved from pftname "
                      "in " + paramfile)
        d.rotation_source_paramfile = paramfile

    print(f"\nWrote {out_path}: {n_time} years ({years[0]}-{years[-1]}), "
          f"{int(have_winter.sum())}/{n_time} with a winter cover crop.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paramfile", required=True,
                     help="parameter file whose pftname array defines the CFT "
                          "ordering (must match paramfile/covercrop_paramfile "
                          "in the case's lnd_in)")
    ap.add_argument("--list-crops", action="store_true",
                     help="print every named PFT/CFT in --paramfile and exit "
                          "(use this to get exact names for the ROTATION list)")
    ap.add_argument("-o", "--out", dest="out_path",
                     help="output transient land-use file (required unless "
                          "--list-crops)")
    args = ap.parse_args()

    if args.list_crops:
        list_crops(args.paramfile)
        return
    if not args.out_path:
        ap.error("-o/--out is required unless --list-crops is given")
    build(args.paramfile, args.out_path)


if __name__ == "__main__":
    sys.exit(main())

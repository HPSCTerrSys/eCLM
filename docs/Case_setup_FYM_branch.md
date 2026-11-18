# Setting up a case on `eCLM_FYM_fixes`

A working-level guide to building this branch and running a case two ways:
unchanged, as a drop-in replacement for an existing single-crop setup, and
then with the branch's own functionality — prognostic crop rotation and
organic-fertiliser (FYM) carbon routing — enabled. Written for someone who
already runs eCLM/CLM5 cases; it does not re-explain CIME/CTSM case
mechanics. For what each feature actually does and why, see
[`eCLM_FYM_branch_guide.md`](eCLM_FYM_branch_guide.md) in this same
directory — this document is the "how", that one is the "what".

## 0. Prerequisites

- A working single-crop eCLM/CLM5 case at your target site or domain, already
  building and running on `master` or an earlier branch. This tutorial
  extends that case; it does not build one from scratch.
- Build toolchain: GCC 13 / gfortran, OpenMPI (`mpicc`/`mpifort`),
  netCDF-C/Fortran, PnetCDF, LAPACK. If any of `gfortran`, `mpifort`,
  `nc-config`, `nf-config`, `pnetcdf-config` are missing, install via your
  system's package manager before proceeding.
- The reference parameter file in [`params/`](params/) alongside this
  document, or your own parameter file built on the same PFT ordering (see
  §3 below for why the ordering matters and how to check it).

## 1. Build

This branch adds public module entities (new namelist variables in
`clm_varctl.F90`, extended arrays in `pftconMod.F90`). A build directory left
over from an earlier branch will use stale `.mod` files and fail or silently
misbehave — always rebuild from a clean build directory when switching onto
this branch for the first time:

```bash
git checkout eCLM_FYM_fixes
git log --oneline -3          # sanity check you're where you think you are

rm -rf <build_dir>/*
# re-run your normal cmake configure step, then:
cmake --build <build_dir> --parallel 8
cmake --install <build_dir> --prefix <install_prefix>
```

## 2. Part A — backward-compatible run

Before touching any of this branch's new functionality, confirm the build
itself is sound by running your existing single-crop case unchanged. This
isolates build/toolchain problems from feature-specific ones later.

```fortran
&clm_inparm
  use_covercropping = .false.
  use_fruittree      = .false.
  use_cfert          = .false.
  paramfile          = '<your existing legacy parameter file>.nc'
/
```

Both flags default to `.false.`, so an existing `lnd_in` that never mentions
them is already in this state — you can run it as-is. Two things to expect
that are specific to this branch, not failures:

- **`CropType.F90` restart fallback.** This branch restarts 12 crop state
  variables (`yrop`, `lt50`, `wdd`, and others) that earlier code left
  un-restarted. If you're initializing from a restart file written before
  this branch existed, those fields are absent and the run falls back to
  planting-time defaults — logged once per masterproc, not an error. Confirm
  it appears once, not repeatedly:
  ```bash
  grep -iE 'fallback|yrop|lt50' <case>/logs/*.comp_lnd.log | head
  ```
- **`taper`/`nstem` fallback**, if your parameter file predates this branch's
  optional handling of those fields — same pattern, logged once:
  ```bash
  grep -iE 'taper|nstem' <case>/logs/*.comp_lnd.log | head
  ```

If this run reproduces your pre-branch results (bit-for-bit, or within
expected tolerance if your case has an inherent source of run-to-run
variation), the build is sound and any issue you hit later is
feature-specific, not a build problem.

## 3. Part B1 — crop rotation

### Prepare the rotation file

Use [`tools/make_rotation_landuse.py`](tools/make_rotation_landuse.py) in
this directory. First, find the exact crop names in the parameter file your
case will use — **read them from the file itself, never assume a fixed
index table**. PFT/CFT index-to-name mappings are not guaranteed stable
across parameter files, and hardcoded indices have caused real, silent bugs
in this branch's own history:

```bash
python3 tools/make_rotation_landuse.py --paramfile <params>.nc --list-crops
```

Edit the `ROTATION` and `DOMAIN` blocks at the top of the script using the
exact names printed above, then build:

```bash
python3 tools/make_rotation_landuse.py --paramfile <params>.nc -o <rotation>.nc
```

Convention to keep straight while editing `ROTATION`: **year N is the crop
harvested in year N.** A winter crop entered for 2015 is sown in autumn
2014, not 2015 — the entry still goes under `2015` in the list.

### Set the namelist flags

```fortran
&clm_inparm
  use_fruittree          = .true.
  use_covercropping      = .true.
  paramfile               = '<params>.nc'
  covercrop_paramfile     = '<params>.nc'
  transient_landuse_file  = '<rotation>.nc'
/
```

`paramfile` and `covercrop_paramfile` **must point to the same file** — the
cover-crop flag array and the `covercrop_1`/`covercrop_2` entries are read
from `covercrop_paramfile` specifically, and a mismatch here silently reads
crop parameters and cover-crop flags from two different sources. Both flags
default to `.false.`, so an existing case is unaffected until you set them.

### Request diagnostics

Add to `hist_fincl1`:

```
IVT, CPHASE, GDDPLANT, GRAINC
```

`IVT` is the rotation itself (active crop PFT index) and is only registered
when `use_covercropping = .true.` — requesting it otherwise aborts the run
at initialization.

### Run

Submission is otherwise unchanged. Two requirements specific to a rotation
run:

- Atmospheric forcing must cover the full rotation period — cyclic forcing
  is not supported.
- The transient land-use file must span the simulated years.

The first simulated year inherits its crop from the restart file, not from
the rotation logic — treat it as spin-up when checking results.

### Verify

Switching events are written to the land component log:

```bash
grep CCROT <case>/*.comp_lnd.log
```

Expect one switching event per crop transition in the prescribed sequence; a
much larger count indicates a configuration problem (often a rotation file
that doesn't span the run, or a mismatched `paramfile`/`covercrop_paramfile`
pair). Cross-check the simulated sequence against what you prescribed:

```bash
ncdump -v IVT <case>.clm2.h0.*.nc
```

## 4. Part B2 — organic fertiliser (FYM) carbon

In the default model, manure nitrogen enters the mineral nitrogen pool
directly with no associated carbon — farmyard manure has no effect on soil
organic carbon. This branch routes it as both a carbon and a nitrogen input.

### Namelist

```fortran
&clm_inparm
  use_cfert              = .true.
/
&cfert_inparm
  manure_CN_ratio        = 25.0
  manure_fmet            = 0.60
  manure_fcel            = 0.30
  manure_flig            = 0.10
  manure_injection_depth = 0.0
  manure_freq_years      = 1
  manure_nh4_frac        = 0.25
  manure_apply_month     = 0
  manure_apply_day       = 1
  cn_balance_tol_c       = 1.0e-7
  cn_balance_tol_n       = 1.0e-7
/
```

Values above are the defaults; `cfert_inparm` is optional — omit it entirely
and these are used. `use_cfert` defaults to `.false.`, so an existing case is
unaffected until set.

**What `manunitro` means now.** The per-crop-PFT rate in the parameter file
is *total* manure nitrogen. Only `(1 - manure_nh4_frac)` of it is immediately
mineral; the rest enters the litter pools as organic nitrogen alongside
carbon at `manure_CN_ratio`:

```
manureC   = (1 - manure_nh4_frac) * manunitro * 1000 * manure_CN_ratio
mineral N = manunitro * 1000 * manure_nh4_frac
organic N = manunitro * 1000 * (1 - manure_nh4_frac)
```

`manure_nh4_frac ≈ 0.25` for solid FYM, `≈ 0.55` for slurry.

**The calibration tradeoff.** At a fixed `manure_CN_ratio`, `manunitro` can
reproduce a target carbon input or a target total-nitrogen input, but not
both independently — moving one moves the other. If your target carbon input
(from a soil-carbon comparison) implies an unrealistic total nitrogen rate,
`manure_CN_ratio` is the correct lever, not `manunitro`:

```
manure_CN_ratio = C_org_target / (N_tot * (1 - manure_nh4_frac))
```

Worked example: 20 t/ha solid FYM applied, target carbon input 108 gC/m²/yr,
`manure_nh4_frac = 0.25`. Solving forward at `manure_CN_ratio = 25`:
`manunitro = 108 / 25 / 0.75 / 1000 = 0.00576` → total N = 57.6 kgN/ha,
mineral N = 14.4 kgN/ha, organic N = 43.2 kgN/ha. Sanity-check the resulting
total N against an independent estimate for your site (typical FYM carries
roughly 5 kgN per tonne fresh mass) before committing to a value.

**Timing.** The full amount applies within a single timestep.
`manure_apply_month = 0` applies at the onset of crop growth (gated by the
same `manure_freq_years` interval as ammoniacal N); a non-zero month/day
applies on that fixed calendar date instead, independent of onset timing.
`manure_freq_years` sets the application interval for biennial or less
frequent amendment.

**Vertical placement.** `manure_injection_depth = 0.0` puts carbon in the
surface layer only (surface spreading). A positive depth distributes it over
soil layers down to that depth (incorporation).

**Balance checks are live**, not effectively disabled — tolerances default
to `1e-7`, not the historical `100`. A run that used to complete under the
old, effectively-disabled tolerance may now abort. If it aborts specifically
on a manure application date, the correct fix is spreading the pulse over
the crop's `ndays_on` window rather than widening `cn_balance_tol_c`/`_n` —
widening the tolerance defeats the purpose of tightening it in the first
place.

### Diagnostics

`Corg_FERT` (gC m⁻² s⁻¹) and `Norg_FERT` reports the applied organic
carbon/nitrogen flux and are registered when `use_cfert` is set. Add them to
`hist_fincl1` and confirm one spike per application year, at the expected
date and magnitude:

```bash
grep -i 'balance' <case>/logs/*.comp_lnd.log | head
```

## 5. Running both together

Rotation and organic fertiliser are independent flags and combine directly —
set both blocks above in the same `lnd_in`. This is the realistic
configuration for a real farm management sequence: a prescribed crop
rotation with periodic FYM application, rather than either in isolation.
There is no separate "combined" namelist group to configure.

## 6. Reverting to a single-crop configuration

Set `use_covercropping = .false.` and `use_fruittree = .false.` and supply
the legacy parameter file. No other change is required — the rotation code
paths are not entered, matching Part A above.

## 7. Verification checklist

Beyond the feature-specific checks above, before trusting results from a new case on this branch:

use_grainproduct is actually active on every rank. This branch fixed a dropped MPI broadcast that previously left it .false. on every rank but 0. If you're comparing against results generated before this fix, expect a real difference: harvested grain carbon now leaves the litter pool instead of returning to it on every rank, not just rank 0.
PFT/CFT indices, if you or a script hardcode any crop-PFT index rather than resolving it from pftname (as make_rotation_landuse.py does) — check it against the actual parameter file in use. This has been the single most common source of silent, wrong-answer bugs in this branch

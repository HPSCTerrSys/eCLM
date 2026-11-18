# eCLM Cover-Cropping Implementation — Source Code Changes

**Branch:** `eCLM_FYM` on fork `tboas/eCLM`  
**Base:** HPSCTerrSys/clm5_0  
**Author:** T. Boas  
**Date:** July 2026  

---

## Overview

This document describes all source code changes introduced to implement
optional, file-driven cover-crop rotation in eCLM (CLM5). The implementation
is fully backward compatible: with `use_covercropping = .false.` (default),
the model behaves identically to the unmodified CLM5.

---

## Design Goals

1. **Backward compatibility** — old parameter files (79 PFTs) and old namelists
   work unchanged when `use_covercropping = .false.`
2. **File-driven rotation** — crop sequence defined externally via a transient
   land-use file, not hardcoded in the source
3. **Spatial** — works for point cases and regional/global domains identically
4. **Timing** — PFT switch happens immediately after cash crop harvest, within
   the same calendar year, enabling fall planting of winter crops and cover crops
5. **Separate param file** — cover-crop PFT physiology in a dedicated param file,
   keeping the standard param file untouched

---

## New Namelist Parameters

Added to `&clm_inparm` in `lnd_in`:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `use_covercropping` | logical | `.false.` | Enable cover-crop rotation |
| `covercrop_paramfile` | character(256) | `' '` | Param file containing `covercrop_1/2` PFTs and `covercrop` flag array |
| `transient_landuse_file` | character(256) | `' '` | NetCDF file defining `PCT_CFT(time, cft, lndgrid)` crop rotation sequence |

---

## Transient Land-Use File Format

Required when `use_covercropping = .true.`:

```
dimensions:
  time    = N      (number of years in rotation)
  cft     = 64     (number of crop functional types, must match model)
  lndgrid = M      (number of gridcells; 1 for point cases)

variables:
  int  YEAR(time)                    -- calendar year for each time slice
  real PCT_CFT(time, cft, lndgrid)   -- CFT fractions 0-100%
  real PCT_CROP(time, lndgrid)       -- total crop area fraction
```

Each year, one CFT has 100% and all others have 0%.
The CFT index maps to CLM5 PFT index as: `PFT_index = CFT_index + cft_lb`
where `cft_lb = natpft_ub + 1 = 15`.

---

## Files Modified

### 1. `src/clm5/main/clm_varctl.F90`

**What changed:** Added two new public character variables.

```fortran
! Added after: logical, public :: use_covercropping = .false.
character(len=256), public :: transient_landuse_file = ' '
character(len=fname_len), public :: covercrop_paramfile = ' '
```

---

### 2. `src/clm5/main/controlMod.F90`

**What changed:** Added both new variables to the `clm_inparm` namelist and
added MPI broadcasts so all tasks receive the values.

```fortran
! Added to namelist declarations:
namelist /clm_inparm/ covercrop_paramfile
namelist /clm_inparm/ transient_landuse_file

! Added to MPI broadcast section (after use_covercropping broadcast):
call mpi_bcast(covercrop_paramfile,    len(covercrop_paramfile),    MPI_CHARACTER, 0, mpicom, ier)
call mpi_bcast(transient_landuse_file, len(transient_landuse_file), MPI_CHARACTER, 0, mpicom, ier)
```

---

### 3. `src/clm5/main/pftconMod.F90`

**What changed:** Replaced the covercrop flag read block so that:
- With `use_covercropping = .false.`: `covercrop(:) = 0`, nothing read from any file
- With `use_covercropping = .true.`: opens `covercrop_paramfile` separately and reads
  the `covercrop` flag array from there; aborts clearly if file not set

**Before:**
```fortran
!Cover crop flag read-in
if (use_covercropping) then
   call ncd_io('covercrop', this%covercrop, 'read', ncid, readvar=readv)
   if (.not. readv) call endrun(...)
else
   this%covercrop(:) = 0._r8
end if
```

**After:**
```fortran
!Cover crop flag read-in --- tboas
! Default: zero array — backward compatible with standard 79-PFT param file.
this%covercrop(:) = 0._r8
if (use_covercropping) then
   if (trim(covercrop_paramfile) == '' ...) call endrun(clear error message)
   block
     ! Open covercrop_paramfile separately
     call ncd_pio_openfile(ncid_cc, covercrop_paramfile, 0)
     call ncd_io('covercrop', this%covercrop, 'read', ncid_cc, readvar=readv)
     if (.not. readv) call endrun(...)
     call ncd_pio_closefile(ncid_cc)
   end block
end if
```

**Key point:** The standard `paramfile` (79 PFTs) is never touched for covercrop
reads. Only the separate `covercrop_paramfile` (81 PFTs with `covercrop_1/2`) is
opened when the flag is on.

---

### 4. `src/clm5/biogeochem/dynHarvestMod.F90`

**What changed:** 
- Added `use dynCovercropFileMod, only: covercrop_switch_ivt`
- Removed hardcoded cash crop rotation (`nswheat`, `nsugarbeet`,
  `ncovercrop_1/2` logic with fixed DOY thresholds)
- `covercropping_update_patch` now delegates entirely to `covercrop_switch_ivt`
- Moved from phenology path → transient land-use/harvest update path
  (called from `dynSubgridDriverMod` after harvest)

**Before (hardcoded):**
```fortran
cashcrop1 = nswheat
cashcrop2 = nsugarbeet
if (harvdate(p) >= 150 .and. ivt(p) == cashcrop1) then
   ivt(p) = covercrop1
   ...
else if (harvdate(p) <= 170 .and. ivt(p) == covercrop1) then
   ivt(p) = cashcrop2
   ...
! etc — fixed wheat/sugarbeet/covercrop sequence
```

**After (file-driven):**
```fortran
! Only act on patches flagged as cover-crop rotation members
if (covercrop(ivt(p)) /= 1) return
! Only switch after harvest has occurred this season
if (harvdate(p) <= 0) return
! Delegate to file-driven rotation in dynCovercropFileMod
call covercrop_switch_ivt(p, crop_inst, cnveg_state_inst)
```

---

### 5. `src/clm5/dyn_subgrid/dynSubgridDriverMod.F90`

**What changed:** Added init and interp calls for the new `dynCovercropFileMod`.

```fortran
! Added use statement:
use dynCovercropFileMod, only: dyncovercrop_init, dyncovercrop_interp

! In dynSubgrid_init, after dynHarvest_init:
if (use_covercropping) call dyncovercrop_init(bounds_proc)

! In dynSubgrid_driver, after dyncrop_interp:
if (use_covercropping) call dyncovercrop_interp(bounds_proc)
```

---

### 6. `src/clm5/dyn_subgrid/dynCovercropFileMod.F90` *(NEW FILE)*

New module implementing the file-driven rotation. Three public subroutines:

#### `dyncovercrop_init(bounds)`
- Called once at startup from `dynSubgridDriverMod`
- Opens `transient_landuse_file`
- Validates `cft` dimension matches model
- Allocates `pct_cft_cur(begg:endg, cft_size)` and `pct_cft_next(begg:endg, cft_size)`
- Calls `dyncovercrop_interp` to load first two time slices
- Aborts clearly if `transient_landuse_file` not set

#### `dyncovercrop_interp(bounds)`
- Called every timestep from `dynSubgridDriverMod`
- Updates `pct_cft_cur` and `pct_cft_next` for current model year
- Uses `dyn_var_time_uninterp_type` (same infrastructure as `dyncropFileMod`)
- `pct_cft_next` holds the NEXT year's crop fractions — used for post-harvest
  planting decisions (winter crops planted in fall of current year)

#### `covercrop_switch_ivt(p, crop_inst, cnveg_state_inst)`
- Called per-patch from `covercropping_update_patch` after harvest
- Finds dominant CFT in `pct_cft_next` for this gridcell `g = patch%gridcell(p)`
- Converts CFT index to global PFT index: `new_ivt = cft_lb + best_cft - 1`
- Only switches if new PFT differs from current
- Resets `croplive`, `cropplant`, `idop` so new PFT starts fresh
- Sets `use_grainproduct = .false.` for cover crops, `.true.` for cash crops

---

### 7. `src/clm5/CMakeLists.txt`

Added new module to build system:

```cmake
dyn_subgrid/dynCovercropFileMod.F90
```

---

## Cover-Crop Param File

The `covercrop_paramfile` must contain:
- `pft` dimension = 81 (79 standard + covercrop_1 + covercrop_2)
- `pftname` array with `covercrop_1` at index 77, `covercrop_2` at index 78
- `covercrop(pft)` integer flag array: `1` for all PFTs that participate in
  rotation (cash crops + cover crops), `0` for all others
- Full physiology for covercrop_1 and covercrop_2 PFTs

File used for DE-RuS Selhausen:
```
/p/project1/cjicg41/jicg4180/clm5_params.c171117_boas_cc34_on_mod5_hybgdd950_apple_perennial_0.nc
```

---

## Backward Compatibility Matrix

| Scenario | Behaviour |
|---|---|
| `use_covercropping = .false.` (default) | Identical to unmodified CLM5. No files read, `covercrop(:)=0`, rotation logic skipped entirely |
| Old 79-PFT param file + flag off | Works unchanged |
| `use_covercropping = .true.`, no `covercrop_paramfile` | Clean `endrun` with message pointing to missing namelist key |
| `use_covercropping = .true.`, no `transient_landuse_file` | Clean `endrun` with message pointing to missing namelist key |
| `use_covercropping = .true.`, both files set | Full file-driven rotation active |

---


# Soil Hydraulic Parameters #

This section describes **setting Soil Hydraulic Parameters from the
surface file**.

The implementation was first introduced by Fernand Eloundou and
adapted by Yorck Ewerdwalbesloh.

## Soil Parameter Perturbation (`SoilStateInitTimeConstMod.F90`) ##

Allows reading perturbed hydraulic parameters from input files instead
of computing them via pedotransfer functions.

**Parameters:**
- `THETAS` - saturated water content
- `SHAPE_PARAM` - Brooks-Corey shape parameter (`bsw`)
- `PSIS_SAT` - saturated matric potential (`sucsat`)
- `KSAT` - saturated hydraulic conductivity (`xksat`)

**Implementation:**
- Hydraulic parameters read from surface file
- Reads EITHER original parameters (for `nlevsoifl=10` soil layers)
  and applies organic matter mixing OR: Reads adjusted parameters with
  `_adj` suffix (for all `nlevgrnd` layers) and **overwrites**
  parameters from organic matter mixing.
- Falls back to pedotransfer functions if parameters aren't in the file
- Modifies organic matter mixing to preserve perturbed parameter
  values

### Surface File

Soil hydraulic parameters are read from the **surface dataset file**,
which is specified in the `lnd_in` namelist file under key `fsurdat`.

#### Sufrace File: Parameter Structure and Dimensions

All soil hydraulic parameters are stored as three-dimensional arrays
with the structure:

```
  (nlevgrnd, lsmlat, lsmlon)
```

Where:
- `nlevgrnd`: Number of soil layers (vertical dimension, typically 25
  layers in eCLM simulations, see namelist file key
  `soil_layerstruct`)
- `lsmlat`: Number of latitude grid points
- `lsmlon`: Number of longitude grid points

This 3D structure enables depth-varying, spatially-distributed soil
properties across the model domain.

#### Surface File: Input Parameter Format

Two options
- parameters that undergo organic mixing
- adjusted parameters that are used by input values

##### Parameters before organic mixing

The surface file must contain the following baseline parameters:

``` text
  THETAS(nlevgrnd, lsmlat, lsmlon)
      long_name: "Porosity"
      units: "vol/vol"

  SHAPE_PARAM(nlevgrnd, lsmlat, lsmlon)
      long_name: "Shape (b) parameter"
      units: "unitless"

  PSIS_SAT(nlevgrnd, lsmlat, lsmlon)
      long_name: "Saturated soil matric potential"
      units: "mmH2O"

  KSAT(nlevgrnd, lsmlat, lsmlon)
      long_name: "Saturated hydraulic conductivity"
      units: "mm/s"
```

These parameters apply to the first 10 soil layers (`nlevsoifl=10`) and
undergo organic matter mixing.

##### Adjusted Parameters after organic mixing

For using adjusted soil parameters from file that represent the whole
soil including organic matter, the surface file should contain
adjusted parameters with the `_adj` suffix:

``` text
  THETAS_adj(nlevgrnd, lsmlat, lsmlon)
      long_name: "Porosity"
      units: "vol/vol"
      _FillValue: 1.e+30

  SHAPE_PARAM_adj(nlevgrnd, lsmlat, lsmlon)
      long_name: "Shape (b) parameter"
      units: "unitless"
      _FillValue: 1.e+30

  PSIS_SAT_adj(nlevgrnd, lsmlat, lsmlon)
      long_name: "Saturated soil matric potential"
      units: "mmH2O"
      _FillValue: 1000.0

  KSAT_adj(nlevgrnd, lsmlat, lsmlon)
      long_name: "Saturated hydraulic conductivity"
      units: "mm/s"
      _FillValue: 1.e+30
```

**Important Notes:**
- Adjusted parameters apply to **all** `nlevgrnd` layers
- When present, adjusted parameters **overwrite** the results of organic
  matter mixing
- `PSIS_SAT_adj` uses a different fill value (1000.0) compared to other
  parameters (1.e+30), reflecting special handling for undefined matric
  potential values
- If adjusted parameters are not present in the surface file, eCLM falls
  back to the original parameters or pedotransfer functions

### Namelist Configuration

The soil hydraulic parameter reading behavior is controlled by two
namelist settings in the `clm_soilstate_inparm` section of the `lnd_in`
namelist file:

#### `soil_hyd_inparm_from_file`

**Type:** logical
**Default:** `.false.`
**Description:** Controls whether to read baseline hydraulic parameters
from the surface dataset file.

When set to `.true.`:
- eCLM reads `THETAS`, `SHAPE_PARAM`, `PSIS_SAT`, and `KSAT` from the
  surface file
- Parameters apply to the first 10 soil layers (`nlevsoifl=10`)
- Parameters undergo organic matter mixing
- If any required variable is missing, the model aborts with an error
  message

When set to `.false.` (default):
- Hydraulic parameters are computed via pedotransfer functions from
  sand and clay fractions
- No parameters are read from the surface file

#### `soil_hyd_inparm_from_file_adj`

**Type:** logical
**Default:** `.false.`
**Description:** Controls whether to read organic-matter-adjusted
hydraulic parameters from the surface dataset file.

When set to `.true.`:
- eCLM reads `THETAS_adj`, `SHAPE_PARAM_adj`, `PSIS_SAT_adj`, and
  `KSAT_adj` from the surface file
- Parameters apply to **all** `nlevgrnd` soil layers (typically 25
  layers)
- Adjusted parameters **overwrite** the results from organic matter
  mixing
- If any required variable is missing, the model aborts with an error
  message

When set to `.false.` (default):
- No organic-matter-adjusted parameters are read from the surface file
- Organic matter mixing results are used as final parameter values

#### Example Configuration

```fortran
&clm_soilstate_inparm
  organic_frac_squared = .false.
  soil_hyd_inparm_from_file = .false.
  soil_hyd_inparm_from_file_adj = .true.
/
```

This configuration:
- Reads adjusted parameters from the surface file which override the
  organic matter mixing results
- Can e.g. be used for ensemble data assimilation applications with
  perturbed soil parameters specified in a group of surface files, one
  surface file per ensemble member.

#### Error Handling

Both namelist parameters enforce strict error checking:
- If set to `.true.`, **all** required parameters must be present in
  the surface file
- Missing variables trigger an immediate model abort with a descriptive
  error message
- This ensures users are explicitly aware when parameter files are
  incomplete

### Note about the Brooks-Corey Shape Parameter ###

When perturbed soil parameters are read from input files, the organic
matter mixing for `bsw` uses the file-read value instead of the
hard-coded Cosby et al. (1984) Table 5 formula (`2.91 + 0.159*clay`).

## Modified Source Code ##

- `src/clm5/biogeophys/SoilStateInitTimeConstMod.F90`

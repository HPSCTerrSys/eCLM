# Perturbation routines #

This section describes **perturbation capabilities for eCLM-PDAF**.

The implementation of the Soil Hydraulic Parameter perturbation was
first introduced by Fernand Eloundou and adapted by Yorck
Ewerdwalbesloh.

The implementation of the atmospheric forcing perturbation routines
was first introduced by Yorck Ewerdwalbesloh.

## Description

eCLM implements perturbations for atmospheric forcing variables
(temperature, precipitation, longwave radiation, and shortwave
radiation) to support ensemble-based data assimilation in
eCLM-PDAF. The perturbation scheme maintains physical consistency
through cross-variable correlations and spatiotemporal coherence.

### Physical Consistency

Perturbed variables are cross-correlated to preserve physical
relationships between forcing fields. For example, a positive
perturbation of incoming shortwave radiation corresponds to a negative
perturbation of longwave radiation and a positive perturbation of
temperature. The cross-correlation structure follows Reichle et
al. (2007) and Han et al. (2014).

### Spatial Correlation

Perturbations are spatially correlated using an isotropic correlation
function based on grid cell separation distance. Precipitation uses a
shorter correlation length scale than other variables to reflect its
more localized spatial structure. Correlation parameters are
configurable.

### Temporal Correlation

Temporal correlation is generated using a first-order autoregressive
(AR-1) model following Evensen (2009). The default temporal
persistence corresponds to a decorrelation timescale of one day, which
is adjustable based on application requirements.

### Implementation

Perturbation fields are read from preprocessed noise files and applied
to atmospheric forcing variables within the eCLM model during runtime.

## Key Components ##

### 1. Soil Parameter Perturbation (`SoilStateInitTimeConstMod.F90`) ###

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

#### Surface File

Soil hydraulic parameters are read from the **surface dataset file**,
which is specified in the `lnd_in` namelist file under key `fsurdat`.

##### Sufrace File: Parameter Structure and Dimensions

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

##### Surface File: Input Parameter Format

Two options
- original parameters that undergo organic mixing
- adjusted parameters that are used by input values

###### Original Parameters

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

###### Adjusted Parameters for Data Assimilation

When running with perturbed soil parameters (e.g., from ensemble data
assimilation), the surface file should contain adjusted parameters
with the `_adj` suffix:

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

#### Namelist Configuration

The soil hydraulic parameter reading behavior is controlled by two
namelist settings in the `clm_soilstate_inparm` section of the `lnd_in`
namelist file:

##### `soil_hyd_inparm_from_surfdata`

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

##### `soil_hyd_inparm_from_surfdata_adj`

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

##### Example Configuration

```fortran
&clm_soilstate_inparm
  organic_frac_squared = .false.
  soil_hyd_inparm_from_surfdata = .false.
  soil_hyd_inparm_from_surfdata_adj = .true.
/
```

This configuration:
- Reads adjusted parameters from the surface file which override the
  organic matter mixing results
- Is typical for ensemble data assimilation applications with perturbed
  soil parameters

##### Error Handling

Both namelist parameters enforce strict error checking:
- If set to `.true.`, **all** required parameters must be present in
  the surface file
- Missing variables trigger an immediate model abort with a descriptive
  error message
- This ensures users are explicitly aware when parameter files are
  incomplete

#### Note about the Brooks-Corey Shape Parameter ####

When perturbed soil parameters are read from input files, the organic
matter mixing for `bsw` uses the file-read value instead of the
hard-coded Cosby et al. (1984) Table 5 formula (`2.91 + 0.159*clay`).

### 2. Noise-Based Forcing Perturbation ###

When having an ensemble run, the memory consumption is too large if
the forcing data is perturbed one by one so that I get a file for each
month for each member idea: perturb the forcings in the CLM sourcecode
with a noise file.  for each perturbed variable (temperature,
precipitation, longwave and shortwave radiation), a stream is
introduced.

Adds spatiotemporal noise to atmospheric forcing data for ensemble
data assimilation.

**Modified files:**
- `shr_stream_mod.F90`
- `shr_strdata_mod.F90`
- `shr_dmodel_mod.F90`

**Key Features:**
- Stores ensemble metadata in stream structure:
  - `caseId` - ensemble member ID
  - `dt` - forcing time resolution
  - `numEns` - ensemble size that the perturbation file was created
    for. Example: Running with 50 ensemble members with a noise file
    created for an ensemble of up to 200 members. Then, `numEns`
    should be set to 200 in the stream file for right usage of
    perturbation dimension.
- **Time-shifting mechanism**: Different ensemble members read different temporal frames from the same noise file
  - Formula: `frame = nt + caseId * 24/dt`
  - Example: For 3-hourly data (`dt=3`), member 0 starts at frame
    `nt`, member 1 at `nt+8`, member 2 at `nt+16`, etc.
- Detects noise fields by checking if model field name contains `"noise"`
- Adjusts time coordinate reading to account for ensemble-extended noise files

#### Preparing Atmospheric Forcing Noise ####

This section describes the workflow for generating and configuring
spatiotemporally correlated noise fields for atmospheric forcing
perturbations.

##### Noise Generation Tool #####

The `correlatedNoise.py`
(https://github.com/HPSCTerrSys/eCLM_atm-forcing-generator/pull/8)
script generates monthly NetCDF files containing spatiotemporally
correlated noise fields for all ensemble members.

**Key Configuration Parameters:**

- **Ensemble size**: Number of ensemble members to generate noise for (must be specified)
- **Temporal resolution** (`dt`): Time step in hours (e.g., `3` for 3-hourly data, `1` for hourly data)
- **Spatial resolution** (`ds`): Grid spacing in km (e.g., `12.5` for 12.5 km grid, `3` for 3 km grid)
- **Spatial sampling** (`nn`): Number of points used for noise generation before upscaling (limited by computational resources)
- **Temporal persistence** (`rho`): AR-1 correlation coefficient (adjust based on forcing time resolution)
- **Covariance matrix**: Cross-variable covariance structure and correlation coefficients (configurable)
- **File paths**: Input/output directories (must be adjusted for local system)

**Output**: One NetCDF file per month containing noise fields for all ensemble members and all perturbed variables.

##### Stream File Configuration #####

Stream files configure how eCLM reads and applies noise fields to
atmospheric forcing data. Three separate stream files are required
(precipitation, solar radiation, and other variables). Each stream
file must specify the following metadata fields:

**Required Metadata:**

- `timeInformation`: Temporal resolution of forcing data in hours (e.g., `3` for 3-hourly data)
- `caseId`: Ensemble member index (e.g., `0` for first member, `1` for second member)
- `numEns`: Total ensemble size used when generating the noise files
- **Perturbation variables**: `tbot_noise` (temperature), `lwdn_noise` (longwave radiation), `precn_noise` (precipitation), `swdn_noise` (shortwave radiation)


##### Stream File Examples #####

The following examples demonstrate proper stream file configuration
for precipitation, solar radiation, and other atmospheric
variables. Each example must be adapted with correct file paths,
temporal parameters, and ensemble member IDs for your specific
application.

###### Precipitation Noise Stream File ######

**File**: `user_datm.streams.precip_noise.stream_0000.txt`

```xml
<dataSource>
   GENERIC
</dataSource>
<domainInfo>
  <variableNames>
     time    time
        xc      lon
        yc      lat
        area    area
        mask    mask
  </variableNames>
  <filePath>
     /path/to/domain/file
  </filePath>
  <fileNames>
     domain.lnd.EUR-11_EUR-11.230216_mask.nc
  </fileNames>
</domainInfo>
<fieldInfo>
   <variableNames>
     PRECTmms precn_noise
   </variableNames>
   <filePath>
     /path/to/noise/files
   </filePath>
   <fileNames>
2003-01.nc
2003-02.nc
2003-03.nc
2003-04.nc
2003-05.nc
2003-06.nc
2003-07.nc
2003-08.nc
2003-09.nc
2003-10.nc
2003-11.nc
2003-12.nc
   </fileNames>
   <offset>
     0 
   </offset>
   <timeInformation>
     3 
   </timeInformation>
   <caseId>
     0 
   </caseId>
   <numEns>
     64 
   </numEns>
</fieldInfo>
```

###### Solar Radiation Noise Stream File ######

**File**: `user_datm.streams.solar_noise.stream_0000.txt`

```xml
<dataSource>
   GENERIC
</dataSource>
<domainInfo>
  <variableNames>
     time    time
        xc      lon
        yc      lat
        area    area
        mask    mask
  </variableNames>
  <filePath>
     /path/to/domain/file
  </filePath>
  <fileNames>
     domain.lnd.EUR-11_EUR-11.230216_mask.nc
  </fileNames>
</domainInfo>
<fieldInfo>
   <variableNames>
     FSDS swdn_noise
   </variableNames>
   <filePath>
     /path/to/noise/files
   </filePath>
   <fileNames>
2003-01.nc
2003-02.nc
2003-03.nc
2003-04.nc
2003-05.nc
2003-06.nc
2003-07.nc
2003-08.nc
2003-09.nc
2003-10.nc
2003-11.nc
2003-12.nc
   </fileNames>
   <offset>
     0 
   </offset>
   <timeInformation>
     3 
   </timeInformation>
   <caseId>
     0 
   </caseId>
   <numEns>
     64 
   </numEns>
</fieldInfo>
```

###### Temperature and Longwave Radiation Noise Stream File ######

**File**: `user_datm.streams.other_noise.stream_0000.txt`

```xml
<dataSource>
   GENERIC
</dataSource>
<domainInfo>
  <variableNames>
     time    time
        xc      lon
        yc      lat
        area    area
        mask    mask
  </variableNames>
  <filePath>
     /path/to/domain/file
  </filePath>
  <fileNames>
     domain.lnd.EUR-11_EUR-11.230216_mask.nc
  </fileNames>
</domainInfo>
<fieldInfo>
   <variableNames>
        TBOT     tbot_noise
        FLDS     lwdn_noise
   </variableNames>
   <filePath>
     /path/to/noise/files
   </filePath>
   <fileNames>
2003-01.nc
2003-02.nc
2003-03.nc
2003-04.nc
2003-05.nc
2003-06.nc
2003-07.nc
2003-08.nc
2003-09.nc
2003-10.nc
2003-11.nc
2003-12.nc
   </fileNames>
   <offset>
     0 
   </offset>
   <timeInformation>
     3 
   </timeInformation>
   <caseId>
     0 
   </caseId>
   <numEns>
     64 
   </numEns>
</fieldInfo>

```

### 3. DATM Integration (`datm_comp_mod.F90`) ###

Passes ensemble information (`inst_index`, `dt_option`, `ninst`) from
the data atmosphere (DATM) component to the stream infrastructure,
enabling the noise perturbation mechanism to operate correctly within
CESM's multi-instance framework.

## Design Rationale ##

1. **Dual perturbation approach**:
   - Parameter perturbation for soil properties (offline preprocessing)
   - Forcing perturbation via temporal noise patterns (runtime)

2. **Backward compatibility**: All changes are guarded by `USE_PDAF`
   preprocessor directives

3. **Efficiency**: Uses a single noise file for all ensemble members
   by time-shifting, avoiding storage duplication

4. **Flexibility**: Soil parameters can be perturbed or computed
   traditionally based on file contents

## Modified Source Code ##

- `src/clm5/biogeophys/SoilStateInitTimeConstMod.F90`
- `src/csm_share/streams/shr_stream_mod.F90`
- `src/csm_share/streams/shr_strdata_mod.F90`
- `src/csm_share/streams/shr_dmodel_mod.F90`
- `src/datm/datm_comp_mod.F90`


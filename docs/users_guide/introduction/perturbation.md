## Perturbation routines

This section describes **perturbation capabilities for eCLM-PDAF**.

The implementation of the perturbation routines was first introduced
by Yorck Ewerdwalbesloh in
https://gitlab.jsc.fz-juelich.de/detect/cluster-c/c01/perturbationroutineclm5.

### Key Components

#### 1. Soil Parameter Perturbation (`SoilStateInitTimeConstMod.F90`)

Allows reading perturbed hydraulic parameters from input files instead of computing them via pedotransfer functions.

**Parameters:**
- `THETAS` - saturated water content
- `SHAPE_PARAM` - Brooks-Corey shape parameter (`bsw`)
- `PSIS_SAT` - saturated matric potential (`sucsat`)
- `KSAT` - saturated hydraulic conductivity (`xksat`)

**Implementation:**
- Reads both original parameters (for `nlevsoifl=10` soil layers) and adjusted parameters with `_adj` suffix (for all `nlevgrnd` layers)
- Falls back to pedotransfer functions if parameters aren't in the file
- Modifies organic matter mixing to preserve perturbed parameter values

#### 2. Noise-Based Forcing Perturbation

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
  - `numEns` - total ensemble size
- **Time-shifting mechanism**: Different ensemble members read different temporal frames from the same noise file
  - Formula: `frame = nt + caseId * 24/dt`
  - Example: For 3-hourly data (`dt=3`), member 0 starts at frame `nt`, member 1 at `nt+8`, member 2 at `nt+16`, etc.
- Detects noise fields by checking if model field name contains `"noise"`
- Adjusts time coordinate reading to account for ensemble-extended noise files

#### 3. DATM Integration (`datm_comp_mod.F90`)

Passes ensemble information (`inst_index`, `dt_option`, `ninst`) from
the data atmosphere (DATM) component to the stream infrastructure,
enabling the noise perturbation mechanism to operate correctly within
CESM's multi-instance framework.

### Design Rationale

1. **Dual perturbation approach**:
   - Parameter perturbation for soil properties (offline preprocessing)
   - Forcing perturbation via temporal noise patterns (runtime)

2. **Backward compatibility**: All changes are guarded by `USE_PDAF` preprocessor directives

3. **Efficiency**: Uses a single noise file for all ensemble members by time-shifting, avoiding storage duplication

4. **Flexibility**: Soil parameters can be perturbed or computed traditionally based on file contents

### Modified Files

- `src/clm5/biogeophys/SoilStateInitTimeConstMod.F90` - 121 additions
- `src/csm_share/streams/shr_stream_mod.F90` - 211 additions
- `src/csm_share/streams/shr_strdata_mod.F90` - 72 additions
- `src/csm_share/streams/shr_dmodel_mod.F90` - 40 additions
- `src/datm/datm_comp_mod.F90` - 62 additions
- `README.md` - documentation



# Create atmospheric forcing files

There exist a few global standard forcing data sets that can be downloaded together with their domain file from the official data repository via this <a href="https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/" target="_blank">link</a>. For beginners, it is easiest to start with these existing data files.

- <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/users_guide/setting-up-and-running-a-case/customizing-the-datm-namelist.html#clmgswp3v1-mode-and-it-s-datm-settings" target="_blank">GSWP3 NCEP forcing dataset</a> 
- <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/users_guide/setting-up-and-running-a-case/customizing-the-datm-namelist.html#clmcruncepv7-mode-and-it-s-datm-settings" target="_blank">CRUNCEP dataset</a> 
- <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/users_guide/setting-up-and-running-a-case/customizing-the-datm-namelist.html#clm-qian-mode-and-it-s-datm-settings" target="_blank">Qian dataset</a>


To run with your own atmospheric forcing data, you need to set them up in NetCDF format that can be read by the atmospheric data model `DATM`. 

There is a list of eight variables that are expected to be on the input files. The names and units can be found in the table below (in the table TDEW and SHUM are optional fields that can be used in place of RH). The table also lists which of the fields are required and if not required what the code will do to replace them. If the names of the fields are different or the list is changed from the standard list of eight fields: FLDS, FSDS, PRECTmms, PSRF, RH, TBOT, WIND, and ZBOT, the resulting streams file will need to be modified to take this into account. 

```{list-table} Atmospheric forcing fields adapted from <a href="https://www2.cesm.ucar.edu/models/cesm1.2/clm/models/lnd/clm/doc/UsersGuide/x12979.html" target="_blank">CESM1.2.0 User's Guide Documentation</a>.
:header-rows: 1
:name: tab1

* - Short-name
  - Description
  - Unit
  - Required?
  - If NOT required how replaced
* - FLDS
  - incident longwave
  - W/m2
  - No
  - calculates based on Temperature, Pressure and Humidity (NOTE: The CRUNCEP data includes LW down, but by default we do NOT use it -- we use the calculated values)
* - FSDS
  - incident solar
  - W/m2
  - Yes
  - /
* - FSDSdif
  - incident solar diffuse
  - W/m2
  - No
  - based on FSDS
* - FSDSdir
  - incident solar direct
  - W/m2
  - No
  - based on FSDS
* - PRECTmms
  - precipitation 
  - mm/s
  - Yes
  - /
* - PSRF
  - pressure at the lowest atm level
  - Pa
  - No
  - assumes standard-pressure
* - RH
  - relative humidity at the lowest atm level
  - \%
  - No
  - can be replaced with SHUM or TDEW
* - SHUM
  - specific humidity at the lowest atm level 
  - kg/kg
  - Optional in place of RH
  - can be replaced with RH or TDEW
* - TBOT
  - temperature at the lowest atm level
  - K (or can be C)
  - Yes
  - /
* - TDEW
  - dew point temperature 
  - K (or can be C)
  - Optional in place of RH
  - can be replaced with RH or SHUM
* - WIND
  - wind at the lowest atm level
  - m/s
  - Yes
  - /
* - ZBOT
  - observational height
  - m
  - No
  - assumes 30 meters
```

All of the variables should be dimensioned: time, lat, lon, with time units in the form of "days since yyyy-mm-d hh:mm:ss" and a calendar attribute that can be "noleap" or "gregorian". There should be separate files for each month called `YYYY-MM.nc` where YYYY-MM corresponds to the four digit year and two digit month with a dash in-between.

For single point cases where the atmospheric data has hourly or half-hourly temporal resolution, all data can be in the same monthly files (`YYYY-MM.nc`). For regional cases and if the data is at coarser temporal resolution, different time interpolation algorithms will be used for solar radiation, precipitation and the remaining input data so the data needs to be split into three files and placed into three different folders (`Precip/`, `Solar/`, `TPHWL/`). You also need a domain file to go with your atmospheric data which can be the same as the land domain file created in the previous workflow if the spatial resolution of your atmospheric data is the same as of your specified domain.

For JSC users, an example python script to create forcings for a single-point case based on hourly observations can be found under `/p/scratch/cslts/shared_data/rlmod_eCLM`.

Simply copy the script to your directory and adapt it to your own data.

```sh
cp /p/scratch/cslts/shared_data/rlmod_eCLM/createnetCDF_forc_hourly_input.py $HOME
```
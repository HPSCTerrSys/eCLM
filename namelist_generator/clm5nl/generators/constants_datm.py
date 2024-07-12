PRESAERO_YR_PARAMS = {"SSP": "2015 2015 2101",
                "clim_1850": "1 1850 1850",
                "clim_2000": "1 2000 2000",
                "clim_2010": "1 2010 2010",
          "trans_1850-2000": "1849 1849 2014"}

STREAM_FILE_TEMPLATE = """<?xml version="1.0"?>
<file id="stream" version="1.0">
  <dataSource>
    GENERIC
  </dataSource>
  <domainInfo>
    <variableNames>
      $DOMAIN_VAR_NAMES
    </variableNames>
    <filePath>
      $DOMAIN_FILE_PATH
    </filePath>
    <fileNames>
      $DOMAIN_FILE_NAMES
    </fileNames>
  </domainInfo>
  <fieldInfo>
    <variableNames>
      $FIELD_VAR_NAMES
    </variableNames>
    <filePath>
      $FIELD_FILE_PATH
    </filePath>
    <fileNames>
      $FIELD_FILE_NAMES
    </fileNames>
  <offset>
    0
  </offset>
  </fieldInfo>
</file>
"""

DATM_STREAM_DEFAULTS = {
  "DOMAIN_VAR_NAMES" : ["time    time",
                        "xc      lon",
                        "yc      lat",
                        "area    area",
                        "mask    mask"],
  "FIELD_VAR_NAMES"  : {
    "Solar"          :  "FSDS       swdn",
    "Precip"         :  "PRECTmms   precn",
    "TPQW"           : ["TBOT       tbot",
                        "WIND       wind",
                        "QBOT       shum",
                        "PSRF       pbot"],
    "CLMGSWP3v1.TPQW": ["TBOT       tbot",
                        "WIND       wind",
                        "QBOT       shum",
                        "PSRF       pbot",
                        "FLDS       lwdn"]
    }
}

PRESAERO_STREAM_DEFAULTS = {
  "DOMAIN_VAR_NAMES" : ["time    time",
                        "lon     lon",
                        "lat     lat",
                        "area    area",
                        "mask    mask"],
  "DOMAIN_FILE_PATH" :  "$DIN_LOC_ROOT/atm/cam/chem/trop_mozart_aero/aero",
  "DOMAIN_FILE_NAMES":  "aerosoldep_WACCM.ensmean_monthly_hist_1849-2015_0.9x1.25_CMIP6_c180926.nc",
  "FIELD_VAR_NAMES"  : ["BCDEPWET   bcphiwet",
                        "BCPHODRY   bcphodry",
                        "BCPHIDRY   bcphidry",
                        "OCDEPWET   ocphiwet",
                        "OCPHIDRY   ocphidry",
                        "OCPHODRY   ocphodry",
                        "DSTX01WD   dstwet1",
                        "DSTX01DD   dstdry1",
                        "DSTX02WD   dstwet2",
                        "DSTX02DD   dstdry2",
                        "DSTX03WD   dstwet3",
                        "DSTX03DD   dstdry3",
                        "DSTX04WD   dstwet4",
                        "DSTX04DD   dstdry4"],
  "FIELD_FILE_PATH"  :  "$DIN_LOC_ROOT/atm/cam/chem/trop_mozart_aero/aero",
  "FIELD_FILE_NAMES" :  "aerosoldep_WACCM.ensmean_monthly_hist_1849-2015_0.9x1.25_CMIP6_c180926.nc",
}

TOPO_STREAM_DEFAULTS = {
  "DOMAIN_VAR_NAMES" : ["time    time",
                        "LONGXY  lon",
                        "LATIXY  lat",
                        "area    area",
                        "mask    mask"],
  "DOMAIN_FILE_PATH" :  "$DIN_LOC_ROOT/atm/datm7/topo_forcing",
  "DOMAIN_FILE_NAMES":  "topodata_0.9x1.25_USGS_070110_stream_c151201.nc",
  "FIELD_VAR_NAMES"  :  "TOPO    topo",
  "FIELD_FILE_PATH"  :  "$DIN_LOC_ROOT/atm/datm7/topo_forcing",
  "FIELD_FILE_NAMES" :  "topodata_0.9x1.25_USGS_070110_stream_c151201.nc"
}

# Store indent spaces for multiline
# STREAM_FILE_TEMPLATE variables
INDENTS = {}
for l in STREAM_FILE_TEMPLATE.split("\n"):
    if l.strip().startswith("$"):
        var_name = l.strip()[1:]
        indent_spaces = " " * l.find("$")
        INDENTS[var_name] = indent_spaces

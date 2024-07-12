"""
Work in progress. Plenty of other user options hasn't been covered yet. 
Default datm_in values are based from these files:

[namelist_definition_datm.xml]: https://github.com/ESMCI/cime/blob/cime5.6.33/src/components/data_comps/datm/cime_config/namelist_definition_datm.xml
[config_component.xml]: https://github.com/ESMCI/cime/blob/cime5.6.33/src/components/data_comps/datm/cime_config/config_component.xml
"""
from copy import deepcopy
from pathlib import Path
from string import Template
from ..structures import datm_in
from .constants_datm import *

__all__ = ['build_datm_in']

_in_nl = {}
_in_opts = {}
_nl = datm_in()
_out_dir = ""

def build_datm_in(opts: dict = None, nl: dict = None, nl_file: str = None):
    global _in_opts, _in_nl, _nl, _out_dir

    _in_opts = opts
    _in_nl = nl
    _nl = datm_in()
    _out_dir = Path(nl_file).parent.absolute() if nl_file else Path.cwd()

    # Validate inputs
    if _in_opts["domainfile"] is None:
        error("datm domainfile must be specified.")
    if _in_opts["datm_presaero"] is not None and _in_opts["datm_presaero"] == "none":
        error("datm_presaero = 'none' is not supported.")

    # Build datm_in
    init_shr_strdata_nml()
    init_datm_nml()

    # Write to file
    if nl_file: 
        _nl.write(nl_file, ["datm_nml", "shr_strdata_nml"])
        print(f"Generated {Path(nl_file).name}")

def error(msg):
    raise ValueError(msg)

def init_datm_nml():
    with _nl.datm_nml as n:
        n.factorfn  = _in_nl.get("factorfn" , "null")
        n.decomp    = _in_nl.get("decomp"   , "1d")
        n.iradsw    = _in_nl.get("iradsw"   , 1)
        n.presaero  = _in_nl.get("presaero" , True) #False if datm_presaero="none"
        n.restfilm  = _in_nl.get("restfilm" , "undefined")
        n.restfils  = _in_nl.get("restfils" , "undefined")
        n.wiso_datm = _in_nl.get("wiso_datm", False) #true if datm_mode="CLM_QIAN_WISO"
        n.force_prognostic_true = _in_nl.get("force_prognostic_true", False)

def init_shr_strdata_nml():
    with _nl.shr_strdata_nml as n:
        n.datamode   = "CLMNCEP" 
        n.domainfile = _in_opts["domainfile"] # not optional!
        n.streams    = generate_streams()
        num_streams  = len(n.streams)

        # array params w/ length = # stream files
        n.dtlimit    = [_in_nl.get("dtlimit"  , 1.5)]        * num_streams # see line 3040
        n.fillalgo   = [_in_nl.get("fillalgo" , "nn")]       * num_streams
        n.fillmask   = [_in_nl.get("fillmask" , "nomask")]   * num_streams
        n.fillread   = [_in_nl.get("fillread" , "NOT_SET")]  * num_streams
        n.fillwrite  = [_in_nl.get("fillwrite", "NOT_SET")]  * num_streams
        n.mapalgo    = [_in_nl.get("mapalgo"  , "bilinear")] * num_streams # stream-dependent; see L2884
        n.mapmask    = [_in_nl.get("mapmask"  , "nomask")]   * num_streams
        n.mapread    = [_in_nl.get("mapread"  , "NOT_SET")]  * num_streams
        n.mapwrite   = [_in_nl.get("mapwrite" , "NOT_SET")]  * num_streams
        n.readmode   = [_in_nl.get("readmode" , "single")]   * num_streams
        n.taxmode    = [_in_nl.get("taxmode"  , "cycle")]    * num_streams # stream-dependent; see L2994
        n.tintalgo   = [_in_nl.get("tintalgo" , "nearest")]  * num_streams # stream-dependent; see L2938
        n.vectors    = [_in_nl.get("vectors"  , "null")]     * num_streams # depends on datm_mode; see L3065

def generate_streams():
    datm_mode = _in_opts["datm_mode"]
    datm_presaero = _in_opts["datm_presaero"]

    s_files = {"Solar":    f'datm.streams.txt.{datm_mode}.Solar',
               "Precip":   f'datm.streams.txt.{datm_mode}.Precip', 
               "TPQW":     f'datm.streams.txt.{datm_mode}.TPQW',
               "presaero": f'datm.streams.txt.presaero.{datm_presaero}',
               "topo":     f'datm.streams.txt.topo.observed'}

    yr_params = "{} {} {}".format(_in_opts["stream_year_align"],
                                  _in_opts["stream_year_first"],
                                  _in_opts["stream_year_last"])

    s_nml = [f'{s_files["Solar"]} {yr_params}',
             f'{s_files["Precip"]} {yr_params}',
             f'{s_files["TPQW"]} {yr_params}',
             f'{s_files["presaero"]} {PRESAERO_YR_PARAMS.get(datm_presaero)}',
             f'{s_files["topo"]} 1 1 1']

    create_stream_files(s_files)
    return s_nml

def create_stream_files(stream_files : dict):
    s_template = Template(STREAM_FILE_TEMPLATE)
    s_vars = {}
    
    for s_type, s_file in stream_files.items():
        # Populate stream variables 
        if s_type == "presaero":
            s_vars = deepcopy(PRESAERO_STREAM_DEFAULTS)
        elif s_type == "topo":
            s_vars = deepcopy(TOPO_STREAM_DEFAULTS)
        else:
            s_vars["DOMAIN_FILE_PATH"]  = Path(_in_opts["domainfile"]).parent.absolute()
            s_vars["DOMAIN_FILE_NAMES"] = Path(_in_opts["domainfile"]).name
            s_vars["FIELD_FILE_PATH"]   = _in_opts["domainfile"]
            s_vars["DOMAIN_VAR_NAMES"]  = DATM_STREAM_DEFAULTS["DOMAIN_VAR_NAMES"]
            s_vars["FIELD_VAR_NAMES"]   = DATM_STREAM_DEFAULTS["FIELD_VAR_NAMES"][s_type]
            s_vars["FIELD_FILE_NAMES"]  = _in_opts["stream_files"]

        # Convert list variables into multiline strings with proper indentation
        for key, val in s_vars.items():
            if isinstance(val, list):
                indented_vals = [f'{INDENTS[key]}{v}' for v in val[1:]]
                s_vars[key] = val[0] + "\n"
                s_vars[key] += "\n".join(indented_vals)
        
        # Write stream file to disk
        with open(Path(_out_dir, s_file), "w+") as output:
            output.write(s_template.safe_substitute(s_vars))

        print(f"Generated {s_file}")

if __name__ == "__main__":
    """
    For testing purposes. To run gen_datm_in.py, 
    directly, execute it via Python script mode:
    
    $ cd <parent folder of clm5nl>
    $ python3 -m clm5nl.generators.gen_datm_in   
    """
    opts, nl = {}, {}
    opts["datm_mode"] = "CLMCRUNCEPv7"
    opts["datm_presaero"] = "clim_2000"
    opts["datm_topo"] = "observed"
    opts["stream_year_align"] = "2017"
    opts["stream_year_first"] = "2017"
    opts["stream_year_last"] = "2017"
    opts["stream_root_folder"] = "/p/scratch/nrw_test_case/COSMOREA6/forcings"
    opts["stream_files"] = ["2017-{}.nc".format(str(month).zfill(2)) for month in range(1,13)]
    opts["domainfile"] = "/p/scratch/nrw_test_case/domain.lnd.300x300_NRW_300x300_NRW.190619.nc"
    build_datm_in(opts, nl, "datm_in_test")

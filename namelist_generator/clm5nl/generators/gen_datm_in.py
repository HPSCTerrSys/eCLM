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

_opts = {}
_user_nl = {}
_nl = datm_in()

def build_datm_in(opts: dict = None, nl_file: str = "datm_in"):
    global _opts, _user_nl, _nl

    _opts = opts.get("general_options", {})
    _user_nl = opts.copy()
    _user_nl.pop("general_options", {})
    _nl = datm_in()

    # Validate inputs
    if _user_nl["domainfile"] is None:
        error("datm domainfile must be specified.")
    if _opts["datm_presaero"] is not None and _opts["datm_presaero"] == "none":
        error("datm_presaero = 'none' is not supported.")

    # Build datm_in
    shr_strdata_nml()
    datm_nml()

    # Set user-specified namelist parameters
    _nl.update(_user_nl)

    # Write to file
    if nl_file and Path(nl_file).name.strip() != "": 
        _nl.write(nl_file, ["datm_nml", "shr_strdata_nml"])
        generated_files = [Path(nl_file)]
        if "streams" not in _user_nl:
            # generate default stream files if no streams were specified
            out_dir = Path(nl_file).parent.absolute()
            generated_files.extend(Path(out_dir, s) for s in create_stream_files(out_dir))
        return True, generated_files
    else:
        return True, ""

def error(msg):
    raise ValueError(msg)

def datm_nml():
    with _nl.datm_nml as n:
        n.factorfn  = _user_nl.get("factorfn" , "null")
        n.decomp    = _user_nl.get("decomp"   , "1d")
        n.iradsw    = _user_nl.get("iradsw"   , 1)
        n.presaero  = _user_nl.get("presaero" , True) #False if datm_presaero="none"
        n.restfilm  = _user_nl.get("restfilm" , "undefined")
        n.restfils  = _user_nl.get("restfils" , "undefined")
        n.wiso_datm = _user_nl.get("wiso_datm", False) #true if datm_mode="CLM_QIAN_WISO"
        n.force_prognostic_true = _user_nl.get("force_prognostic_true", False)

def shr_strdata_nml():
    with _nl.shr_strdata_nml as n:
        n.datamode   = "CLMNCEP" 
        n.domainfile = _user_nl["domainfile"] # not optional!
        if "streams" in _user_nl:
            n.streams = _user_nl["streams"]
        else:
            n.streams = generate_streams()
        num_streams  = len(n.streams)

        # array params w/ length = # stream files
        n.dtlimit    = set_array_values("dtlimit"  , 1.5,        num_streams)  # see line 3040
        n.fillalgo   = set_array_values("fillalgo" , "nn",       num_streams)      
        n.fillmask   = set_array_values("fillmask" , "nomask",   num_streams)  
        n.fillread   = set_array_values("fillread" , "NOT_SET",  num_streams)
        n.fillwrite  = set_array_values("fillwrite", "NOT_SET",  num_streams)
        n.mapalgo    = set_array_values("mapalgo"  , "bilinear", num_streams)  # stream-dependent; see L2884
        n.mapmask    = set_array_values("mapmask"  , "nomask",   num_streams)  
        n.mapread    = set_array_values("mapread"  , "NOT_SET",  num_streams) 
        n.mapwrite   = set_array_values("mapwrite" , "NOT_SET",  num_streams) 
        n.readmode   = set_array_values("readmode" , "single",   num_streams)  
        n.taxmode    = set_array_values("taxmode"  , "cycle",    num_streams)  # stream-dependent; see L2994
        n.tintalgo   = set_array_values("tintalgo" , "nearest",  num_streams)  # stream-dependent; see L2938
        n.vectors    = set_array_values("vectors"  , "null",     num_streams)  # depends on datm_mode; see L3065

def set_array_values(key, default_val, array_len):
    if key in _user_nl:
        return _user_nl[key]
    else:
        return [default_val] * array_len

def generate_streams():
    datm_mode = _opts["datm_mode"]
    datm_presaero = _opts["datm_presaero"]

    s_files = {"Solar":    f'datm.streams.txt.{datm_mode}.Solar',
               "Precip":   f'datm.streams.txt.{datm_mode}.Precip', 
               "TPQW":     f'datm.streams.txt.{datm_mode}.TPQW',
               "presaero": f'datm.streams.txt.presaero.{datm_presaero}',
               "topo":     f'datm.streams.txt.topo.observed'}

    yr_params = "{} {} {}".format(_opts["stream_year_align"],
                                  _opts["stream_year_first"],
                                  _opts["stream_year_last"])

    s_nml = [f'{s_files["Solar"]} {yr_params}',
             f'{s_files["Precip"]} {yr_params}',
             f'{s_files["TPQW"]} {yr_params}',
             f'{s_files["presaero"]} {PRESAERO_YR_PARAMS.get(datm_presaero)}',
             f'{s_files["topo"]} 1 1 1']

    return s_nml

def create_stream_files(out_dir : str):
    s_template = Template(STREAM_FILE_TEMPLATE)
    s_vars = {}
    s_files = []
    for stream in _nl.shr_strdata_nml.streams:
        s_file, s_type = parse_stream_param(stream)
        s_files.append(s_file)
        if s_type == "presaero":
            s_vars = deepcopy(PRESAERO_STREAM_DEFAULTS)
            s_vars["DOMAIN_FILE_PATH"]  = Path(_user_nl["domainfile"]).parent.absolute()
            s_vars["FIELD_FILE_PATH"]   = Path(_user_nl["domainfile"]).parent.absolute()
        elif s_type == "topo":
            s_vars = deepcopy(TOPO_STREAM_DEFAULTS)
            s_vars["DOMAIN_FILE_PATH"]  = Path(_user_nl["domainfile"]).parent.absolute()
            s_vars["FIELD_FILE_PATH"]   = Path(_user_nl["domainfile"]).parent.absolute()
        else:
            s_vars["DOMAIN_FILE_PATH"]  = Path(_user_nl["domainfile"]).parent.absolute()
            s_vars["DOMAIN_FILE_NAMES"] = Path(_user_nl["domainfile"]).name
            s_vars["FIELD_FILE_PATH"]   = _opts.get("stream_root_dir", "")
            s_vars["DOMAIN_VAR_NAMES"]  = DATM_STREAM_DEFAULTS["DOMAIN_VAR_NAMES"]
            s_vars["FIELD_VAR_NAMES"]   = DATM_STREAM_DEFAULTS["FIELD_VAR_NAMES"].get(s_type, "")
            s_vars["FIELD_FILE_NAMES"]  = _opts.get("stream_files", "")

        # Convert list variables into multiline strings with proper indentation
        for key, val in s_vars.items():
            if isinstance(val, list):
                indented_vals = [f'{INDENTS[key]}{v}' for v in val[1:]]
                s_vars[key] = val[0] + "\n"
                s_vars[key] += "\n".join(indented_vals)
        
        # Write stream file to disk
        with open(Path(out_dir, s_file), "w+") as output:
            output.write(s_template.safe_substitute(s_vars))
    return s_files

def parse_stream_param(stream):
    if len(stream.split(" ")) == 4:
        stream_file = stream.split(" ")[0]
        sf = stream_file.lower()
        if "solar" in sf:
            stream_type = "Solar"
        elif "precip" in sf:
            stream_type = "Precip"
        elif "tpqw" in sf:
            stream_type = "TPQW"
        elif "presaero" in sf:
            stream_type = "presaero"
        elif "topo" in sf:
            stream_type = "topo"
        else:
            stream_type = "Unknown"
        return stream_file, stream_type
    else:
        error(f"""
               Invalid stream namelist parameter '{line}'.
               The correct syntax is:
               <stream_file> <year_align> <year_first> <year_last>
               """)

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
    opts["stream_root_dir"] = "/p/scratch/nrw_test_case/COSMOREA6/forcings"
    opts["stream_files"] = ["2017-{}.nc".format(str(month).zfill(2)) for month in range(1,13)]
    opts["domainfile"] = "/p/scratch/nrw_test_case/domain.lnd.300x300_NRW_300x300_NRW.190619.nc"
    build_datm_in(opts, nl, "datm_in_test")

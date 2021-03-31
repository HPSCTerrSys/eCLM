"""
Work in progress. Plenty of other user options hasn't been covered yet. 
Default mosart_in values are based from these files:

[namelist_definition_mosart.xml]: https://github.com/ESCOMP/MOSART/blob/release-cesm2.0/cime_config/namelist_definition_mosart.xml
[config_component.xml]: https://github.com/ESCOMP/MOSART/blob/release-cesm2.0/cime_config/config_component.xml
"""

from pathlib import Path
from ..structures import mosart_in


__all__ = ['build_mosart_in']

# _in_nl = {}
# _in_opts = {}
# _nl = datm_in()

def build_mosart_in(opts: dict = None, nl_file: str = "mosart_in"):
    # Global vars aren't necessary for now
    # global _in_opts, _in_nl, _nl
    #_in_opts = opts
    #_in_nl = nl
    _nl = mosart_in()

    with _nl.mosart_inparm as n:
        n.bypass_routing_option = "direct_in_place"
        n.coupling_period = "10800"
        n.decomp_option = "roundrobin"
        n.delt_mosart = "3600"
        n.do_rtm = False
        n.do_rtmflood = False
        n.finidat_rtm = " "
        n.frivinp_rtm = opts.get("frivinp_rtm", "$CESMDATAROOT/inputdata")
        n.ice_runoff = True 
        n.qgwl_runoff_option = "threshold"
        n.rtmhist_fexcl1 = ""
        n.rtmhist_fexcl2 = ""
        n.rtmhist_fexcl3 = ""
        n.rtmhist_fincl1 = ""
        n.rtmhist_fincl2 = ""
        n.rtmhist_fincl3 = ""
        n.rtmhist_mfilt = 1
        n.rtmhist_ndens = 1 
        n.rtmhist_nhtfrq = 0
        n.smat_option = "Xonly"

    # Write to file
    if nl_file and Path(nl_file).name.strip() != "": 
        _nl.write(nl_file)
        print(f"Generated {Path(nl_file).name}")

def error(msg):
    raise ValueError(msg)

if __name__ == "__main__":
    """
    For testing purposes. To run gen_datm_in.py, 
    directly, execute it via Python script mode:
    
    $ cd <parent folder of clm5nl>
    $ python3 -m clm5nl.generators.gen_mosart_in   
    """
    opts, nl = {}, {}
    nl["frivinp_rtm"] = "/p/scratch/nrw_test_case/inputdata"
    build_mosart_in(opts, nl, "mosart_in_test")

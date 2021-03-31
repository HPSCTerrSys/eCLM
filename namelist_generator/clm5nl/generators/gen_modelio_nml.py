"""
Work in progress. Default modelio_nml values are based from namelist_definition_modelio.xml.

[namelist_definition_modelio.xml]: https://github.com/ESMCI/cime/blob/cime5.6.33/src/drivers/mct/cime_config/namelist_definition_modelio.xml
"""
from pathlib import Path
from ..structures import modelio_in
from datetime import datetime

__all__ = ['build_modelio_nml']

# _in_nl = {}
# _in_opts = {}
# _nl = datm_in()

def build_modelio_nml(opts: dict = None, out_dir: str = None):
    # Global vars aren't necessary for now
    # global _in_opts, _in_nl, _nl
    #_in_opts = opts
    #_in_nl = nl

    _nl = modelio_in()

    with _nl.modelio as n:
        n.diri = "UNUSED"
        n.diro = opts.get("run_dir", Path(out_dir).absolute())

    with _nl.pio_inparm as n:
        n.pio_netcdf_format = "64bit_offset"
        n.pio_numiotasks = -99
        n.pio_rearranger = 1
        n.pio_root = 1
        n.pio_stride = 8
        n.pio_typename = "netcdf"

    if out_dir is None: out_dir = Path.cwd()
    components = ["atm", "cpl", "esp", "glc", "ice", "lnd", "ocn", "rof", "wav"]
    for comp in components:
        nl_file = Path(out_dir, f"{comp}_modelio.nml")
        _nl.modelio.logfile = "{}.log.{}".format(comp, datetime.now().strftime("%Y-%m-%d_%H%M%S"))
        _nl.write(nl_file, ["modelio", "pio_inparm"])
        print(f"Generated {Path(nl_file).name}")

if __name__ == "__main__":
    """
    For testing purposes. To run gen_modelio_nml.py, 
    directly, execute it via Python script mode:
    
    $ cd <parent folder of clm5nl>
    $ python3 -m clm5nl.generators.gen_modelio_nml   
    """
    opts, nl = {}, {}
    opts["diro"] = "/p/scratch/nrw_test_case/run"
    out_dir = Path("modelio_test")
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving modelio namelists to {out_dir.absolute()}")
    build_modelio_nml(opts, nl, out_dir)
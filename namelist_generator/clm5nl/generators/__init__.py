from pathlib import PurePath, Path
from .gen_lnd_in import build_lnd_in
from .gen_datm_in import build_datm_in
from .gen_modelio_nml import build_modelio_nml
from .gen_mosart_in import build_mosart_in
from .gen_drv_in import build_drv_in
from .gen_seq_maps import build_seq_maps_rc
from .gen_drv_flds_in import build_drv_flds_in

__all__ = ['build_namelist',
           'build_lnd_in', 
           'build_datm_in', 
           'build_modelio_nml',
           'build_mosart_in',
           'build_drv_in',
           'build_seq_maps_rc',
           'build_drv_flds_in']

def build_namelist(nl_key: str, opts: dict, out_dir: str = ""):
    if str(out_dir).strip() != "":
        out_file = Path(out_dir) / nl_key
    else:
        out_file = Path.cwd() / nl_key

    if nl_key == "lnd_in":
        success, status_msg = build_lnd_in(opts, out_file)   
    elif nl_key == "datm_in":
        success, status_msg = build_datm_in(opts, out_file)
    elif nl_key == "mosart_in":
        success, status_msg = build_mosart_in(opts, out_file)
    elif nl_key == "drv_in":
        success, status_msg = build_drv_in(opts, out_file)
    elif nl_key == "seq_maps.rc":
        success, status_msg = build_seq_maps_rc(out_file)
    elif nl_key == "drv_flds_in":
        success, status_msg = build_drv_flds_in(opts, out_file)
    elif nl_key == "modelio_nml":
        success, status_msg = build_modelio_nml(opts, out_dir)
    else:
        success = False
        status_msg = f"build_namelist error: Namelist '{nl_key}' is not supported."
    if success: print_build_status(status_msg)
    return success, status_msg

def print_build_status(message):
    if isinstance(message, PurePath):
        print(f"--> Generated {Path(message).name}")
    elif isinstance(message, list):
        for m in message:
            print_build_status(m) 

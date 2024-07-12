"""
Work in progress. Plenty of other user options hasn't been covered yet. 
Default datm_in values are based from these files:

[namelist_definition_drv.xml]: https://github.com/ESMCI/cime/blob/cime5.6.33/src/drivers/mct/cime_config/namelist_definition_drv.xml
[config_component.xml]: https://github.com/ESMCI/cime/blob/cime5.6.33/src/drivers/mct/cime_config/config_component.xml
"""
from pathlib import Path
from io import StringIO
from ..structures import drv_in

__all__ = ['build_drv_in','build_seq_maps_rc']

BASE_DT = {
    "hour"   : 3600,
    "day"    : 3600 * 24,
    "year"   : 3600 * 24 * 365,
    "decade" : 3600 * 24 * 365 * 10
}

_user_nl = {}
_opts = {}
_nl = drv_in()

def build_drv_in(opts: dict = None, user_nl: dict = None, nl_file: str = None):
    global _opts, _user_nl, _nl

    _opts = opts
    _user_nl = user_nl
    _nl = drv_in()

    # Generate sections of drv_in namelist
    seq_timemgr_inparm()

    # setup_cmdl_run_type
    if _opts["clm_start_type"] == "default":
        first_yr = _nl.seq_timemgr_inparm.start_ymd / 10000
        if first_yr == 1850 or first_yr == 2000:
            _opts["clm_start_type"] = "startup"
        else:
            _opts["clm_start_type"] = "arb_ic"

    seq_infodata_inparm()
    cime_driver_inst()
    cime_pes()
    esmf_inparm()
    papi_inparm()
    pio_default_inparm()
    prof_inparm()
    seq_cplflds_inparm()
    seq_cplflds_userspec()
    seq_flux_mct_inparm()
    #Write to file
    if nl_file: 
        _nl.write(nl_file)
        print(f"Generated {Path(nl_file).name}")

def build_seq_maps_rc(out_dir: str = None):
    # Seems like this could be transformed into a
    # loop, but I don't see a clear pattern how.
    seq_maps = {
        "atm2ice_fmapname" : "idmap",
        "atm2ice_fmaptype" : "X",
        "atm2ice_smapname" : "idmap",
        "atm2ice_smaptype" : "X",
        "atm2ice_vmapname" : "idmap",
        "atm2ice_vmaptype" : "X",
        "atm2lnd_fmapname" : "idmap",
        "atm2lnd_fmaptype" : "X",
        "atm2lnd_smapname" : "idmap",
        "atm2lnd_smaptype" : "X",
        "atm2ocn_fmapname" : "idmap",
        "atm2ocn_fmaptype" : "X",
        "atm2ocn_smapname" : "idmap",
        "atm2ocn_smaptype" : "X",
        "atm2ocn_vmapname" : "idmap",
        "atm2ocn_vmaptype" : "X",
        "atm2wav_smapname" : "idmap",
        "atm2wav_smaptype" : "Y",
        "glc2ice_rmapname" : "idmap_ignore",
        "glc2ice_rmaptype" : "Y",
        "glc2lnd_fmapname" : "idmap",
        "glc2lnd_fmaptype" : "Y",
        "glc2lnd_smapname" : "idmap",
        "glc2lnd_smaptype" : "Y",
        "glc2ocn_ice_rmapname" : "idmap_ignore",
        "glc2ocn_ice_rmaptype" : "Y",
        "glc2ocn_liq_rmapname" : "idmap_ignore",
        "glc2ocn_liq_rmaptype" : "Y",
        "ice2atm_fmapname" : "idmap",
        "ice2atm_fmaptype" : "Y",
        "ice2atm_smapname" : "idmap",
        "ice2atm_smaptype" : "Y",
        "ice2wav_smapname" : "idmap",
        "ice2wav_smaptype" : "Y",
        "lnd2atm_fmapname" : "idmap",
        "lnd2atm_fmaptype" : "Y",
        "lnd2atm_smapname" : "idmap",
        "lnd2atm_smaptype" : "Y",
        "lnd2glc_fmapname" : "idmap",
        "lnd2glc_fmaptype" : "X",
        "lnd2glc_smapname" : "idmap",
        "lnd2glc_smaptype" : "X",
        "lnd2rof_fmapname" : "idmap",
        "lnd2rof_fmaptype" : "X",
        "ocn2atm_fmapname" : "idmap",
        "ocn2atm_fmaptype" : "Y",
        "ocn2atm_smapname" : "idmap",
        "ocn2atm_smaptype" : "Y",
        "ocn2wav_smapname" : "idmap",
        "ocn2wav_smaptype" : "Y",
        "rof2lnd_fmapname" : "idmap",
        "rof2lnd_fmaptype" : "Y",
        "rof2ocn_fmapname" : "idmap_ignore",
        "rof2ocn_fmaptype" : "Y",
        "rof2ocn_ice_rmapname" : "idmap",
        "rof2ocn_ice_rmaptype" : "Y",
        "rof2ocn_liq_rmapname" : "idmap",
        "rof2ocn_liq_rmaptype" : "Y",
        "wav2ocn_smapname" : "idmap",
        "wav2ocn_smaptype" : "X"
    }

    if out_dir is None: out_dir = Path.cwd()
    seq_maps_file = Path(out_dir, "seq_maps.rc")
    with open(seq_maps_file, "w") as f:
        for k, v in seq_maps.items():
            f.write(f'{k} : "{v}"\n')
    print(f"Generated {Path(seq_maps_file).name}")

def error(msg):
    raise ValueError(msg)

def cime_driver_inst():
    _nl.cime_driver_inst.ninst_driver = 1

def cime_pes():
    with _nl.cime_pes as n:
        n.atm_layout   = "concurrent"
        n.atm_ntasks   = _opts["NTASKS"]
        n.atm_nthreads = _opts.get("NTHREADS", 1)
        n.atm_pestride = 1
        n.atm_rootpe   = 0
        n.cpl_ntasks   = _opts["NTASKS"]
        n.cpl_nthreads = _opts.get("NTHREADS", 1)
        n.cpl_pestride = 1
        n.cpl_rootpe   = 0
        n.esp_layout   = "concurrent"
        n.esp_ntasks   = _opts["NTASKS"]
        n.esp_nthreads = _opts.get("NTHREADS", 1)
        n.esp_pestride = 1
        n.esp_rootpe   = 0
        n.glc_layout   = "concurrent"
        n.glc_ntasks   = _opts["NTASKS"]
        n.glc_nthreads = _opts.get("NTHREADS", 1)
        n.glc_pestride = 1
        n.glc_rootpe   = 0
        n.ice_layout   = "concurrent"
        n.ice_ntasks   = _opts["NTASKS"]
        n.ice_nthreads = _opts.get("NTHREADS", 1)
        n.ice_pestride = 1
        n.ice_rootpe   = 0
        n.lnd_layout   = "concurrent"
        n.lnd_ntasks   = _opts["NTASKS"]
        n.lnd_nthreads = _opts.get("NTHREADS", 1)
        n.lnd_pestride = 1
        n.lnd_rootpe   = 0
        n.ocn_layout   = "concurrent"
        n.ocn_ntasks   = _opts["NTASKS"]
        n.ocn_nthreads = _opts.get("NTHREADS", 1)
        n.ocn_pestride = 1
        n.ocn_rootpe   = 0
        # TODO: Include logic for compset-dependent parameters
        # n.rof_layout   = "concurrent"
        # n.rof_ntasks   = _opts["NTASKS"]
        # n.rof_nthreads = _opts.get("NTHREADS", 1)
        # n.rof_pestride = 1
        # n.rof_rootpe   = 0
        # n.wav_layout   = "concurrent"
        # n.wav_ntasks   = _opts["NTASKS"]
        # n.wav_nthreads = _opts.get("NTHREADS", 1)
        # n.wav_pestride = 1
        # n.wav_rootpe   = 0

def esmf_inparm():
    _nl.esmf_inparm.esmf_logfile_kind = "ESMF_LOGKIND_NONE"

def papi_inparm():
    with _nl.papi_inparm as n:
        n.papi_ctr1_str = "PAPI_FP_OPS"
        n.papi_ctr2_str = "PAPI_NO_CTR"
        n.papi_ctr3_str = "PAPI_NO_CTR"
        n.papi_ctr4_str = "PAPI_NO_CTR"

def pio_default_inparm():
    with _nl.pio_default_inparm as n:
        n.pio_async_interface = False
        n.pio_blocksize = -1
        n.pio_buffer_size_limit = -1
        n.pio_debug_level = 0
        n.pio_rearr_comm_enable_hs_comp2io = True
        n.pio_rearr_comm_enable_hs_io2comp = False
        n.pio_rearr_comm_enable_isend_comp2io = False
        n.pio_rearr_comm_enable_isend_io2comp = True
        n.pio_rearr_comm_fcd = "2denable"
        n.pio_rearr_comm_max_pend_req_comp2io = 0
        n.pio_rearr_comm_max_pend_req_io2comp = 64
        n.pio_rearr_comm_type = "p2p"

def prof_inparm():
    with _nl.prof_inparm as n:
        n.profile_add_detail = False
        n.profile_barrier = False
        n.profile_depth_limit = 4
        n.profile_detail_limit = 2
        n.profile_disable = False
        n.profile_global_stats = True
        n.profile_outpe_num = 1
        n.profile_outpe_stride = 0
        n.profile_ovhd_measurement = False
        n.profile_papi_enable = False
        n.profile_single_file = False
        n.profile_timer = 4

def seq_cplflds_inparm():
    with _nl.seq_cplflds_inparm as n:
        n.flds_bgc_oi = False
        n.flds_co2_dmsa = False
        n.flds_co2a = False
        n.flds_co2b = False
        n.flds_co2c = False
        n.flds_wiso = False
        n.glc_nec = 10 # TODO: check dependency with maxpatch_glcmec parameter from lnd_in 
        n.ice_ncat = 1
        n.nan_check_component_fields = True
        n.seq_flds_i2o_per_cat = False

def seq_cplflds_userspec():
    _nl.seq_cplflds_userspec.cplflds_custom = ""

def seq_flux_mct_inparm():
    with _nl.seq_flux_mct_inparm as n:
        n.seq_flux_atmocn_minwind = 0.5
        n.seq_flux_mct_albdif = 0.06
        n.seq_flux_mct_albdir = 0.07

def seq_infodata_inparm():
    with _nl.seq_infodata_inparm as n:
        # process_namelist_commandline_clm_start_type
        if _opts["clm_start_type"] == "cold" or _opts["clm_start_type"] == "arb_ic":
            n.start_type = "startup"
        else:
            n.start_type = _opts["clm_start_type"]
        n.aoflux_grid = "ocn"
        n.aqua_planet = False
        n.aqua_planet_sst = 1
        n.atm_gnam = "CLM_USRDAT"
        n.bfbflag = False
        n.brnch_retain_casename = False
        n.budget_ann = 1
        n.budget_daily = 0
        n.budget_inst = 0
        n.budget_ltann = 1
        n.budget_ltend = 0
        n.budget_month = 1
        n.case_desc = "UNSET"
        n.case_name = _opts.get("CASE","UNSET")
        n.cime_model = "cesm"
        n.coldair_outbreak_mod = True
        n.cpl_decomp = 0
        n.cpl_seq_option = "CESM1_MOD"
        n.do_budgets = False
        n.do_histinit = False
        n.drv_threading = False
        n.eps_aarea = 9e-07
        n.eps_agrid = 1e-12
        n.eps_amask = 1e-13
        n.eps_frac = 1.0e-02
        n.eps_oarea = 0.1
        n.eps_ogrid = 0.01
        n.eps_omask = 1e-06
        n.flux_albav = False
        n.flux_convergence = 0.01
        n.flux_diurnal = False
        n.flux_epbal = "off"
        n.flux_max_iteration = 5
        n.force_stop_at = "month"
        n.glc_gnam = "null"
        n.glc_renormalize_smb = "on_if_glc_coupled_fluxes"
        n.gust_fac = 0.0
        n.histaux_a2x = False
        n.histaux_a2x1hr = False
        n.histaux_a2x1hri = False
        n.histaux_a2x24hr = False
        n.histaux_a2x3hr = False
        n.histaux_a2x3hrp = False
        n.histaux_double_precision = False
        n.histaux_l2x = False
        n.histaux_l2x1yrg = False
        n.histaux_r2x = False
        n.histavg_atm = True
        n.histavg_glc = True
        n.histavg_ice = True
        n.histavg_lnd = True
        n.histavg_ocn = True
        n.histavg_rof = True
        n.histavg_wav = True
        n.histavg_xao = True
        n.hostname = _opts.get("HOSTNAME","MACHINE")
        n.ice_gnam = "null"
        n.info_debug = 1
        n.lnd_gnam = "CLM_USRDAT"
        n.logfilepostfix = ".log"
        n.max_cplstep_time = 0.0
        n.mct_usealltoall = False
        n.mct_usevector = False
        n.model_doi_url = "https://doi.org/10.5065/D67H1H0V"
        n.model_version = "release-clm5.0.34-2-ga2989b0"
        n.ocn_gnam = "null"
        n.orb_eccen = 1.e36
        n.orb_iyear = 2000
        n.orb_iyear_align = 2000
        n.orb_mode = "fixed_year"
        n.orb_mvelp = 1.e36
        n.orb_obliq = 1.e36
        n.outpathroot = "./"
        n.reprosum_diffmax = -1.0e-8
        n.reprosum_recompute = False
        n.reprosum_use_ddpdd = False
        n.restart_file = "str_undefined"
        n.rof_gnam = "null"
        n.run_barriers = False
        n.scmlat = -999.
        n.scmlon = -999.
        n.shr_map_dopole = True
        n.single_column = False
        n.tchkpt_dir = "timing/checkpoints"
        n.tfreeze_option = "mushy"
        n.timing_dir = "timing"
        n.username = "user1"
        n.vect_map = "cart3d"
        n.wall_time_limit = -1.0
        n.wav_gnam = "null"
        n.wv_sat_scheme = "GoffGratch"
        n.wv_sat_table_spacing = 1.0
        n.wv_sat_transition_start = 20.0
        n.wv_sat_use_tables = False

        # Overwrite brnch_retain_casename
        if n.start_type != 'startup':
            if (_opts.get("CASE","UNSET") == _opts.get("RUN_REFCASE","case.std")):
                n.brnch_retain_casename = True

def seq_timemgr_inparm():
    with _nl.seq_timemgr_inparm as n:
        # Important time parameters
        n.stop_option = _opts["STOP_OPTION"]
        n.start_ymd = int("".join(str(x) for x in _opts["RUN_STARTDATE"].split('-')))      
        n.stop_ymd = int("".join(str(x) for x in _opts["STOP_DATE"].split('-')))
        n.stop_n = _opts.get("STOP_N", -1)
        n.restart_option = _opts.get("RESTART_OPTION", n.stop_option)
        n.restart_ymd = n.stop_ymd
        n.restart_n = n.stop_n

        # set component coupling frequencies
        base_period  = _opts.get("NCPL_BASE_PERIOD","day")
        if _opts.get("CALENDAR", "NO_LEAP") != 'NO_LEAP' and (base_period == "year" or base_period == "decade"):
            error(f"Invalid CALENDAR for NCPL_BASE_PERIOD {base_period} ")
        cpl_dt = {comp : calc_cpl_dt(comp, base_period) for comp in ["atm", "glc", "ice", "lnd", "ocn", "rof", "wav"]}
        cpl_dt["base_dt"] = BASE_DT[base_period]
        if cpl_dt["atm"] != min(cpl_dt.values()):
            error("Active atm should match shortest model timestep atmdt={} mindt={}".format(cpl_dt["atm"], min(cpl_dt.values())))
        n.atm_cpl_dt = cpl_dt["atm"]
        n.glc_cpl_dt = cpl_dt["glc"]
        n.ice_cpl_dt = cpl_dt["ice"]
        n.lnd_cpl_dt = cpl_dt["lnd"]
        n.ocn_cpl_dt = cpl_dt["ocn"]
        n.rof_cpl_dt = cpl_dt["rof"]
        n.wav_cpl_dt = cpl_dt["wav"]

        # set tprof_option and tprof_n - if tprof_total is > 0
        stop_option = _opts["STOP_OPTION"]
        if 'nyear' in stop_option:
            tprofoption = 'ndays'
            tprof_mult = 365
        elif 'nmonth' in stop_option:
            tprofoption = 'ndays'
            tprof_mult = 30
        elif 'nday' in stop_option:
            tprofoption = 'ndays'
            tprof_mult = 1
        else:
            tprof_mult = 1
            tprofoption = 'never'
        tprof_total = _opts.get("TPROF_TOTAL", 0)
        if ((tprof_total > 0) and (_opts.get("STOP_DATE",-999) < 0) and ('ndays' in tprofoption)):
            tprof_n = int((tprof_mult * n.stop_n) / tprof_total)
            n.tprof_option = tprofoption
            n.tprof_n = tprof_n if tprof_n > 0 else 1
        else:
            n.tprof_n = -999
            n.tprof_option = "never"

        # Set esp interval if pause is active
        n.pause_n = _opts.get("PAUSE_N",0)
        n.pause_option = _opts.get("PAUSE_OPTION", "never")
        if n.pause_option not in ["never", "none", None]:
            if "nstep" in n.pause_option:
                n.esp_cpl_dt = min(cpl_dt.values())
            else:
                n.esp_cpl_dt = get_time_in_seconds(n.pause_n, n.pause_option)

        # Set defaults
        n.atm_cpl_offset = 0
        n.barrier_n = 1
        n.barrier_option = "ndays"
        n.barrier_ymd = -999
        n.calendar = "NO_LEAP"
        n.data_assimilation_atm = False
        n.data_assimilation_cpl = False
        n.data_assimilation_glc = False
        n.data_assimilation_ice = False
        n.data_assimilation_lnd = False
        n.data_assimilation_ocn = False
        n.data_assimilation_rof = False
        n.data_assimilation_wav = False
        n.end_restart = False
        n.esp_cpl_offset = 0
        n.esp_run_on_pause = True
        n.glc_avg_period = "yearly"
        n.glc_cpl_offset = 0
        n.histavg_n = -999
        n.histavg_option = "never"
        n.histavg_ymd = -999
        n.history_n = -999
        n.history_option = "never"
        n.history_ymd = -999
        n.ice_cpl_offset = 0
        n.lnd_cpl_offset = 0
        n.ocn_cpl_offset = 0
        n.pause_active_atm = False
        n.pause_active_cpl = False
        n.pause_active_glc = False
        n.pause_active_ice = False
        n.pause_active_lnd = False
        n.pause_active_ocn = False
        n.pause_active_rof = False
        n.pause_active_wav = False   
        n.start_tod = 0
        n.tprof_ymd = -999
        n.wav_cpl_offset = 0

def calc_cpl_dt(comp, base_period):
    ncpl = _opts.get("{}_NCPL".format(comp.upper()), 48) #TODO: default NCPL must be computed!
    if ncpl is not None:
        cpl_dt = int(BASE_DT[base_period] / int(ncpl))
        total_dt = cpl_dt * int(ncpl)
        if total_dt != BASE_DT[base_period]:
            error(f"{comp} ncpl doesn't divide base dt evenly")
        return cpl_dt

def get_time_in_seconds(timeval, unit):
    """
    Convert a time from 'unit' to seconds
    """
    if 'nyear' in unit:
        dmult = 365 * 24 * 3600
    elif 'nmonth' in unit:
        dmult = 30 * 24 * 3600
    elif 'nday' in unit:
        dmult = 24 * 3600
    elif 'nhour' in unit:
        dmult = 3600
    elif 'nminute' in unit:
        dmult = 60
    else:
        dmult = 1

    return dmult * timeval
            
if __name__ == "__main__":
    """
    For testing purposes. To run gen_datm_in.py, 
    directly, execute it via Python script mode:
    
    $ cd <parent folder of clm5nl>
    $ python3 -m clm5nl.generators.gen_drv_in   
    """
    opts, user_nl = {}, {}
    opts["CASE"] = "NRW_300x300"
    opts["HOSTNAME"] = "JUWELS"
    opts["RUN_REFCASE"] = "case.std" # L78 
    opts["CALENDAR"] = "NO_LEAP"
    opts["STOP_OPTION"] = "date"
    opts["RUN_STARTDATE"] = "2017-01-01"
    opts["STOP_DATE"] = "2017-12-31"
    opts["STOP_N"] = -1
    opts["TPROF_TOTAL"] = 0
    opts["PAUSE_N"] = 0
    opts["PAUSE_OPTION"] = "never"
    opts["NCPL_BASE_PERIOD"] = "day" # L78
    opts["ATM_NCPL"] = 48
    opts["LND_NCPL"] = 48
    opts["ICE_NCPL"] = 48
    opts["OCN_NCPL"] = 48
    opts["GLC_NCPL"] = 48
    opts["ESP_NCPL"] = 48 
    opts["ROF_NCPL"] = 8
    opts["WAV_NCPL"] = 48
    opts["NTASKS"] = 96     # number of MPI tasks
    opts["clm_start_type"] = "default"

    build_drv_in(opts, user_nl, "drv_in_test")
    build_seq_maps_rc()

"""
Contains the core logic how the parameters in lnd_in are generated. 
The codes are ported from the Perl script [CLMBuildNamelist.pm]. 

STATUS: This module is still **under heavy development**. Testing was done 
only on one specific case. More work still needs to be done to cover all 
CLM5 model capabilities.

[CLMBuildNamelist.pm]: https://github.com/ESCOMP/CTSM/blob/03954bf6f697a019f289632636007a29a21e79d2/bld/CLMBuildNamelist.pm
"""
from pathlib import Path
from ..structures import lnd_in, drv_in

__all__ = ['build_lnd_in']

# Module-level variables
_env = {}
_opts = {}
_user_nl = {}
_nl = lnd_in()

def build_lnd_in(opts: dict = None, nl_file: str = "lnd_in"):

    # Initialize module level variables
    global _opts, _user_nl
    global _nl, _env
    _opts = opts
    _user_nl = opts.get("user_nl", {})
    _nl = lnd_in()

    # set defaults
    if "drv_in.start_type" not in _opts:
        return False, "Missing required option 'drv_in.start_type"
    _opts["clm_start_type"] = opts.get("clm_start_type", "startup")
    _opts["co2_ppmv"] = opts.get("co2_ppmv", 367.0)
    _opts["co2_type"] = opts.get("co2_type", "constant")
    _opts["crop"] = opts.get("crop", 1) #if opts["bgc_mode"] != "sp"
    _opts["dtime"] = opts.get("dtime", None)
    _opts["dynamic_vegetation"] = opts.get("dynamic_vegetation", 0)
    _opts["GLC_TWO_WAY_COUPLING"] = opts.get("GLC_TWO_WAY_COUPLING", False)
    _opts["glc_nec"] = opts.get("glc_nec", 10)
    _opts["ignore_ic_date"] = opts.get("ignore_ic_date", False)
    _opts["ignore_ic_year"] = opts.get("ignore_ic_year", False)
    _opts["light_res"] = opts.get("light_res", "default")
    _opts["nrevsn"] = opts.get("nrevsn", None) # required if start_type=branch
    _opts["override_nsrest"] = opts.get("override_nsrest", None)
    _opts["res"] = opts.get("res", "UNSET")
    _opts["ssp_rcp"] = opts.get("ssp_rcp", "hist")
    _opts["use_case"] = opts.get("use_case", None)
    _opts["use_dynroot"] = opts.get("use_dynroot", False)
    _opts["use_init_interp"] = opts.get("use_init_interp", True)
    _opts["vichydro"] = opts.get("vichydro", 0)

    _env = {"bgc_spinup":None,
            "cnfireson":None,
            "finundation_res":None,
            "mask":None,
            "use_case_desc":None}

    # Build lnd_in namelist
    process_namelist_commandline_options()         # high-level options (e.g sim year, bgc mode, spinup option, )
    process_namelist_commandline_use_case()        # use case (e.g. 1850, 20th century, 2000, 2010, SSPx-y.z)
    process_namelist_inline_logic()                # rest of namelist parameters

    # this param is needed by drv_flds_in
    _opts["use_fates"] = _nl.clm_inparm.use_fates
    
    # Write to file
    if nl_file and Path(nl_file).name.strip() != "":
        _nl.write(nl_file, lnd_nl_groups())
        return True, Path(nl_file)
    else:
        return True, ""
   
def process_namelist_commandline_options():
    #setup_cmdl_chk_res()
    #  _opts["chk_res"] = 0

    #setup_cmdl_resolution()
    _opts["res"] = "UNSET"

    #setup_cmdl_mask()
    _env["mask"] = "gx1v6"

    setup_cmdl_bgc()
    setup_cmdl_fire_light_res() #?
    setup_cmdl_spinup()
    setup_cmdl_crop()

    #setup_cmdl_maxpft()
    _nl.clm_inparm.maxpatch_pft = 79 if _nl.clm_inparm.use_crop else 17

    #setup_cmdl_irrigation()
    #_env["irrig"] = False #only for CLM4.0 physics

    #setup_cmdl_ssp_rcp()
    _opts["ssp_rcp"] = "hist"

    #setup_cmdl_simulation_year()
    _opts["sim_year_range"] = "constant"
    _opts["sim_year"] = 2000

    setup_cmdl_dynamic_vegetation()
    setup_cmdl_fates_mode()

    #setup_cmdl_vichydro()
    if _opts["vichydro"] == 1:
        _nl.clm_inparm.use_vichydro = True

    #setup_cmdl_output_reals()

    #setup_logic_lnd_tuning()
    _opts["lnd_tuning_mode"] = "clm5_0_GSWP3v1"

def process_namelist_commandline_use_case():
    # TODO: read default values from _opts["use_case"] XML file
    #2000_control.xml
    _nl.clm_inparm.irrigate = True
    _opts["sim_year"] = 2000
    _opts["sim_year_range"] = "constant"
    _nl.ndepdyn_nml.stream_year_first_ndep = 2000
    _nl.ndepdyn_nml.stream_year_last_ndep = 2000
    _nl.popd_streams.stream_year_first_popdens = 2000
    _nl.popd_streams.stream_year_last_popdens = 2000
    _nl.urbantv_streams.stream_year_first_urbantv = 2000
    _nl.urbantv_streams.stream_year_last_urbantv = 2000
    _env["use_case_desc"] = "Conditions to simulate 2000 land-use"

def error(msg):
    raise ValueError(msg)

def process_namelist_inline_logic():

    ##############################
    # namelist group: clm_inparm #
    ##############################
    setup_logic_site_specific()
    setup_logic_lnd_frac()
    setup_logic_co2_type()
    setup_logic_irrigate()
    setup_logic_start_type()
    setup_logic_delta_time()
    setup_logic_decomp_performance()
    setup_logic_snow()
    setup_logic_glacier()
    setup_logic_dynamic_plant_nitrogen_alloc()
    setup_logic_luna()
    setup_logic_hydrstress()
    setup_logic_dynamic_roots()
    setup_logic_params_file()
    setup_logic_create_crop_landunit()
    setup_logic_subgrid()
    setup_logic_fertilizer()
    setup_logic_grainproduct()
    setup_logic_soilstate()
    setup_logic_demand()
    setup_logic_surface_dataset()
    if _opts["clm_start_type"] != "branch":
        setup_logic_initial_conditions()
    setup_logic_dynamic_subgrid()
    setup_logic_spinup()
    setup_logic_supplemental_nitrogen()
    setup_logic_snowpack()
    setup_logic_fates()

    #########################################
    # namelist group: atm2lnd_inparm
    #########################################
    setup_logic_atm_forcing()

    #########################################
    # namelist group: lnd2atm_inparm
    #########################################
    setup_logic_lnd2atm()

    #########################################
    # namelist group: clm_humanindex_inparm #
    #########################################
    setup_logic_humanindex()

    #################################
    # namelist group: cnfire_inparm #
    #################################
    setup_logic_cnfire()

    ######################################
    # namelist group: cnprecision_inparm #
    ######################################
    setup_logic_cnprec()

    ###############################
    # namelist group: clmu_inparm #
    ###############################
    setup_logic_urban()

    ###############################
    # namelist group: crop        #
    ###############################
    setup_logic_crop()

    ###############################
    # namelist group: ch4par_in   #
    ###############################
    setup_logic_methane()
    setup_logic_c_isotope()

    ###############################
    # namelist group: ndepdyn_nml #
    ###############################
    setup_logic_nitrogen_deposition()

    ##########################################
    # namelist group: soil_moisture_streams  #
    ##########################################
    setup_logic_soilm_streams()

    ##################################
    # namelist group: cnmresp_inparm #
    ##################################
    setup_logic_cnmresp()

    #################################
    # namelist group: nitrif_inparm #
    #################################
    setup_logic_nitrif_params()

    ####################################
    # namelist group: photosyns_inparm #
    ####################################
    setup_logic_photosyns()

    #################################
    # namelist group: popd_streams  #
    #################################
    setup_logic_popd_streams()

    ####################################
    # namelist group: urbantv_streams  #
    ####################################
    setup_logic_urbantv_streams()

    ##################################
    # namelist group: light_streams  #
    ##################################
    setup_logic_lightning_streams()

    ##################################
    # namelist group: lai_streams  #
    ##################################
    setup_logic_lai_streams()

    ##################################
    # namelist group: bgc_shared
    ##################################
    setup_logic_bgc_shared()

    #############################################
    # namelist group: soilwater_movement_inparm #
    #############################################
    setup_logic_soilwater_movement()

    #############################################
    # namelist group: rooting_profile_inparm    #
    #############################################
    setup_logic_rooting_profile()

    #############################################
    # namelist group: friction_velocity         #
    #############################################
    setup_logic_friction_vel()

    ################################################
    # namelist group: century_soilbgcdecompcascade #
    ################################################
    setup_logic_century_soilbgcdecompcascade()

    #############################
    # namelist group: cngeneral #
    #############################
    setup_logic_cngeneral()

    ####################################
    # namelist group: cnvegcarbonstate #
    ####################################
    setup_logic_cnvegcarbonstate()

    #############################################
    # namelist group: soil_resis_inparm #
    #############################################
    setup_logic_soil_resis()

    #############################################
    # namelist group: canopyfluxes_inparm #
    #############################################
    setup_logic_canopyfluxes()

    #############################################
    # namelist group: canopyhydrology_inparm #
    #############################################
    setup_logic_canopyhydrology()

    #####################################
    # namelist group: clm_canopy_inparm #
    #####################################
    setup_logic_canopy()

    ########################################
    # namelist group: soilhydrology_inparm #
    ########################################
    setup_logic_hydrology_params()

    #####################################
    # namelist group: irrigation_inparm #
    #####################################
    setup_logic_irrigation_parameters()

    #######################################################################
    # namelist groups: clm_hydrology1_inparm and clm_soilhydrology_inparm #
    #######################################################################
    setup_logic_hydrology_switches()

    #########################################
    # namelist group: clm_initinterp_inparm #
    #########################################
    setup_logic_initinterp()

def lnd_nl_groups() -> list:
    """
    Namelist groups sorted in the same order as the lnd_in namelist 
    generated by CLM5.
    """
    return ["clm_inparm",
            "ndepdyn_nml",
            "popd_streams",
            "urbantv_streams",
            "light_streams",
            "soil_moisture_streams",
            "lai_streams",
            "atm2lnd_inparm",
            "lnd2atm_inparm",
            "clm_canopyhydrology_inparm",
            "cnphenology",
            "clm_soilhydrology_inparm",
            "dynamic_subgrid",
            "cnvegcarbonstate",
            "finidat_consistency_checks",
            "dynpft_consistency_checks",
            "clm_initinterp_inparm",
            "century_soilbgcdecompcascade",
            "soilhydrology_inparm",
            "luna",
            "friction_velocity",
            "mineral_nitrogen_dynamics",
            "soilwater_movement_inparm",
            "rooting_profile_inparm",
            "soil_resis_inparm",
            "bgc_shared",
            "canopyfluxes_inparm",
            "aerosol",
            "clmu_inparm",
            "clm_soilstate_inparm",
            "clm_nitrogen",
            "clm_snowhydrology_inparm",
            "cnprecision_inparm",
            "clm_glacier_behavior",
            "crop",
            "irrigation_inparm",
            "ch4par_in",
            "clm_humanindex_inparm",
            "cnmresp_inparm",
            "photosyns_inparm",
            "cnfire_inparm",
            "cn_general",
            "nitrif_inparm",
            "lifire_inparm",
            "ch4finundated",
            "clm_canopy_inparm"]

def setup_logic_site_specific():
    if _opts["res"] == "1x1_vancouverCAN":
        _nl.clm_inparm.use_vancouver = True
    elif _opts["res"] == "1x1_mexicocityMEX":
        _nl.clm_inparm.use_mexicocity = True
    elif _opts["res"] == "1x1_smallvilleIA" or _opts["res"] == "1x1_numaIA":
        if not (_opts["res"] or _nl.clm_inparm.use_crop):
            error("{} grids must use a compset with CN and CROP turned on".format(_opts["res"]))

def setup_logic_lnd_frac():
    _nl.clm_inparm.fatmlndfrc = _opts["lnd_frac"]

def setup_logic_co2_type():
    _nl.clm_inparm.co2_type = _opts["co2_type"]
    if _opts["co2_type"] == "constant":     
        if _opts["co2_ppmv"] is None:
            if _opts["sim_year"] == 2100:
                ssp_co2_defaults = {"SSP5-8.5":1135.2, "SSP5-3.4":496.6, "SSP1-2.6":445.6}
                _nl.clm_inparm.co2_ppmv = ssp_co2_defaults.get(_opts["ssp_rcp"], "Invalid ssp_rcp value")
            else:
                yearly_co2_defaults = {"1000":379.0, "1850":284.7, "2000":379.0, "2010":388.8, "2015":397.5, "PtVg":284.7}
                _nl.clm_inparm.co2_ppmv = yearly_co2_defaults.get(_opts["sim_year"],"Invalid sim_year value")
        else:
            if _opts["co2_ppmv"] <= 0:
                error("co2_ppmv can NOT be less than or equal to zero")
            else:
                _nl.clm_inparm.co2_ppmv = _opts["co2_ppmv"]

def setup_logic_irrigate():
    _nl.clm_inparm.irrigate = not (_nl.clm_inparm.use_crop and _nl.clm_inparm.use_cndv)

def setup_logic_start_type():
    my_start_type = _opts["clm_start_type"]
    drv_in_start_type = _opts["drv_in.start_type"]
    if not _opts["override_nsrest"] == None:
        start_type = {0:"startup", 1:"continue", 3:"branch"}
        my_start_type = start_type.get(_opts["override_nsrest"], "Invalid start_type value")
        if my_start_type == drv_in_start_type:
            error("no need to set override_nsrest to same as start_type")
        if drv_in_start_type != "startup":
            error("can NOT set override_nsrest if driver is NOT a startup type")
        _nl.clm_inparm.override_nsrest = _opts["override_nsrest"]
    
    if my_start_type == "branch":
        if _opts["nrevsn"] is None:
            error("nrevsn is required for a branch type.")
        else:
            _nl.clm_inparm.nrevsn = _opts["nrevsn"]
        if _opts["use_init_interp"]:
            print("WARNING: use_init_interp will NOT happen for a branch case.")
    else:
        if not _opts["nrevsn"] is None:
            error("nrevsn should ONLY be set for a branch type")
    if _opts["use_init_interp"]:
        _nl.clm_inparm.use_init_interp = True

def setup_logic_delta_time():
    if _opts["l_ncpl"] is None:
        _nl.clm_inparm.dtime = 1800
    else:
        if _opts["l_ncpl"] <= 0: 
            error("bad value for -l_ncpl option")
        if _opts["dtime"] is None:
            _nl.clm_inparm.dtime = (3600 * 24) / _opts["l_ncpl"]
        else:
            error("can NOT set both -l_ncpl option (via LND_NCPL env variable) AND dtime namelist variable.")

def setup_logic_decomp_performance():
    _nl.clm_inparm.nsegspc = 35

def setup_logic_snow():
    _nl.clm_canopyhydrology_inparm.snowveg_flag = "ON_RAD"
    if _user_nl["fsnowoptics"] is not None:
        _nl.clm_inparm.fsnowoptics = _user_nl["fsnowoptics"]
    else:
       _nl.clm_inparm.fsnowoptics = "lnd/clm2/snicardata/snicar_optics_5bnd_c090915.nc"
    if _user_nl["fsnowaging"] is not None:
        _nl.clm_inparm.fsnowaging = _user_nl["fsnowaging"]
    else:
        _nl.clm_inparm.fsnowaging = "lnd/clm2/snicardata/snicar_drdt_bst_fit_60_c070416.nc"

def setup_logic_glacier():
    # glc_do_dynglacier is set via GLC_TWO_WAY_COUPLING; it cannot be set via
    # user_nl_clm (this is because we might eventually want the coupler and glc
    # to also respond to GLC_TWO_WAY_COUPLING, by not bothering to send / map
    # these fields - so we want to ensure that CLM is truly listening to this
    # shared xml variable and not overriding it)
    with _nl.clm_inparm as n:
        n.glc_do_dynglacier = _opts["GLC_TWO_WAY_COUPLING"]
        n.maxpatch_glcmec = _opts["glc_nec"]
        n.glc_snow_persistence_max_days = 0
        n.albice = [0.50, 0.30]

    with _nl.clm_glacier_behavior as n:
        n.glacier_region_behavior = ["single_at_atm_topo", "virtual", "virtual", "multiple"]
        n.glacier_region_melt_behavior = ["remains_in_place", "replaced_by_ice", "replaced_by_ice", "replaced_by_ice"]
        n.glacier_region_ice_runoff_behavior = ["melted", "melted", "remains_ice", "remains_ice"]
        n.glacier_region_rain_to_snow_behavior = ["converted_to_snow", "converted_to_snow", "converted_to_snow", "converted_to_snow"]

def setup_logic_dynamic_plant_nitrogen_alloc():
    if _nl.clm_inparm.use_cn:
        _nl.clm_inparm.use_cn = True
        _nl.clm_inparm.use_flexibleCN = True
        with _nl.clm_nitrogen as n:
            n.MM_Nuptake_opt = True
            n.downreg_opt = False
            n.plant_ndemand_opt = 3
            n.substrate_term_opt = True
            n.nscalar_opt = True
            n.temp_scalar_opt = True
            n.CNratio_floating = True
            n.reduce_dayl_factor = False
            n.vcmax_opt = 3
            n.CN_residual_opt = 1
            n.CN_partition_opt = 1
            n.CN_evergreen_phenology_opt = 1
            n.carbon_resp_opt = 0 if _nl.clm_inparm.use_fun else 1

def setup_logic_luna():
    _nl.clm_inparm.use_luna = not _nl.clm_inparm.use_fates
    _nl.clm_inparm.use_nguardrail = _nl.clm_inparm.use_cn
    if _nl.clm_inparm.use_luna or _nl.clm_nitrogen.vcmax_opt == 3 or _nl.clm_nitrogen.vcmax_opt == 4:
        _nl.clm_nitrogen.lnc_opt = _nl.clm_inparm.use_cn
    if _nl.clm_nitrogen.lnc_opt and not _nl.clm_inparm.use_cn:
        error("Cannot turn lnc_opt to true when bgc=sp")
    if _nl.clm_inparm.use_luna:
        _nl.luna.jmaxb1 = 0.093563
    
def setup_logic_hydrstress():
    _nl.clm_inparm.use_hydrstress = not _nl.clm_inparm.use_fates

def setup_logic_dynamic_roots():
    with _nl.clm_inparm as n:
        n.use_dynroot = _opts["use_dynroot"]
        if n.use_dynroot:
            if _opts["bgc_mode"] == "sp":
                error("Cannot turn dynroot mode on mode bgc=sp. Set the bgc mode to 'cn' or 'bgc'")
            if n.use_hydrstress:
                error("Cannot turn use_dynroot on when use_hydrstress is on")

def setup_logic_params_file():
    if _user_nl["paramfile"] is not None:
        _nl.clm_inparm.paramfile = _user_nl["paramfile"]
    else:
        _nl.clm_inparm.paramfile = "lnd/clm2/paramdata/clm5_params.c171117.nc"

def setup_logic_create_crop_landunit():
    _nl.clm_inparm.create_crop_landunit = not _nl.clm_inparm.use_fates

def setup_logic_subgrid():
    _nl.clm_inparm.run_zero_weight_urban = False

def setup_logic_fertilizer():
    _nl.clm_inparm.use_fertilizer = _nl.clm_inparm.use_crop
    
def setup_logic_grainproduct():
    _nl.clm_inparm.use_grainproduct = _nl.clm_inparm.use_crop

def setup_logic_soilstate():
    _nl.clm_soilstate_inparm.organic_frac_squared = False
    _nl.clm_inparm.soil_layerstruct = "20SL_8.5m"
    _nl.clm_inparm.use_bedrock = not (_nl.clm_inparm.use_fates or _opts["vichydro"] == 1)

def setup_logic_demand():
    # Deal with options that the user has said are required...
    pass

def setup_logic_surface_dataset():
    if not _nl.dynamic_subgrid.flanduse_timeseries is None:
        if _nl.clm_inparm.use_cndv: error("dynamic PFT's (setting flanduse_timeseries) are incompatible with dynamic vegetation (use_cndv=.true)")
        if _nl.clm_inparm.use_fates: error("dynamic PFT's (setting flanduse_timeseries) are incompatible with ecosystem dynamics (use_fates=.true)")
    if _user_nl["fsurdat"] is not None:
        _nl.clm_inparm.fsurdat = _user_nl["fsurdat"]
    else:    
        surface_file = {}
        if _opts["sim_year"] == "1850":
            if _nl.clm_inparm.use_crop:
                surface_file["48x96"] = "release-clm5.0.18/surfdata_48x96_hist_78pfts_CMIP6_simyr1850_c190214.nc"
                surface_file["0.9x1.25"] ="release-clm5.0.18/surfdata_0.9x1.25_hist_78pfts_CMIP6_simyr1850_c190214.nc"
                surface_file["1.9x2.5"] = "release-clm5.0.18/surfdata_1.9x2.5_hist_78pfts_CMIP6_simyr1850_c190304.nc"
                surface_file["10x15"] = "release-clm5.0.18/surfdata_10x15_hist_78pfts_CMIP6_simyr1850_c190214.nc"
                surface_file["4x5"] = "release-clm5.0.18/surfdata_4x5_hist_78pfts_CMIP6_simyr1850_c190214.nc"
                surface_file["1x1_smallvilleIA"] = "release-clm5.0.18/surfdata_1x1_smallvilleIA_hist_78pfts_CMIP6_simyr1850_c190214.nc"
                surface_file["1x1_numaIA"] = "release-clm5.0.18/surfdata_1x1_numaIA_hist_78pfts_CMIP6_simyr1850_c190214.nc"
                surface_file["1x1_brazil"] = "release-clm5.0.18/surfdata_1x1_brazil_hist_78pfts_CMIP6_simyr1850_c190214.nc"
                surface_file["ne30np4"] = "landuse.timeseries_ne30np4_hist_16pfts_Irrig_CMIP6_simyr1850-2015_c170824.nc"
            elif not _nl.clm_inparm.use_crop and _nl.clm_inparm.irrigate:
                surface_file["48x96"] = "release-clm5.0.18/surfdata_48x96_hist_16pfts_Irrig_CMIP6_simyr1850_c190214.nc"
                surface_file["0.9x1.25"] = "release-clm5.0.18/surfdata_0.9x1.25_hist_16pfts_Irrig_CMIP6_simyr1850_c190214.nc"
                surface_file["1.9x2.5"] = "release-clm5.0.18/surfdata_1.9x2.5_hist_16pfts_Irrig_CMIP6_simyr1850_c190304.nc"
                surface_file["10x15"] = "release-clm5.0.18/surfdata_10x15_hist_16pfts_Irrig_CMIP6_simyr1850_c190214.nc"
                surface_file["4x5"] = "release-clm5.0.18/surfdata_4x5_hist_16pfts_Irrig_CMIP6_simyr1850_c190214.nc"
                surface_file["1x1_brazil"] = "release-clm5.0.18/surfdata_1x1_brazil_hist_16pfts_Irrig_CMIP6_simyr1850_c190214.nc"
                surface_file["ne30np4"] = "release-clm5.0.18/surfdata_ne30np4_hist_16pfts_Irrig_CMIP6_simyr1850_c190303.nc"
        elif _opts["sim_year"] == "2000":
            if _nl.clm_inparm.use_crop:
                surface_file["0.9x1.25"] = "release-clm5.0.18/surfdata_0.9x1.25_hist_78pfts_CMIP6_simyr2000_c190214.nc"
                surface_file["1.9x2.5"] = "release-clm5.0.18/surfdata_1.9x2.5_hist_78pfts_CMIP6_simyr2000_c190304.nc"
                surface_file["10x15"] = "release-clm5.0.18/surfdata_10x15_hist_78pfts_CMIP6_simyr2000_c190214.nc"
                surface_file["4x5"] = "release-clm5.0.18/surfdata_4x5_hist_78pfts_CMIP6_simyr2000_c190214.nc"
                surface_file["1x1_numaIA"] = "release-clm5.0.18/surfdata_1x1_numaIA_hist_78pfts_CMIP6_simyr2000_c190214.nc"
                surface_file["1x1_smallvilleIA"] = "release-clm5.0.18/surfdata_1x1_smallvilleIA_hist_78pfts_CMIP6_simyr2000_c190214.nc"
                surface_file["ne30np4"] = "release-clm5.0.18/surfdata_ne30np4_hist_78pfts_CMIP6_simyr2000_c190303.nc"
                surface_file["ne16np4"] = "release-clm5.0.18/surfdata_ne16np4_hist_78pfts_CMIP6_simyr2000_c190214.nc"
            elif not _nl.clm_inparm.use_crop and _nl.clm_inparm.irrigate:
                surface_file["48x96"] = "release-clm5.0.18/surfdata_48x96_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["0.9x1.25"] = "release-clm5.0.18/surfdata_0.9x1.25_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["1.9x2.5"] = "release-clm5.0.18/surfdata_1.9x2.5_hist_16pfts_Irrig_CMIP6_simyr2000_c190304.nc"
                surface_file["4x5"] = "release-clm5.0.18/surfdata_4x5_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["10x15"] = "release-clm5.0.18/surfdata_10x15_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["ne30np4"] = "release-clm5.0.18/surfdata_ne30np4_hist_16pfts_Irrig_CMIP6_simyr2000_c190303.nc"
                surface_file["ne16np4"] = "release-clm5.0.18/surfdata_ne16np4_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["5x5_amazon"] = "release-clm5.0.18/surfdata_5x5_amazon_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"               
                surface_file["1x1_brazil"] = "release-clm5.0.18/surfdata_1x1_brazil_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["64x128"] = "release-clm5.0.18/surfdata_64x128_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["1x1_camdenNJ"] = "release-clm5.0.18/surfdata_1x1_camdenNJ_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["1x1_vancouverCAN"] = "release-clm5.0.18/surfdata_1x1_vancouverCAN_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["1x1_mexicocityMEX"] = "release-clm5.0.18/surfdata_1x1_mexicocityMEX_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
                surface_file["1x1_urbanc_alpha"] = "release-clm5.0.18/surfdata_1x1_urbanc_alpha_hist_16pfts_Irrig_CMIP6_simyr2000_c190214.nc"
        elif _opts["sim_year"] == "2100" and _nl.clm_inparm.use_crop:
            if _opts["ssp_rcp"] == "SSP1-2.6":
                surface_file["0.9x1.25"] = "release-clm5.0.30/surfdata_0.9x1.25_SSP1-2.6_78pfts_CMIP6_simyr2100_c200329.nc"
            elif _opts["ssp_rcp"] == "SSP1-2.6":
                surface_file["0.9x1.25"] = "release-clm5.0.30/surfdata_0.9x1.25_SSP5-8.5_78pfts_CMIP6_simyr2100_c200330.nc"
            elif _opts["ssp_rcp"] == "SSP1-2.6":
                surface_file["0.9x1.25"] = "release-clm5.0.30/surfdata_0.9x1.25_SSP5-3.4_78pfts_CMIP6_simyr2100_c200330.nc"
        elif _opts["sim_year"] == "PtVg" and not _nl.clm_inparm.use_crop and not _nl.clm_inparm.irrigate:
            # Potential vegetation land use dataset, crop is off, and zeroed, all areas are natural vegetation without human disturbance
            surface_file["0.9x1.25"] = "surfdata_0.9x1.25_hist_16pfts_nourb_CMIP6_simyrPtVg_c181114.nc"
        sf = surface_file.get(_opts["res"], None)
        if not sf is None:
            _nl.clm_inparm.fsurdat = "lnd/clm2/surfdata_map/" + sf

def setup_logic_initial_conditions():
    if _opts["clm_start_type"] == "cold":
        if not _user_nl["finidat"] is None:
            print("""
            WARNING: setting finidat (either explicitly in your user_nl_clm or by doing a hybrid or branch RUN_TYPE) is 
            incomptable with using a cold start (by setting CLM_FORCE_COLDSTART=on)
            Overridding input finidat file with one specifying that this is a cold start from arbitrary initial conditions.""")
        _opts["finidat"] = "' '"
    elif not _user_nl["finidat"] is None and _user_nl["finidat"] == "' '":
        error("""You are setting finidat to blank which signals arbitrary initial conditions.
        But, CLM_FORCE_COLDSTART is off which is a contradiction. For arbitrary initial conditions just use the CLM_FORCE_COLDSTART option
        To do a cold-start set ./xmlchange CLM_FORCE_COLDSTART=on, and remove the setting of finidat in the user_nl_clm file""")
    
    if _user_nl["finidat"] is None:
        #TODO
        pass
    else:
        _nl.clm_inparm.finidat = _user_nl["finidat"]

def setup_logic_dynamic_subgrid():
    # Options controlling which parts of flanduse_timeseries to use
    setup_logic_do_transient_pfts()
    setup_logic_do_transient_crops()
    setup_logic_do_harvest()

def setup_logic_do_transient_pfts():
    cannot_be_true = ""
    default_val = True
    if _nl.dynamic_subgrid.flanduse_timeseries is None:
        cannot_be_true = "do_transient_pfts can only be set to true when running a transient case (flanduse_timeseries non-blank)"
    elif _nl.clm_inparm.use_cndv:
        cannot_be_true = "do_transient_pfts cannot be combined with use_cndv"
    elif _nl.clm_inparm.use_fates:
        cannot_be_true = "do_transient_pfts cannot be combined with use_fates"

    if cannot_be_true:
        default_val = False

    if not cannot_be_true:
        _nl.dynamic_subgrid.do_transient_pfts = default_val

    if _nl.dynamic_subgrid.do_transient_pfts and cannot_be_true:
        raise_error(cannot_be_true)

def setup_logic_do_transient_crops():
    cannot_be_true = ""
    default_val = True
    if _nl.dynamic_subgrid.flanduse_timeseries is None:
        cannot_be_true = "do_transient_crops can only be set to true when running a transient case (flanduse_timeseries non-blank)"
    elif _nl.clm_inparm.use_fates:
        cannot_be_true = "do_transient_crops has not been tested with ED, so for now these two options cannot be combined"

    if cannot_be_true:
        default_val = False

    if not cannot_be_true:
        _nl.dynamic_subgrid.do_transient_crops = default_val

    if _nl.dynamic_subgrid.do_transient_pfts and cannot_be_true:
        raise_error(cannot_be_true)

    if ((_nl.dynamic_subgrid.do_transient_crops and not _nl.dynamic_subgrid.do_transient_pfts) or
        (not _nl.dynamic_subgrid.do_transient_crops and _nl.dynamic_subgrid.do_transient_pfts)):
        error("do_transient_crops and do_transient_pfts do NOT agree and need to")

def setup_logic_do_harvest():
    cannot_be_true = ""
    default_val = True
    if _nl.dynamic_subgrid.flanduse_timeseries is None:
        cannot_be_true = "do_harvest can only be set to true when running a transient case (flanduse_timeseries non-blank)"
    elif _nl.clm_inparm.use_cndv:
        cannot_be_true = "do_harvest cannot be combined with use_cndv"
    elif _nl.clm_inparm.use_fates:
        cannot_be_true = "do_harvest cannot be combined with use_fates"

    if cannot_be_true:
        default_val = False

    if not cannot_be_true:
        _nl.dynamic_subgrid.do_harvest = default_val

    if _nl.dynamic_subgrid.do_transient_pfts and cannot_be_true:
        raise_error(cannot_be_true)

def setup_logic_spinup():
    with _nl.clm_inparm as n:
        if _opts["bgc_mode"] == "sp" and n.override_bgc_restart_mismatch_dump:
            error("CN must be on if override_bgc_restart_mismatch_dump is set.")
        if _opts["clm_accelerated_spinup"] == "on":
            n.hist_nhtfrq = 8760
            n.hist_empty_htapes = True
            n.hist_mfilt = 20
            if _nl.clm_inparm.use_fates:
                n.hist_fincl1 = ["TOTSOMC", "TOTSOMN", "TLAI", "GPP", "NPP", "TWS"]
            else:
                if _nl.clm_inparm.use_cn:
                    if _nl.clm_inparm.use_cndv:
                        n.hist_fincl1 = ["TOTECOSYSC", "TOTECOSYSN", "TOTSOMC", "TOTSOMN", "TOTVEGC", "TOTVEGN", "TLAI", "GPP", "NPP", "TWS", "TSAI", "HTOP", "HBOT"]
                    else:
                        n.hist_fincl1 = ["TOTECOSYSC", "TOTECOSYSN", "TOTSOMC", "TOTSOMN", "TOTVEGC", "TOTVEGN", "TLAI", "GPP", "CPOOL", "NPP", "TWS"]
                else:
                    n.hist_fincl1 = ["TLAI" "TWS"]

def setup_logic_supplemental_nitrogen():
    with _nl.clm_inparm as n:
        if not (_opts["bgc_mode"] == "sp" or _opts["bgc_mode"] == "fates") and _nl.clm_inparm.use_crop:
            n.suplnitro = "NONE" if _nl.clm_inparm.use_cn else ""

        if not n.suplnitro is None:
            if _opts["bgc_mode"] == "sp":
                error("supplemental Nitrogen (suplnitro) is set, but neither CN nor CNDV is active!")
            if _nl.clm_inparm.use_crop and n.suplnitro == "PROG_CROP_ONLY":
                error("supplemental Nitrogen is set to run over prognostic crops, but prognostic crop is NOT active")
            if n.suplnitro == "ALL" and _env["bgc_spinup"] == "on":
                print("WARNING: There is no need to use a bgc_spinup mode when supplemental Nitrogen is on for all PFT's, as these modes spinup Nitrogen")

def setup_logic_snowpack():
    _nl.aerosol.fresh_snw_rds_max = 204.526
    with _nl.clm_inparm as n:
        n.nlevsno = 12
        n.h2osno_max = 10000.0
        n.int_snow_max = 2000
        n.n_melt_glcmec = 10.0

    with _nl.clm_snowhydrology_inparm as n:
        n.wind_dependent_snow_density = True
        n.snow_overburden_compaction_method = "Vionnet2012"
        n.lotmp_snowdensity_method = "Slater2017"
        n.upplim_destruct_metamorph = 175.0  
        n.reset_snow = False
        n.reset_snow_glc = False
        n.reset_snow_glc_ela = 1e9

        if n.snow_overburden_compaction_method == "Vionnet2012":
            if not n.overburden_compress_Tfactor is None:
                error("'overburden_compress_tfactor is set, but does not apply when using snow_overburden_compaction_method=Vionnet2012'")
        else:
            n.overburden_compress_Tfactor = 0.08

def setup_logic_fates():
    if _nl.clm_inparm.use_fates:
        with _nl.clm_inparm as n:
            n.fates_paramfile = "lnd/clm2/paramdata/fates_params_api.8.0.0_12pft_c191216.nc"
            n.use_fates_spitfire = False
            n.use_fates_planthydro = False
            n.use_fates_ed_st3 = False
            n.use_fates_ed_prescribed_phys = False
            n.use_fates_inventory_init = False
            n.use_fates_logging = False
            n.fates_parteh_mode = 1
            if not n.use_fates_inventory_init is None and n.use_fates_inventory_init:
                if n.fates_inventory_ctrl_filename is None:
                    error("fates_inventory_ctrl_filename when use_fates_inventory_init is set")
                #elif invalid_file(n.fates_inventory_ctrl_filename):
                #   error("fates_inventory_ctrl_filename does NOT point to a valid filename")
                #

def setup_logic_atm_forcing():
    with _nl.atm2lnd_inparm as n:
        n.glcmec_downscale_longwave = True
        n.repartition_rain_snow = True
        n.lapse_rate = 0.006
        if n.glcmec_downscale_longwave:
            n.lapse_rate_longwave = 0.032
            n.longwave_downscaling_limit = 0.5
        else:
            if not n.lapse_rate_longwave is None or not n.longwave_downscaling_limit is None:
                error("lapse_rate_longwave/longwave_downscaling_limit can only be set if glcmec_downscale_longwave is true")
        if n.repartition_rain_snow:
            n.precip_repartition_glc_all_snow_t = -2.0
            n.precip_repartition_glc_all_rain_t = 0.0
            n.precip_repartition_nonglc_all_snow_t = 0.0
            n.precip_repartition_nonglc_all_rain_t = 2.0
        else:
            if (not n.precip_repartition_glc_all_snow_t is None or
            not n.precip_repartition_glc_all_rain_t is None or
            not n.precip_repartition_nonglc_all_snow_t is None or
            not n.precip_repartition_nonglc_all_rain_t is None):
                error("precip_repartition_glc_all_snow_t/precip_repartition_glc_all_  can only be set if precip_repartition_glc_all_snow_t is true")

def setup_logic_lnd2atm():
    _nl.lnd2atm_inparm.melt_non_icesheet_ice_runoff = True

def setup_logic_humanindex():
    _nl.clm_humanindex_inparm.calc_human_stress_indices = "FAST"

def setup_logic_cnfire():
    with _nl.lifire_inparm as n:
        if _nl.clm_inparm.use_cn:
            if _nl.cnfire_inparm.fire_method == "li2014qianfrc":
                n.rh_low = 30.0
                n.rh_hgh = 80.0
                n.bt_min = 0.3
                n.bt_max = 0.7
                n.cli_scale = 0.035
                n.boreal_peatfire_c = 4.2e-5
                n.non_boreal_peatfire_c = 0.001
                n.pot_hmn_ign_counts_alpha = 0.035
                n.cropfire_a1 = 0.3
                n.occur_hi_gdp_tree = 0.39
                n.lfuel = 75.0
                n.ufuel = 1050.0
                n.cmb_cmplt_fact = [0.5, 0.25]
            elif _nl.cnfire_inparm.fire_method == "li2016crufrc":
                if _opts["lnd_tuning_mode"] == "clm5_0_GSWP3v1" or _opts["lnd_tuning_mode"] == "clm5_0_CRUv7":
                    n.rh_low = 30.0
                    n.pot_hmn_ign_counts_alpha = 0.010
                elif _opts["lnd_tuning_mode"] == "clm5_0_cam6.0":
                    n.rh_low = 20.0
                    n.pot_hmn_ign_counts_alpha = 0.008
                n.rh_hgh = 80.0
                n.bt_min = 0.85
                n.bt_max = 0.98
                n.cli_scale = 0.033
                n.boreal_peatfire_c = 0.09e-4
                n.non_boreal_peatfire_c = 0.17e-3     
                n.cropfire_a1 = 1.6e-4
                n.occur_hi_gdp_tree = 0.33
                n.lfuel = 105.0
                n.ufuel = 1050.0
                n.cmb_cmplt_fact = [0.5, 0.28]
        else:
            pass

def setup_logic_cnprec():
    if _nl.clm_inparm.use_cn:
        _nl.cnprecision_inparm.ncrit = 1e-9
        _nl.cnprecision_inparm.cnegcrit = -60.0
        _nl.cnprecision_inparm.nnegcrit = -6.0

def setup_logic_urban():
    _nl.clmu_inparm.building_temp_method = 1
    _nl.clmu_inparm.urban_hac = "ON_WASTEHEAT"
    _nl.clmu_inparm.urban_traffic = False

def setup_logic_crop():
    if _nl.clm_inparm.use_crop:
        _nl.crop.baset_mapping = "varytropicsbylat"
        _nl.crop.baset_latvary_slope = 0.4
        _nl.crop.baset_latvary_intercept = 12.0
        _nl.cnphenology.initial_seed_at_planting = 3.0
    else:
        error("Can NOT be set without crop on")

def setup_logic_methane():
    if _nl.clm_inparm.use_lch4:
        _nl.ch4par_in.finundation_method = "TWS_inversion"
        _env["finundation_res"] = "1.9x2.5"
        _nl.ch4finundated.stream_fldfilename_ch4finundated = "lnd/clm2/paramdata/finundated_inversiondata_0.9x1.25_c170706.nc"
        _nl.ch4par_in.use_aereoxid_prog = True
        # TODO: Ch4 namelist checking
        # Unknown nl params:
        #   lake_decomp_fact
        #   pftspecific_rootingprofile
        #   rootprof_exp
    else:
        error("ch4par_in namelist variables were set, but Methane model NOT defined in the configuration (use_lch4)")

def setup_logic_c_isotope():
    with _nl.clm_inparm as n:
        if _env["bgc_spinup"] != "sp" and _env["bgc_spinup"] != "fates":
            if _env["bgc_spinup"] != "bgc":
                if not n.use_c13 is None and n.use_c13:
                    print("WARNING: use_c13 is ONLY scientifically validated with the bgc=BGC configuration")
                if not n.use_c14 is None and n.use_c14:
                    print("WARNING: use_c14 is ONLY scientifically validated with the bgc=BGC configuration")           
            if not n.use_c14 is None:
                if n.use_c14:
                    if n.use_c14_bombspike:
                        atm_c14_filename = {"hist":"lnd/clm2/isotopes/atm_delta_C14_CMIP6_3x1_global_1850-2015_yearly_v2.0_c190528.nc",
                                            "SSP1-1.9":"lnd/clm2/isotopes/atm_delta_C14_CMIP6_SSP119_3x1_global_1850-2100_yearly_c181209.nc",
                                            "SSP1-2.6":"lnd/clm2/isotopes/atm_delta_C14_CMIP6_SSP126_3x1_global_1850-2100_yearly_c181209.nc",
                                            "SSP2-4.5":"lnd/clm2/isotopes/atm_delta_C14_CMIP6_SSP245_3x1_global_1850-2100_yearly_c181209.nc",
                                            "SSP3-7.0":"lnd/clm2/isotopes/atm_delta_C14_CMIP6_SSP3B_3x1_global_1850-2100_yearly_c181209.nc",
                                            "SSP5-3.4":"lnd/clm2/isotopes/atm_delta_C14_CMIP6_SSP534os_3x1_global_1850-2100_yearly_c181209.nc",
                                            "SSP5-8.5":"lnd/clm2/isotopes/atm_delta_C14_CMIP6_SSP5B_3x1_global_1850-2100_yearly_c181209.nc"}
                        n.atm_c14_filename = atm_c14_filename.get(_opts["ssp_rcp"], None)
                else:
                    if not (n.atm_c14_filename is None and n.use_c14_bombspike is None):
                        error("use_c14 is FALSE and use_c14_bombspike or atm_c14_filename set")
            else:
                if not (n.atm_c14_filename is None and n.use_c14_bombspike is None):
                    error("use_c14 NOT set to .true., but use_c14_bompspike/atm_c14_filename defined.")       

            if not n.use_c13 is None:
                if n.use_c13:
                    if not n.use_c13_timeseries is None and n.use_c13_timeseries:
                        atm_c13_filename = {"hist":"lnd/clm2/isotopes/atm_delta_C13_CMIP6_1850-2015_yearly_v2.0_c190528.nc",
                                            "SSP1-1.9":"lnd/clm2/isotopes/atm_delta_C13_CMIP6_SSP119_1850-2100_yearly_c181209.nc",
                                            "SSP1-2.6":"lnd/clm2/isotopes/atm_delta_C13_CMIP6_SSP126_1850-2100_yearly_c181209.nc",
                                            "SSP2-4.5":"lnd/clm2/isotopes/atm_delta_C13_CMIP6_SSP245_1850-2100_yearly_c181209.nc",
                                            "SSP3-7.0":"lnd/clm2/isotopes/atm_delta_C13_CMIP6_SSP3B_1850-2100_yearly_c181209.nc",
                                            "SSP5-3.4":"lnd/clm2/isotopes/atm_delta_C13_CMIP6_SSP534os_1850-2100_yearly_c181209.nc",
                                            "SSP5-8.5":"lnd/clm2/isotopes/atm_delta_C13_CMIP6_SSP5B_1850-2100_yearly_c181209.nc"}
                        n.atm_c13_filename = atm_c13_filename.get(_opts["ssp_rcp"], None)
                else:
                    if not (n.atm_c13_filename is None and n.use_c13_timeseries is None):
                        error("use_c13 is FALSE and use_c13_timeseries or atm_c13_filename set")
            else:
                if not (n.atm_c13_filename is None and n.use_c13_timeseries is None):
                    error("use_c13 NOT set to .true., but use_c13_bompspike/atm_c13_filename defined.")
        else:
            if (not n.use_c13 is None or
                not n.use_c14 is None or
                not n.use_c14_bombspike is None or
                not n.atm_c14_filename is None or
                not n.use_c13_timeseries is None or
                not n.atm_c13_filename is None):
                error("bgc=sp and C isotope  namelist variables were set, both can't be used at the same time")

def setup_logic_nitrogen_deposition():
    with _nl.ndepdyn_nml as n:
        if _opts["bgc_mode"] == "cn" or _opts["bgc_mode"] == "bgc":
            if _nl.clm_inparm.use_cn:
                if _opts["res"] in ["1x1_brazil", "1x1_mexicocityMEX", "1x1_vancouverCAN", "1x1_urbanc_alpha",
                                "1x1_camdenNJ", "1x1_asphaltjungleNJ", "5x5_amazon"]:
                    n.ndepmapalgo = "nn"
                else:
                    n.ndepmapalgo = "bilinear"
                n.ndep_taxmode = "cycle"
                n.ndep_varlist = "NDEP_month"
                if _opts["sim_year_range"] == "1850-2100":
                    n.stream_year_first_ndep = 2015
                    n.stream_year_last_ndep = 2101
                    n.model_year_align_ndep = 2015
                elif _opts["sim_year_range"] == "2100-2300":
                    n.stream_year_first_ndep = 2101
                    n.stream_year_last_ndep = 2101
                    n.model_year_align_ndep = 2101
                elif _opts["sim_year"] in ["1850", "2000", "2010"]:
                    n.stream_year_first_ndep = int(_opts["sim_year"])
                    n.stream_year_last_ndep = int(_opts["sim_year"])
                elif _opts["sim_year"] == "1000":
                    n.stream_year_first_ndep = 2000
                    n.stream_year_last_ndep = 2000
                elif (_opts["sim_year"] == "constant" and 
                      (_opts["sim_year_range"] == "1000-1002" or _opts["sim_year_range"] == "1000-1004")):
                    n.stream_year_first_ndep = 2000
                    n.stream_year_last_ndep = 2000
                stream_fldfilename_ndep = {"hist":"lnd/clm2/ndepdata/fndep_clm_hist_b.e21.BWHIST.f09_g17.CMIP6-historical-WACCM.ensmean_1849-2015_monthly_0.9x1.25_c180926.nc",
                                           "SSP5-8.5":"lnd/clm2/ndepdata/fndep_clm_f09_g17.CMIP6-SSP5-8.5-WACCM_1849-2101_monthly_c191007.nc",
                                           "SSP1-2.6":"lnd/clm2/ndepdata/fndep_clm_f09_g17.CMIP6-SSP1-2.6-WACCM_1849-2101_monthly_c191007.nc",
                                           "SSP2-4.5":"lnd/clm2/ndepdata/fndep_clm_f09_g17.CMIP6-SSP2-4.5-WACCM_1849-2101_monthly_c191007.nc",
                                           "SSP3-7.0":"lnd/clm2/ndepdata/fndep_clm_f09_g17.CMIP6-SSP3-7.0-WACCM_1849-2101_monthly_c191007.nc"}
                n.stream_fldfilename_ndep = stream_fldfilename_ndep.get(_opts["ssp_rcp"], None)
                if n.stream_fldfilename_ndep is None:
                    print("""WARNING: Did NOT find the Nitrogen-deposition forcing file (stream_fldfilename_ndep) for this ssp_rcp.
                        "One way to get around this is to point to a file for another existing ssp_rcp in your user_nl_clm file.
                        "If you are running with CAM and WACCM chemistry Nitrogen deposition will come through the coupler.
                        "This file won't be used, so it doesn't matter what it points to -- but it's required to point to something.""")
        else:
            if (not n.stream_year_first_ndep is None or
                not n.stream_year_last_ndep is None or
                not n.model_year_align_ndep is None or
                not n.ndep_taxmode is None or
                not n.ndep_varlist is None or
                not n.stream_fldfilename_ndep is None):
                error("""When bgc is NOT CN or CNDV none of: stream_year_first_ndep,
                                stream_year_last_ndep, model_year_align_ndep, ndep_taxmod,
                                ndep_varlist, nor stream_fldfilename_ndep
                                can be set!""")

def setup_logic_soilm_streams():
    _nl.clm_inparm.use_soil_moisture_streams = False
    with _nl.soil_moisture_streams as n:
        if _nl.clm_inparm.use_soil_moisture_streams:     
            n.soilm_tintalgo = "linear"
            n.soilm_offset = 0
            n.stream_year_first_soilm = 1997
            n.stream_year_last_soilm = 1997
            if n.stream_year_first_soilm != n.stream_year_last_soilm:
                n.model_year_align_soilm = 1997
            if _opts["res"] == "0.9x1.25":
                n.stream_fldfilename_soilm = "lnd/clm2/prescribed_data/LFMIP-pdLC-SST.H2OSOI.0.9x1.25.20levsoi.natveg.1980-2014.MONS_climo.c190716.nc"
            if _opts["use_case"] == "transient" and n.soilm_tintalgo == "linear":
                print("""WARNING: For a transient case, soil moisture streams, should NOT use soilm_tintalgo='linear'
                        since vegetated areas could go from missing to not missing or vice versa""")
        else:
            if (not n.stream_year_first_soilm is None or
                not n.model_year_align_soilm is None or
                not n.stream_fldfilename_soilm is None or
                not n.soilm_tintalgo is None or
                not n.soilm_offset is None or
                not n.stream_year_last_soilm is None):
                error("""One of the soilm streams namelist items (stream_year_first_soilm,
                               model_year_align_soilm, stream_fldfilename_soilm, stream_fldfilename_soilm)
                               soilm_tintalgo soilm_offset is defined, but use_soil_moisture_streams option NOT set to true""")

def setup_logic_cnmresp():
    if _opts["bgc_mode"] != "sp":
        if _nl.clm_inparm.use_fun:
            _nl.cnmresp_inparm.br_root = 0.83e-6
    else:
        if not _nl.cnmresp_inparm.br_root is None:
            error("br_root can NOT be set when phys==clm4_0 or bgc_mode==sp!")

def setup_logic_nitrif_params():
    if not _nl.clm_inparm.use_nitrif_denitrif:
        with _nl.nitrif_inparm as n:
            if (not n.k_nitr_max is None or
                not n.denitrif_respiration_coefficient is None or
                not n.denitrif_respiration_exponent is None or
                not n.denitrif_nitrateconc_coefficient is None or
                not n.denitrif_nitrateconc_exponent is None):
                error("nitrif vars are only used when use_nitrif_denitrif is turned on")

def setup_logic_photosyns():
    with _nl.photosyns_inparm as n:
        n.rootstem_acc = False
        n.light_inhibit = True
        n.leafresp_method = 2 if _nl.clm_inparm.use_cn else 0
        n.modifyphoto_and_lmr_forcrop = True
        n.stomatalcond_method = "Medlyn2011" if _nl.clm_inparm.use_hydrstress else "Ball-Berry1987"
        if _nl.clm_inparm.use_cn:
            if n.leafresp_method == 0:
                error("leafresp_method can NOT be set to scaled to vcmax (0) when CN is on!")
        else:
            if n.leafresp_method != 0:
                error("leafresp_method can NOT be set to anything besides scaled to vcmax (0) when bgc_mode==sp!")

def setup_logic_popd_streams():
    with _nl.popd_streams as n:
        if _env["cnfireson"]:
            if _nl.clm_inparm.use_cn:
                if _opts["res"] in ["1x1_brazil", "1x1_mexicocityMEX", "1x1_vancouverCAN", "1x1_urbanc_alpha", 
                               "1x1_camdenNJ", "1x1_asphaltjungleNJ", "5x5_amazon"]:
                    n.popdensmapalgo = "nn"
                else:
                    n.popdensmapalgo = "bilinear"
                if _opts["sim_year_range"] == "1850-2100":
                    n.stream_year_first_popdens = 2015
                    n.stream_year_last_popdens = 2101
                    n.model_year_align_popdens = 2015
                elif _opts["sim_year_range"] == "2100-2300":
                    n.stream_year_first_popdens = 2100
                    n.stream_year_last_popdens = 2100
                    n.model_year_align_popdens = 2100
                elif _opts["sim_year"] in ["1850", "2000", "2010"]:
                    n.stream_year_first_popdens = int(_opts["sim_year"])
                    n.stream_year_last_popdens = int(_opts["sim_year"])
                elif _opts["sim_year"] == "1000":
                    n.stream_year_first_popdens = 2000
                    n.stream_year_last_popdens = 2000
                elif (_opts["sim_year"] == "constant" and 
                        (_opts["sim_year_range"] == "1000-1002" or _opts["sim_year_range"] == "1000-1004")):
                    n.stream_year_first_popdens = 2000
                    n.stream_year_last_popdens = 2000
                stream_fldfilename_popdens = {"SSP1-1.9":"lnd/clm2/firedata/clmforc.Li_2018_SSP1_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2100_c181205.nc",
                                              "SSP1-2.6":"lnd/clm2/firedata/clmforc.Li_2018_SSP1_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2100_c181205.nc",
                                              "SSP2-4.5":"lnd/clm2/firedata/clmforc.Li_2018_SSP2_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2100_c181205.nc",
                                              "SSP3-7.0":"lnd/clm2/firedata/clmforc.Li_2018_SSP3_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2100_c181205.nc",
                                              "SSP4-6.0":"lnd/clm2/firedata/clmforc.Li_2018_SSP4_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2100_c181205.nc",
                                              "SSP4-3.4":"lnd/clm2/firedata/clmforc.Li_2018_SSP4_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2100_c181205.nc",
                                              "SSP5-8.5":"lnd/clm2/firedata/clmforc.Li_2018_SSP5_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2100_c181205.nc",
                                              "SSP5-3.4":"lnd/clm2/firedata/clmforc.Li_2018_SSP5_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2100_c181205.nc"}
                n.stream_fldfilename_popdens = stream_fldfilename_popdens.get(_opts["ssp_rcp"], "lnd/clm2/firedata/clmforc.Li_2017_HYDEv3.2_CMIP6_hdm_0.5x0.5_AVHRR_simyr1850-2016_c180202.nc")
        else:
            if (not n.stream_fldfilename_popdens is None or
                not n.stream_year_last_popdens is None or
                not n.model_year_align_popdens is None or
                not n.popdens_tintalgo is None or
                not n.stream_fldfilename_popdens is None):
                error("""When bgc is SP (NOT CN or BGC) or fire_method==nofire none of: stream_year_first_popdens,
                               stream_year_last_popdens, model_year_align_popdens, popdens_tintalgo nor
                               stream_fldfilename_popdens can be set""")

def setup_logic_urbantv_streams():
    with _nl.urbantv_streams as n:
        n.urbantvmapalgo = "nn"
        if _opts["sim_year_range"] == "1850-2100":
            n.stream_year_first_urbantv = 2015
            n.stream_year_last_urbantv = 2106
            n.model_year_align_urbantv = 2015
        elif _opts["sim_year_range"] == "2100-2300":
            n.stream_year_first_urbantv = 2100
            n.stream_year_last_urbantv = 2106
            n.model_year_align_urbantv = 2100
        elif _opts["sim_year"] in ["1850", "2000"]:
            n.stream_year_first_urbantv = int(_opts["sim_year"])
            n.stream_year_last_urbantv = int(_opts["sim_year"])
        elif _opts["sim_year"] == "1000":
            n.stream_year_first_urbantv = 2000
            n.stream_year_last_urbantv = 2000
        elif (_opts["sim_year"] == "constant" and 
                (_opts["sim_year_range"] == "1000-1002" or _opts["sim_year_range"] == "1000-1004")):
            n.stream_year_first_urbantv = 2000
            n.stream_year_last_urbantv = 2000
        n.stream_fldfilename_urbantv = "lnd/clm2/urbandata/CLM50_tbuildmax_Oleson_2016_0.9x1.25_simyr1849-2106_c160923.nc"

def setup_logic_lightning_streams():
    with _nl.light_streams as n:
        if _env["cnfireson"]:
            if _nl.clm_inparm.use_cn:
                if _opts["res"] in ["1x1_brazil", "1x1_mexicocityMEX", "1x1_vancouverCAN", "1x1_urbanc_alpha", 
                            "1x1_camdenNJ", "1x1_asphaltjungleNJ", "5x5_amazon"]:
                    n.lightngmapalgo = "nn"
                else:
                    n.lightngmapalgo = "bilinear"
                n.stream_year_first_lightng = 1
                n.stream_year_last_lightng = 1
                if _opts["light_res"] == "94x192":
                    n.stream_fldfilename_lightng = "atm/datm7/NASA_LIS/clmforc.Li_2012_climo1995-2011.T62.lnfm_Total_c140423.nc"
                elif _opts["light_res"] == "360x720":
                    n.stream_fldfilename_lightng = "atm/datm7/NASA_LIS/clmforc.Li_2016_climo1995-2013.360x720.lnfm_Total_c160825.nc"
        else:
            if (not n.stream_year_first_lightng is None or
                not n.stream_year_last_lightng is None or
                not n.model_year_align_lightng is None or
                not n.lightng_tintalgo is None or
                not n.stream_fldfilename_lightng is None):
                error("""When bgc is SP (NOT CN or BGC) or fire_method==nofire none of: stream_year_first_lightng,
                               stream_year_last_lightng, model_year_align_lightng, lightng_tintalgo nor
                               stream_fldfilename_lightng can be set!""")

def setup_logic_lai_streams():
    _nl.clm_inparm.use_lai_streams = False
    with _nl.lai_streams as n:
        if _nl.clm_inparm.use_crop and _nl.clm_inparm.use_lai_streams:
            error("turning use_lai_streams on is incompatable with use_crop set to true.")
        if _opts["bgc_mode"] == "sp":
            if _nl.clm_inparm.use_lai_streams:
                if _opts["res"] in ["1x1_brazil", "1x1_mexicocityMEX", "1x1_vancouverCAN", "1x1_urbanc_alpha",
                               "1x1_camdenNJ", "1x1_asphaltjungleNJ", "5x5_amazon"]:
                    n.lai_mapalgo = "nn"
                else:
                    n.lai_mapalgo   = "bilinear"
                n.stream_year_first_lai = 2001
                n.stream_year_last_lai = 2013
                n.model_year_align_lai = 2001
                n.stream_fldfilename_lai = "lnd/clm2/lai_streams/MODISPFTLAI_0.5x0.5_c140711.nc"
        else:
            if (not n.stream_year_first_lai is None or
                not n.stream_year_last_lai is None or
                not n.model_year_align_lai is None or
                not n.lai_tintalgo is None or
                not n.stream_fldfilename_lai is None):
                error("""When bgc is NOT SP none of the following can be set: stream_year_first_lai,\n" .
                  "stream_year_last_lai, model_year_align_lai, lai_tintalgo nor\n" .
                  "stream_fldfilename_lai (eg. don't use this option with BGC,CN,CNDV nor BGDCV""")

def setup_logic_bgc_shared():
    if _opts["bgc_mode"] != "sp":
        _nl.bgc_shared.constrain_stress_deciduous_onset = True
    # FIXME(bja, 201606) the logic around fates / bgc_mode /
    # use_century_decomp is confusing and messed up. This is a hack
    # workaround.
    if _nl.clm_inparm.use_century_decomp:
         _nl.bgc_shared.decomp_depth_efolding = 10.0
         
def setup_logic_soilwater_movement():
    with _nl.soilwater_movement_inparm as n:
        n.soilwater_movement_method = 1
        n.upper_boundary_condition = 1
        if n.soilwater_movement_method == 1:
            if not _nl.clm_inparm.use_bedrock and _opts["vichydro"] == 1:
                n.lower_boundary_condition = 3
            else:
                n.lower_boundary_condition = 2
        elif n.soilwater_movement_method == 0:
            n.lower_boundary_condition = 4
        n.dtmin = 60.0
        n.verySmall = 1e-8
        n.xTolerUpper = 1e-1
        n.xTolerLower = 1e-2
        n.expensive = 42
        n.inexpensive = 1
        n.flux_calculation = 1

def setup_logic_rooting_profile():
    _nl.rooting_profile_inparm.rooting_profile_method_water = 1
    _nl.rooting_profile_inparm.rooting_profile_method_carbon = 1

def setup_logic_friction_vel():
    _nl.friction_velocity.zetamaxstable = 0.5

def setup_logic_century_soilbgcdecompcascade():
    with _nl.clm_inparm as n:
        if n.use_century_decomp:
            if (n.use_cn and not n.use_fates) or (not n.use_cn and n.use_fates):
                _nl.century_soilbgcdecompcascade.initial_Cstocks = [200.0, 200.0, 200.0]
                _nl.century_soilbgcdecompcascade.initial_Cstocks_depth = [1.50]         

def setup_logic_cngeneral():
    with _nl.clm_inparm as n:
        if n.use_cn:
            if n.use_crop:
                _nl.cn_general.dribble_crophrv_xsmrpool_2atm = True if n.co2_type == "prognostic" else False
            else:
                if not _nl.cn_general.dribble_crophrv_xsmrpool_2atm is None:
                    error("When CROP is NOT on dribble_crophrv_xsmrpool_2atm can NOT be set")
        else:
            if (not _nl.cn_general.reseed_dead_plants is None or
                not _nl.cn_general.dribble_crophrv_xsmrpool_2atm is None):
                error("""When CN is not on none of the following can be set: ,
                               dribble_crophrv_xsmrpool_2atm nor reseed_dead_plantsr
                               (eg. don't use these options with SP mode)""")

def setup_logic_cnvegcarbonstate():
    if _nl.clm_inparm.use_cn:
        if _nl.clm_nitrogen.MM_Nuptake_opt is None:
            _nl.clm_nitrogen.MM_Nuptake_opt = False
        _nl.cnvegcarbonstate.initial_vegC = 100.0 if _nl.clm_nitrogen.MM_Nuptake_opt else 1.0
    
def setup_logic_soil_resis():
    _nl.soil_resis_inparm.soil_resis_method = 1

def setup_logic_canopyfluxes():
    _nl.canopyfluxes_inparm.use_undercanopy_stability = False

def setup_logic_canopyhydrology():
    _nl.clm_canopyhydrology_inparm.interception_fraction = 1.0
    _nl.clm_canopyhydrology_inparm.maximum_leaf_wetted_fraction = 0.05
    _nl.clm_canopyhydrology_inparm.use_clm5_fpi = True

def setup_logic_canopy():
    _nl.clm_canopy_inparm.leaf_mr_vcm = 0.015

def setup_logic_hydrology_params():
    lbc = _nl.soilwater_movement_inparm.lower_boundary_condition
    with _nl.soilhydrology_inparm as n:
        if lbc == 1 or lbc == 2:
            n.baseflow_scalar = 0.01 if lbc == 1 else 0.001
        if not n.baseflow_scalar is None and not (lbc == 1 or lbc == 2):
            error("baseflow_scalar is only used for lower_boundary_condition of flux or zero-flux")

def setup_logic_irrigation_parameters():
    with _nl.irrigation_inparm as n:
        n.irrig_min_lai = 0.0
        n.irrig_start_time = 21600
        n.irrig_length = 14400
        n.irrig_target_smp = -3400.0
        n.irrig_depth = 0.6
        n.irrig_threshold_fraction = 1.0
        n.limit_irrigation_if_rof_enabled = False
        if n.limit_irrigation_if_rof_enabled:
            n.irrig_river_volume_threshold = 0.1
        elif not n.irrig_river_volume_threshold is None:
            error("irrig_river_volume_threshold can only be set if limit_irrigation_if_rof_enabled is true")

def setup_logic_hydrology_switches():
    origflag = _nl.clm_soilhydrology_inparm.origflag
    h2osfcflag = _nl.clm_soilhydrology_inparm.h2osfcflag
    if origflag == 1 and _nl.clm_inparm.subgridflag == 1:
        error("if origflag is ON, subgridflag can NOT also be on!")
    if h2osfcflag == 1 and _nl.clm_inparm.subgridflag != 1:
        error("if h2osfcflag is ON, subgridflag can NOT be off!")
    if (not origflag is None or
        not h2osfcflag is None or 
        not _nl.clm_canopyhydrology_inparm.oldfflag is None):
        error("ERROR:: origflag/h2osfcflag/oldfflag is deprecated and can only be used with CLM4.5")
    
    lower = _nl.soilwater_movement_inparm.lower_boundary_condition
    use_vic = _nl.clm_inparm.use_vichydro
    use_bed = _nl.clm_inparm.use_bedrock
    soilmtd = _nl.soilwater_movement_inparm.soilwater_movement_method

    if(not soilmtd is None and not lower is None) and soilmtd == 0 and lower != 4:
        error("If soil water movement method is zeng-decker -- lower_boundary_condition can only be aquifer")

    if(not soilmtd is None and not lower is None) and soilmtd == 1 and lower == 4:
        error("If soil water movement method is adaptive -- lower_boundary_condition can NOT be aquifer")

    if(not use_bed is None and not lower is None) and use_bed and lower != 2:
        error("If use_bedrock is on -- lower_boundary_condition can only be flux")

    if(not use_vic is None and not lower is None) and use_vic and lower != 3 and lower != 4:
        error("If use_vichydro is on -- lower_boundary_condition can only be table or aquifer")

    if(not origflag is None and not use_vic is None) and use_vic and origflag == 1:
        error("If use_vichydro is on -- origflag can NOT be equal to 1")

    if(not h2osfcflag is None and not lower is None) and h2osfcflag == 0 and lower != 4:
        error("If h2osfcflag is 0 lower_boundary_condition can only be aquifer")

def setup_logic_initinterp():
    if _nl.clm_inparm.use_init_interp:
        _nl.clm_initinterp_inparm.init_interp_method = "general"
    elif not _nl.clm_initinterp_inparm.init_interp_method is None:
        error("init_interp_method can only be set if use_init_interp is true")

def setup_cmdl_bgc():
    with _nl.clm_inparm as n:
        if _opts["bgc_mode"] == "cn":
            n.use_cn = True
            n.use_fates = False
            n.use_vertsoilc = False
            n.use_century_decomp = False
            n.use_lch4 = False
            n.use_nitrif_denitrif = False
            n.use_fun = False
        elif _opts["bgc_mode"] == "bgc":
            n.use_cn = True
            n.use_fates = False
            n.use_vertsoilc = True
            n.use_century_decomp = True
            n.use_lch4 = True
            n.use_nitrif_denitrif = True
            n.use_fun = True
        elif _opts["bgc_mode"] == "fates":
            n.use_cn = False
            n.use_fates = True
            n.use_vertsoilc = True
            n.use_century_decomp = True
            n.use_lch4 = False
            n.use_nitrif_denitrif = False
            n.use_fun = False
        elif _opts["bgc_mode"] == "sp":
            n.use_cn = False
            n.use_fates = False
            n.use_vertsoilc = False
            n.use_century_decomp = False
            n.use_lch4 = False
            n.use_nitrif_denitrif = False
            n.use_fun = False
        else:
            error("Unsupported bgc_mode = " + _opts["bgc_mode"])

def setup_cmdl_fire_light_res():
    if _opts["light_res"] == "default":
        if not _nl.clm_inparm.use_cn or _nl.cnfire_inparm.fire_method == "nofire":
            _opts["light_res"] = "none"
        else:
            _opts["light_res"] = "94x192"
    else:
        if _nl.cnfire_inparm.fire_method == "nofire":
            error("light_res used with fire_method='nofire'. light_res can ONLY be used without the nofire option")
        if not _nl.light_streams.stream_fldfilename_lightng is None:
            error("light_res used while also explicitly setting stream_fldfilename_lightng filename which is a contradiction. Use one or the other not both.")
        if not _nl.clm_inparm.use_cn:
            error("light_res used CN is NOT on. light_res can only be used when CN is on (with bgc: cn or bgc)")
        if not _nl.clm_inparm.use_cn and _opts["light_res"] is None:
            error("light_res is set to none, but CN is on (with bgc: cn or bgc) which is a contradiction")
    if _nl.clm_inparm.use_cn:
        _nl.cnfire_inparm.fire_method = "li2016crufrc"
        _env["cnfireson"] = True
    elif _nl.cnfire_inparm.fire_method == "nofire":
        _env["cnfireson"] = False
    else:
        _env["cnfireson"] = False

def setup_cmdl_spinup():
    if _nl.clm_inparm.use_cn:
        if _opts["clm_accelerated_spinup"] == "on":
            _nl.clm_inparm.spinup_state = 2
        else:
            _nl.clm_inparm.spinup_state = 0
        if _nl.clm_inparm.spinup_state != 0:
            _env["bgc_spinup"] = "on"
            if _opts["bgc_mode"] == "sp":
                error("spinup_state is accelerated (=1 or 2) which is for a BGC mode of CN or BGC, but the BGC mode is Satellite Phenology, change one or the other")
            if _opts["clm_accelerated_spinup"] == "off":
                error("spinup_state is accelerated, but clm_accelerated_spinup is off, change one or the other")
    else:
        _env["bgc_spinup"] = "off"

    if _env["bgc_spinup"] == "on" and not _nl.clm_inparm.use_cn and not _nl.clm_inparm.use_fates:
        error("clm_accelerated_spinup can not be on if neither CN nor ED is turned on")
    if _nl.clm_inparm.spinup_state == 0 and _env["bgc_spinup"] == "on":
        error("Namelist spinup_state contradicts the command line option bgc_spinup")
    if _nl.clm_inparm.spinup_state == 1 and _env["bgc_spinup"] == "off":
        error("Namelist spinup_state contradicts the command line option bgc_spinup")

def setup_cmdl_crop():
    if _opts["crop"] == 1 and _opts["bgc_mode"] == "sp":
        error("Cannot turn crop mode on mode bgc=sp")
    _nl.clm_inparm.use_crop = (_opts["crop"] == 1)

def setup_cmdl_dynamic_vegetation():
    if _opts["dynamic_vegetation"] == 1 and _opts["bgc_mode"] == "sp":
        if _opts["bgc_mode"] == "sp":
            error("Cannot turn dynamic_vegetation mode on with bgc=sp")
        else:
            _nl.clm_inparm.use_cndv = True
        
def setup_cmdl_fates_mode():
    with _nl.clm_inparm as n:
        if n.use_crop and _opts["bgc_mode"] == "fates":
            error("Cannot turn fates mode on with crop")
        elif n.use_fates:
            n.use_vertsoilc = True
            n.use_century_decomp = True
            n.use_lch4 = False
        else:
            if (not n.use_fates_spitfire is None or not n.use_fates_planthydro is None or
                not n.use_fates_ed_st3 is None or not n.use_fates_ed_prescribed_phys is None or
                not n.use_fates_inventory_init is None or not n.fates_inventory_ctrl_filename is None or
                not n.use_fates_logging is None or not n.fates_parteh_mode is None):
                error("is being set, but can ONLY be set when -bgc fates option is used.")

if __name__ == "__main__":
    """
    For testing purposes. To run gen_lnd_in.py, 
    directly, execute it via Python script mode:
    
    $ cd <parent folder of clm5nl>
    $ python3 -m clm5nl.generators.gen_lnd_in   
    """

    opts, user_nl = {}, {}
    opts["bgc_mode"] = "bgc"
    opts["clm_accelerated_spinup"] = "off"
    opts["clm_start_type"] = "startup"
    opts["co2_ppmv"] = 367.0 
    opts["co2_type"] = "constant"
    opts["crop"] = 1
    opts["dtime"] = None
    opts["dynamic_vegetation"] = 0
    opts["GLC_TWO_WAY_COUPLING"] = False
    opts["glc_nec"] = 10
    opts["ignore_ic_date"] = False
    opts["ignore_ic_year"] = False
    opts["l_ncpl"] = 48
    opts["light_res"] = "default"
    opts["lnd_frac"] = "/p/scratch/nrw_test_case/domain.lnd.300x300_NRW_300x300_NRW.190619.nc"
    opts["lnd_tuning_mode"] = "clm5_0_CRUv7"
    opts["nrevsn"] = None
    opts["override_nsrest"] = None
    opts["res"] = "UNSET"
    opts["sim_year"] = "2000"
    opts["sim_year_range"] = "constant"
    opts["ssp_rcp"] = "hist"
    opts["use_case"] = None
    opts["use_dynroot"] = False
    opts["use_init_interp"] = True
    opts["vichydro"] = 0
    user_nl["finidat"] = "/p/scratch/nrw_test_case/FSpinup_300x300_NRW.clm2.r.2222-01-01-00000.nc"
    user_nl["fsnowaging"] = "/p/scratch/nrw_test_case/snicar_drdt_bst_fit_60_c070416.nc"
    user_nl["fsnowoptics"] = "/p/scratch/nrw_test_case/snicar_optics_5bnd_c090915.nc"
    user_nl["fsurdat"] = "/p/scratch/nrw_test_case/surfdata_300x300_NRW_hist_78pfts_CMIP6_simyr2000_c190619.nc"
    user_nl["paramfile"] = "/p/scratch/nrw_test_case/clm5_params.c171117.nc"
    build_lnd_in(opts, user_nl, "lnd_in_test")
    print("Successfully generated lnd_in_test")


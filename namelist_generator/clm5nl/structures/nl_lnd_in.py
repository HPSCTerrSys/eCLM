"""
Lnd stdin namelist
"""
from typing import List
from .namelist import Namelist, namelist_group , namelist_item

class lnd_in(Namelist):

    @namelist_group
    class aerosol():

        @namelist_item
        def fresh_snw_rds_max(self) -> float:
            """
            maximum warm (at freezing) fresh snow effective radius [microns]
            """
            pass

    @namelist_group
    class atm2lnd_inparm():

        @namelist_item
        def glcmec_downscale_longwave(self) -> bool:
            """
            If TRUE, downscale longwave radiation over glc_mec landunits.
            This downscaling is conservative.
            """
            pass

        @namelist_item
        def lapse_rate(self) -> float:
            """
            Surface temperature lapse rate (K m-1)
            A positive value means a decrease in temperature with increasing height
            """
            pass

        @namelist_item
        def lapse_rate_longwave(self) -> float:
            """
            Longwave radiation lapse rate (W m-2 m-1)
            A positive value means a decrease in LW radiation with increasing height
            Only relevant if glcmec_downscale_longwave is .true.
            """
            pass

        @namelist_item
        def longwave_downscaling_limit(self) -> float:
            """
            Relative limit for how much longwave downscaling can be done (unitless)
            The pre-normalized, downscaled longwave is restricted to be in the range
            [lwrad*(1-longwave_downscaling_limit), lwrad*(1+longwave_downscaling_limit)]
            This parameter must be in the range [0,1]
            Only relevant if glcmec_downscale_longwave is .true.
            """
            pass

        @namelist_item
        def precip_repartition_glc_all_rain_t(self) -> float:
            """
            Temperature above which all precipitation falls as rain, for glacier columns (deg C)
            Only relevant if repartition_rain_snow is .true.
            """
            pass

        @namelist_item
        def precip_repartition_glc_all_snow_t(self) -> float:
            """
            Temperature below which all precipitation falls as snow, for glacier columns (deg C)
            Only relevant if repartition_rain_snow is .true.
            """
            pass

        @namelist_item
        def precip_repartition_nonglc_all_rain_t(self) -> float:
            """
            Temperature above which all precipitation falls as rain, for non-glacier columns (deg C)
            Only relevant if repartition_rain_snow is .true.
            """
            pass

        @namelist_item
        def precip_repartition_nonglc_all_snow_t(self) -> float:
            """
            Temperature below which all precipitation falls as snow, for non-glacier columns (deg C)
            Only relevant if repartition_rain_snow is .true.
            """
            pass

        @namelist_item
        def repartition_rain_snow(self) -> bool:
            """
            If TRUE, repartition rain/snow from atmosphere based on temperature.
            """
            pass

    @namelist_group
    class bgc_shared():

        @namelist_item
        def constrain_stress_deciduous_onset(self) -> bool:
            """
            If TRUE use additional stress deciduous onset trigger
            """
            pass

        @namelist_item
        def decomp_depth_efolding(self) -> float:
            """
            E-folding depth over which decomposition is slowed with depth in all soils.
            """
            pass

    @namelist_group
    class canopyfluxes_inparm():

        @namelist_item
        def use_undercanopy_stability(self) -> bool:
            """
            If TRUE use the undercanopy stability term used with CLM4.5 (Sakaguchi & Zeng, 2008)
            """
            pass
        
    @namelist_group
    class century_soilbgcdecompcascade():

        @namelist_item
        def initial_Cstocks(self) -> List[float]:
            """
            Initial stocks of Carbon to use in soil organic matter pools for CENTURY decomposition
            """
            pass

        @namelist_item
        def initial_Cstocks_depth(self) -> List[float]:
            """
            Soil depth to place initial stocks of Carbon in soil organic matter pools for CENTURY decomposition
            """
            pass

    @namelist_group
    class ch4par_in():

        @namelist_item
        def allowlakeprod(self) -> bool:
            """
            If TRUE, turn on methane biogeochemistry model for lake columns, 
            using a simplified version of the CH4 submodel. (EXPERIMENTAL)
            """
            pass

        @namelist_item
        def finundation_method(self) -> str:
            """
            Inundated fraction method type to use for the CH4 submodel (possibly affecting soil 
            heterotrophic respiration and denitrification depending on the configuration),

            h2osfc ----------- Use prognostic saturated fraction h2osfc value calculated in Soil Hydrology
            ZWT_inversion ---- Use inversion of Prigent Satellite data to model ZWT
            TWS_inversion ---- Use inversion of Prigent Satellite data to model TWS

            Inversion options require additional data on fsurdat or use of stream_fldfilename_ch4finundated files.
            (h2osfc option is EXPERIMENTAL and NOT tested)
            """
            pass

        @namelist_item
        def use_aereoxid_prog(self) -> bool:
            """
            Allows user to tune the value of aereoxid.  If set to FALSE, then use the value of aereoxid from 
            the parameter file (set to 0.0, but may be tuned with values in the range {0.0,1.0}.  If set to TRUE,
            then don't fix aere (see ch4Mod.F90).
            """
            pass

    @namelist_group
    class ch4finundated():

        @namelist_item
        def stream_fldfilename_ch4finundated(self) -> str:
            """
            Filename of input stream data for finundated inversion of observed (from Prigent dataset) 
            to hydrologic variables (either TWS or ZWT)
            """
            pass

    @namelist_group
    class clm_canopy_inparm():

        @namelist_item
        def leaf_mr_vcm(self) -> float:
            """
            Scalar of leaf respiration to vcmax
            """
            pass

    @namelist_group
    class clm_canopyhydrology_inparm():

        @namelist_item
        def interception_fraction(self) -> float:
            """
            Fraction of intercepted precipitation
            """
            pass

        @namelist_item
        def maximum_leaf_wetted_fraction(self) -> float:
            """
            Maximum fraction of leaf that may be wet prior to drip occuring
            """
            pass

        @namelist_item
        def oldfflag(self) -> int:
            """
            Use old snow cover fraction from Niu et al. 2007
            (deprecated -- will be removed)
            """
            pass

        @namelist_item
        def snowveg_flag(self) -> str:
            """
            Turn vegetation snow canopy ON, OFF, or ON with albedo influence (ON_RAD)
            """
            pass

        @namelist_item
        def use_clm5_fpi(self) -> str:
            """
            If TRUE use clm5 equation for fraction of intercepted precipitation
            """
            pass

    @namelist_group
    class clm_glacier_behavior():
      
        @namelist_item
        def glacier_region_behavior(self) -> List[str]:
            """
            Behavior of each glacier region (GLACIER_REGION in surface dataset).
            First item corresponds to GLACIER_REGION with ID 0 in the surface dataset,
            second to GLACIER_REGION with ID 1, etc.
            Allowed values are:
              'multiple': grid cells can potentially have multiple glacier elevation defes,
                          but no virtual columns
              'virtual': grid cells have virtual columns: values are computed for every glacier
                         elevation def, even those with 0 area (in order to provide surface mass
                         balance for every glacier elevation def).
              'single_at_atm_topo': glacier landunits in these grid cells have a single column,
                                    whose elevation matches the atmosphere's topographic height (so that there is no
                                    adjustment due to downscaling)
            Behavior of 'virtual' is required in the region where we have an ice sheet model
            """
            pass

        @namelist_item
        def glacier_region_ice_runoff_behavior(self) -> List[str]:
            """
            Treatment of ice runoff for each glacier region (GLACIER_REGION in surface dataset).
            First item corresponds to GLACIER_REGION with ID 0 in the surface dataset,
            second to GLACIER_REGION with ID 1, etc.
            Allowed values are:
              'remains_ice': ice runoff is sent to the river model as ice; this is a crude parameterization
                             of iceberg calving, and so is appropriate in regions where there is substantial 
                             iceberg calving in reality
              'melted': ice runoff generated by the CLM physics (primarily due to snow capping) is melted
                        (generating a negative sensible heat flux) and runs off as liquid; this is appropriate in
                        regions that have little iceberg calving in reality. This can be important to avoid unrealistic
                        cooling of the ocean and consequent runaway sea ice growth.
                        Only applies when melt_non_icesheet_ice_runoff is .true.
            """
            pass

        @namelist_item
        def glacier_region_melt_behavior(self) -> List[str]:
            """
            Treatment of ice melt for each glacier region (GLACIER_REGION in surface dataset).
            First item corresponds to GLACIER_REGION with ID 0 in the surface dataset,
            second to GLACIER_REGION with ID 1, etc.
            Allowed values are:
              'replaced_by_ice': any melted ice runs off and is immediately replaced by solid ice;
                                 this results in positive liquid runoff and negative ice runoff
              'remains_in_place': any melted ice remains in place as liquid until it refreezes;
                                  thus, ice melt does not result in any runoff        
            IMPORTANT NOTE: Regions with the 'remains_in_place' behavior also do not
            compute SMB (because negative SMB would be pretty much meaningless in
            those regions). Thus, you cannot use this behavior where GLC is
            operating.
            Regions with the 'replaced_by_ice' behavior also compute SMB for the
            vegetated column.
            """
            pass

        @namelist_item
        def glacier_region_rain_to_snow_behavior(self) -> List[str]:
            """
            When rain-snow repartitioning / downscaling results in rain being converted to
            snow, the behavior of the resulting additional snow.
            First item corresponds to GLACIER_REGION with ID 0 in the surface dataset,
            second to GLACIER_REGION with ID 1, etc.
            Allowed values are:
              'converted_to_snow': rain is converted to snow, with a corresponding sensible
                                   heat flux correction
              'runs_off': rather than being converted to snow, the excess rain runs off immediately
              
              IMPORTANT NOTE: Unlike other glacier_region*behavior namelist options, this
              option applies to all landunit types in the given regions.
              Only applies when repartition_rain_snow is .true.
            """
            pass

    @namelist_group
    class clm_humanindex_inparm():

        @namelist_item
        def calc_human_stress_indices(self) -> str:
            """
            Human heat stress indices:
            ALL  = All indices will be calculated
            FAST = A subset of indices will be calculated (will not include the computationally 
                expensive wet bulb calculation and associated indices)
            NONE = No indices will be calculated
            """
            pass

    @namelist_group
    class clm_initinterp_inparm():

        @namelist_item
        def init_interp_method(self) -> str:
            """
            Method to use for init_interp. Only applies when use_init_interp = .true.

            'general': The general-purpose method that can be used when changing
            grids, configurations, etc. This starts off with subgrid areas taken
            from the surface dataset.

            'use_finidat_areas': This starts off with subgrid areas taken from the
            input finidat file. This is needed to achieve bit-for-bit results in a
            coupled case (where areas in initialization impact initial fields sent
            to the atmosphere) (but using the 'general' method will typically have
            only a very minor impact on results in this case). For this method to
            work, the input finidat file needs to be at the same resolution as the
            current configuration. So this is a less general form of
            init_interp. However, it can be used in cases where the only difference
            is in internal memory allocation. In order to catch possible problems,
            this uses a different algorithm for finding the input point for each
            output point, which ensures that each active output point is associated
            with exactly one input point with the same latitude, longitude and
            type. This method requires (a) the same grid for input and output,
            within roundoff; (b) any non-zero-weight point in the input must have
            memory allocated for it in this grid cell in the output (this will be
            satisfied if the point is non-zero-weight on the surface dataset or if
            it's a point for which we allocate memory even for zero-weight points);
            (c) any active point in the output (based on the surface dataset and
            rules for determining active points) must have a matching point in this
            grid cell in the input. (Note that this generally can NOT be used when
            transitioning from a spinup run to a transient run, because spinup runs
            typically have irrigation off and transient runs have irrigation on, and
            the presence/absence of irrigation affects the subgrid structure; if it
            weren't for that difference, then this option would be useful for this
            use case.)
            """
            pass

    @namelist_group
    class clm_inparm():

        @namelist_item
        def albice(self) -> List[float]:
            """
            Visible and Near-infrared albedo's for glacier ice
            """
            pass

        @namelist_item
        def anoxia(self) -> bool:
            """
            If TRUE, reduce heterotrophic respiration according to available oxygen predicted by CH4 submodel.
            """
            pass

        @namelist_item
        def anoxia_wtsat(self) -> bool:
            """
            If TRUE, weight calculation of oxygen limitation by the inundated fraction and diagnostic saturated column gas
            concentration profile calculated in the CH4 submodel. Only applies if anoxia = TRUE.
            (EXPERIMENTAL AND NOT FUNCTIONAL!)
            (deprecated -- will be removed)
            """
            pass

        @namelist_item
        def atm_c13_filename(self) -> str:
            """
            Filename with time series of atmospheric Delta C13 data, which use CMIP6 format.
            variables in file are "time" and "delta13co2_in_air".  time variable is in format: years since 1850-01-01 0:0:0.0. units are permil.
            """
            pass

        @namelist_item
        def atm_c14_filename(self) -> str:
            """
            Filename with time series of atmospheric Delta C14 data. variables in file are "time" and 
            "Delta14co2_in_air". time variable is in format: years since 1850-01-01 0:0:0.0  units are permil.
            """
            pass

        @namelist_item
        def co2_ppmv(self) -> float:
            """
            Atmospheric CO2 molar ratio (by volume) only used when co2_type==constant (umol/mol)
            (Set by CCSM_CO2_PPMV)
            """
            pass

        @namelist_item
        def co2_type(self) -> str:
            """
            Type of CO2 feedback.
                constant   = use the input co2_ppmv value
                prognostic = use the prognostic value sent from the atmosphere
                diagnostic = use the diagnostic value sent from the atmosphere
            """
            pass

        @namelist_item
        def create_crop_landunit(self) -> bool:
            """
            If TRUE, separate the vegetated landunit into a crop landunit and a natural vegetation landunit
            """
            pass

        @namelist_item
        def dtime(self) -> int:
            """
            Time step (seconds)
            """
            pass

        @namelist_item
        def fates_inventory_ctrl_filename(self) -> str:
            """
            Full pathname to the inventory initialization control file.
            (Required, if use_fates_inventory_init=T)
            """
            pass

        @namelist_item
        def fates_paramfile(self) -> str:
            """
            Full pathname datafile with fates parameters
            """
            pass

        @namelist_item
        def fates_parteh_mode(self) -> int:
            """
            Switch deciding which nutrient model to use in FATES.
            """
            pass

        @namelist_item
        def fatmlndfrc(self) -> str:
            """
            Full pathname of land fraction data file.
            """
            pass

        @namelist_item
        def finidat(self) -> str:
            """
            Full pathname of initial conditions file. If blank CLM will startup from arbitrary initial conditions.
            """
            pass

        @namelist_item
        def fsnowaging(self) -> str:
            """
            SNICAR (SNow, ICe, and Aerosol Radiative model) snow aging data file name
            """
            pass

        @namelist_item
        def fsnowoptics(self) -> str:
            """
            SNICAR (SNow, ICe, and Aerosol Radiative model) optical data file name
            """
            pass

        @namelist_item
        def fsurdat(self) -> str:
            """
            Full pathname of surface data file.
            """
            pass

        @namelist_item
        def glc_do_dynglacier(self) -> bool:
            """
            If TRUE, dynamically change areas and topographic heights over glacier points.
            Only works when running with a non-stub glacier model.
            """
            pass

        @namelist_item
        def glc_snow_persistence_max_days(self) -> int:
            """
            Number of days before one considers the perennially snow-covered point 'land ice'
            (and thus capable of generating a positive surface mass balance for the glacier model).
            This is meant to compensate for the fact that, with small values of h2osno_max,
            the onset of a snow-capped state (and thus conversion to land ice) can occur in an
            unrealistically short amount of time.
            Thus, in general, large values of h2osno_max should have glc_snow_persistence_max_days = 0;
            small values of h2osno_max should have glc_snow_persistence_max_days > 0.
            """
            pass

        @namelist_item
        def h2osno_max(self) -> float:
            """
            Maximum snow depth in mm H2O equivalent. Additional mass gains will be capped when this depth 
            is exceeded.
            Changes in this value should possibly be accompanied by changes in:
            - nlevsno: larger values of h2osno_max should be accompanied by increases in nlevsno
            - glc_snow_persistence_max_days: large values of h2osno_max should generally have
              glc_snow_persistence_max_days = 0; small values of h2osno_max should generally have
              glc_snow_persistence_max_days > 0.
            """
            pass

        @namelist_item
        def hist_empty_htapes(self) -> bool:
            """
            If TRUE, indicates do NOT output any default history fields (requires you to use
            hist_fincl* to set the exact output fields to use)
            """
            pass

        @namelist_item
        def hist_fincl1(self) -> List[str]:
            """
            Fields to add to history tape series  1
            """
            pass

        @namelist_item
        def hist_mfilt(self) -> int:
            """
            Per tape series  maximum number of time samples.
            """
            pass

        @namelist_item
        def hist_nhtfrq(self) -> int:
            """
            Per tape series history write frequency. 
                positive means in time steps
                0=monthly
                negative means hours
                (i.e. 5 means every 24 time-steps and -24 means every day
            """
            pass

        @namelist_item
        def int_snow_max(self) -> int:
            """
            Limit applied to integrated snowfall when determining changes in snow-covered 
            fraction during melt (mm H2O)
            """
            pass

        @namelist_item
        def irrigate(self) -> bool:
            """
            If TRUE, irrigation will be active.
            """
            pass

        @namelist_item
        def maxpatch_glcmec(self) -> int:
            """
            Number of  multiple elevation defes over glacier points.
            """
            pass

        @namelist_item
        def maxpatch_pft(self) -> int:
            """
            Max number of plant functional types in naturally vegetated landunit.
            """
            pass

        @namelist_item
        def n_melt_glcmec(self) -> float:
            """
            SCA shape parameter for glc_mec (glacier multiple elevation def) columns
            For most columns, n_melt is based on the standard deviation of 1km topography in the grid cell;
            but glc_mec columns already account for subgrid topographic variability through their use of
            multiple elevation defes; thus, to avoid double-accounting for topographic variability
            in these columns, we use a fixed value of n_melt.
            """
            pass

        @namelist_item
        def nlevsno(self) -> int:
            """
            Number of snow layers.
            Values less than 5 are mainly useful for testing, and should not be used for science.
            valid_values="3,4,5,6,7,8,9,10,11,12"
            """
            pass

        @namelist_item
        def nrevsn(self) -> str:
            """
            Full pathname of master restart file for a branch run. (only used if RUN_TYPE=branch)
            (Set with RUN_REFCASE and RUN_REFDATE)
            """
            pass

        @namelist_item
        def nsegspc(self) -> int:
            """
            Number of segments per clump for decomposition
            """
            pass

        @namelist_item
        def override_bgc_restart_mismatch_dump(self) -> bool:
            """
            Flag for overriding the crash that should occur if user tries to start the model from a restart file 
            made with a different version of the soil decomposition structure than is currently being used.
            """
            pass

        @namelist_item
        def override_nsrest(self) -> int:
            """
            Override the start type from the driver: it can only be set to 3 meaning branch.
            """
            pass

        @namelist_item
        def paramfile(self) -> str:
            """
            Full pathname datafile with plant function type (PFT) constants combined with
            constants for biogeochem modules
            """
            pass

        @namelist_item
        def run_zero_weight_urban(self) -> bool:
            """
            If TRUE, run all urban landunits everywhere where we have valid urban data.
            This forces memory to be allocated and calculations to be run even for 0-weight urban points.
            This has a substantial impact on memory use and performance, and should only be used
            if you're interested in potential urban behavior globally.
            """
            pass

        @namelist_item
        def soil_layerstruct(self) -> str:
            """
            10SL_3.5m    = standard CLM4 and CLM4.5 version
            23SL_3.5m    = more vertical layers for permafrost simulations 
            49SL_10m     = 49 layer soil column, 10m of soil, 5 bedrock layers
            20SL_8.5m    = 20 layer soil column, 8m of soil, 5 bedrock layers
            """
            pass

        @namelist_item
        def spinup_state(self) -> int:
            """
            Flag for setting the state of the Accelerated decomposition spinup state for the BGC model.  
                0 = normal model behavior; 
                1 = AD spinup (standard)
                2 = AD spinup (accelerated spinup from Ricciuto, doesn't work for CNDV and not implemented for CN soil decomposition)
            Entering and exiting spinup mode occurs automatically by comparing the namelist and restart file values for this variable.
            NOTE: THIS CAN ONLY BE SET TO NON-ZERO WHEN BGC_MODE IS NOT SATELITE PHENOLOGY!
            """
            pass

        @namelist_item
        def subgridflag(self) -> int:
            """
            Subgrid fluxes for snow
            """
            pass

        @namelist_item
        def suplnitro(self) -> str:
            """
            Supplemental Nitrogen mode and for what type of vegetation it's turned on for. 
            In this mode Nitrogen is unlimited rather than prognosed and in general vegetation is 
            over-productive.
                NONE           = No vegetation types get supplemental Nitrogen
                ALL            = Supplemental Nitrogen is active for all vegetation types
            """
            pass

        @namelist_item
        def use_bedrock(self) -> bool:
            """
            If TRUE, use variable soil depth.
            If present on surface dataset, use depth to bedrock information to
            specify spatially variable soil thickness. If not present, use bottom
            of soil column (nlevsoi).
            """
            pass

        @namelist_item
        def use_c13(self) -> bool:
            """
            Enable C13 model
            """
            pass

        @namelist_item
        def use_c13_timeseries(self) -> bool:
            """
            Flag to use the atmospheric time series of C13 concentrations from natural abundance 
            and the Seuss Effect, rather than static values.
            """
            pass

        @namelist_item
        def use_c14(self) -> bool:
            """
            Enable C14 model
            """
            pass

        @namelist_item
        def use_c14_bombspike(self) -> bool:
            """
            Flag to use the atmospheric time series of C14 concentrations from bomb fallout and Seuss effect, 
            rather than natural abundance C14 (nominally set as 10^-12 mol C14 / mol C)
            """
            pass

        @namelist_item
        def use_century_decomp(self) -> bool:
            """
            Use parameters for decomposition from the CENTURY Carbon model
            Requires the CN or FATES model to work (either CN or CNDV).
            """
            pass

        @namelist_item
        def use_cn(self) -> bool:
            """
            CLM Biogeochemistry mode : Carbon Nitrogen model (CN) 
            (or CLM45BGC if phys=clm4_5, vsoilc_centbgc='on', and clm4me='on')
            """
            pass

        @namelist_item
        def use_cndv(self) -> bool:
            """
            CLM Biogeochemistry mode : Carbon Nitrogen with Dynamic Global Vegetation Model (CNDV)
            (or CLM45BGCDV if phys=clm4_5, vsoilc_centbgc='on', and clm4me='on')
            """
            pass

        @namelist_item
        def use_crop(self) -> bool:
            """
            Toggle to turn on the prognostic crop model
            """
            pass

        @namelist_item
        def use_dynroot(self) -> bool:
            """
            Toggle to turn on the dynamic root model
            """
            pass

        @namelist_item
        def use_fates(self) -> bool:
            """
            Toggle to turn on the FATES model (use_fates= '.true.' is EXPERIMENTAL NOT SUPPORTED!)
            """
            pass

        @namelist_item
        def use_fates_ed_prescribed_phys(self) -> bool:
            """
            Toggle to turn on prescribed physiology (only relevant if FATES is being used).
            """
            pass

        @namelist_item
        def use_fates_ed_st3(self) -> bool:
            """
            Toggle to turn on Static Stand Structure Mode (only relevant if FATES is being used).
            (use_fates_ed_st3=".true." is EXPERIMENTAL NOT SUPPORTED! Nor is it Tested!)
            """
            pass

        @namelist_item
        def use_fates_inventory_init(self) -> bool:
            """
            Toggle to turn on inventory initialization to startup FATES (only relevant if FATES is being used).
            (use_fates_inventory_init=".true." is EXPERIMENTAL NOT SUPPORTED! Nor is it Tested!)
            """
            pass

        @namelist_item
        def use_fates_logging(self) -> bool:
            """
            Toggle to turn on the logging module (only relevant if FATES is being used).
            """
            pass

        @namelist_item
        def use_fates_planthydro(self) -> bool:
            """
            Toggle to turn on plant hydraulics (only relevant if FATES is on).
            (use_fates_planthydro=".true." is EXPERIMENTAL NOT SUPPORTED! Nor is it Tested!)
            """
            pass

        @namelist_item
        def use_fates_spitfire(self) -> bool:
            """
            Toggle to turn on spitfire module for modeling fire (only relevant if FATES is being used).
            """
            pass

        @namelist_item
        def use_fertilizer(self) -> bool:
            """
            Toggle to turn on the prognostic fertilizer for crop model
            """
            pass

        @namelist_item
        def use_flexibleCN(self) -> bool:
            """
            Allow the CN ratio to flexibly change with the simulation, rather than being fixed
            """
            pass

        @namelist_item
        def use_fun(self) -> bool:
            """
            Turn the Fixation and Uptate of Nitrogen model version 2 (FUN2.0)
            Requires the CN model to work (either CN or CNDV).
            """
            pass

        @namelist_item
        def use_grainproduct(self) -> bool:
            """
            Toggle to turn on the 1-year grain product pool in the crop model
            """
            pass

        @namelist_item
        def use_hydrstress(self) -> bool:
            """
            Toggle to turn on the plant hydraulic stress model
            """
            pass

        @namelist_item
        def use_init_interp(self) -> bool:
            """
            If set to .true., interpinic will be called to interpolate the file given by finidat,
            creating the output file specified by finidat_interp_dest. 
            This requires that finidat be non-blank.
            """
            pass

        @namelist_item
        def use_lai_streams(self) -> bool:
            """
            Toggle to turn on use of LAI streams in place of the LAI on the surface dataset when using Satellite Phenology mode.
            (EXPERIMENTAL and NOT tested)
            """
            pass

        @namelist_item
        def use_lch4(self) -> bool:
            """
            Turn on methane model. Standard part of CLM45BGC model.
            """
            pass

        @namelist_item
        def use_luna(self) -> bool:
            """
            Toggle to turn on the LUNA model, to effect Photosynthesis by leaf Nitrogen
            LUNA operates on C3 and non-crop vegetation (see vcmax_opt for how other veg is handled)
            LUNA: Leaf Utilization of Nitrogen for Assimilation
            """
            pass

        @namelist_item
        def use_mexicocity(self) -> bool:
            """
            Toggle for mexico city specific logic.
            """
            pass

        @namelist_item
        def use_nguardrail(self) -> bool:
            """
            Apply the guardrail for leaf-Nitrogen that ensures it doesn't go negative or too small
            """
            pass

        @namelist_item
        def use_nitrif_denitrif(self) -> bool:
            """
            Nitrification/denitrification splits the prognostic mineral N pool into two 
            mineral N pools: NO3 and NH4, and includes the transformations between them.
            Requires the CN model to work (either CN or CNDV).
            """
            pass

        @namelist_item
        def use_soil_moisture_streams(self) -> bool:
            """
            Toggle to turn on use of input prescribed soil moisture streams rather than have CLM prognose it (EXPERIMENTAL)
            """
            pass

        @namelist_item
        def use_vancouver(self) -> bool:
            """
            Toggle for vancouver specific logic.
            """
            pass

        @namelist_item
        def use_vertsoilc(self) -> bool:
            """
            Turn on vertical soil carbon.
            Requires the CN or FATES model to work (either CN or CNDV).
            """
            pass

        @namelist_item
        def use_vichydro(self) -> bool:
            """
            Toggle to turn on the VIC hydrologic parameterizations
            (vichydro=".true." is EXPERIMENTAL NOT SUPPORTED!)
            """
            pass

    @namelist_group
    class clm_nitrogen():

        @namelist_item
        def carbon_resp_opt(self) -> int:
            """
            Carbon respiration option to burn off carbon when CN ratio is too high; do NOT use when FUN is on (EXPERIMENTAL and NOT tested)
            """
            pass

        @namelist_item
        def CN_evergreen_phenology_opt(self) -> int:
            """
            Evergreen phenology option for CNPhenology (EXPERIMENTAL and NOT tested)
            """
            pass

        @namelist_item
        def CN_partition_opt(self) -> int:
            """
            Partition option for flexible-CN (EXPERIMENTAL and NOT tested)
                CN_partition_opt = 1 
            """
            pass

        @namelist_item
        def CN_residual_opt(self) -> int:
            """
            Residual option for flexible-CN (EXPERIMENTAL and NOT tested)
            """
            pass

        @namelist_item
        def CNratio_floating(self) -> bool:
            """
            Flexible CN ratio used for Phenology (EXPERIMENTAL and NOT tested)
            """
            pass

        @namelist_item
        def downreg_opt(self) -> bool:
            """
            GPP downregulation for use_flexibleCN option (EXPERIMENTAL and NOT tested)
            """
            pass

        @namelist_item
        def lnc_opt(self) -> bool:
            """
            How LUNA and Photosynthesis (if needed) will get Leaf nitrogen content
              lnc_opt = true  get from leaf N from CN model
              lnc_opt = false get based on LAI and fixed CN ratio from parameter file
            """
            pass
        
        @namelist_item
        def MM_Nuptake_opt(self) -> bool:
            """
            Michaelis Menten nitrogen uptake kinetics
            """
            pass
        
        @namelist_item
        def nscalar_opt(self) -> bool:
            """
            Michaelis Menten nitrogen limitation for use_flexibleCN option (EXPERIMENTAL and NOT tested)
            """
            pass
        
        @namelist_item
        def plant_ndemand_opt(self) -> int:
            """
            Plant nitrogen demand for use_flexibleCN option (EXPERIMENTAL and NOT tested)
            valid_values="0,1,2,3"
            """
            pass

        @namelist_item
        def reduce_dayl_factor(self) -> bool:
            """
            Reduce day length factor (NOT implemented)
            """
            pass
        
        @namelist_item
        def substrate_term_opt(self) -> bool:
            """
            Michaelis Menten substrate limitation for use_flexibleCN option (EXPERIMENTAL and NOT tested)
            """
            pass

        @namelist_item
        def temp_scalar_opt(self) -> bool:
            """
            Michaelis Menten substrate limitation for use_flexibleCN option (EXPERIMENTAL and NOT tested)
            """
            pass
        
        @namelist_item
        def vcmax_opt(self) -> int:
            """
            Vcmax calculation for Photosynthesis
              vcmax_opt = 4 As for vcmax_opt=0, but using leafN, and exponential if tree  (EXPERIMENTAL NOT TESTED!)
              vcmax_opt = 3 Based on leafN and VCAD (used with Luna for crop and C4 vegetation)
              vcmax_opt = 0 Based on canopy top and foilage Nitrogen limitation factor from params file (clm4.5)
            """
            pass

    @namelist_group
    class clm_snowhydrology_inparm():

        @namelist_item
        def lotmp_snowdensity_method(self) -> str:
            """
            Snow density method to use for low temperatures (below -15C)
            TruncatedAnderson1976 -- Truncate the Anderson-1976 equation at the value for -15C
            Slater2017 ------------- Use equation from Slater that increases snow density for very cold temperatures  (Arctic, Antarctic)
            """
            pass

        @namelist_item
        def overburden_compress_Tfactor(self) -> float:
            """
            Snow compaction overburden exponential factor (1/K)
            Not used for snow_overburden_compaction_method=Vionnet2012
            """
            pass

        @namelist_item
        def reset_snow(self) -> bool:
            """
            If set to .true., then reset the snow pack over non-glacier columns to a small value.
            This is useful when transitioning from a spinup under one set of atmospheric forcings
            to a run under a different set of atmospheric forcings: By resetting too-large snow packs,
            we make it more likely that points will remain only seasonally snow-covered under the new
            atmospheric forcings. (This is particularly true in a coupled run, where starting with a
            too-large snow pack can cool the atmosphere, thus maintaining the too-large snow pack.)

            WARNING: Setting this to .true. will break water conservation for approximately the first
            day of the new run. This is by design: The excess snow is completely removed from the system.
            """
            pass

        @namelist_item
        def reset_snow_glc(self) -> bool:
            """
            If set to .true., then reset the snow pack over glacier columns to a small value.
            This is useful when transitioning from a spinup under one set of atmospheric forcings
            to a run under a different set of atmospheric forcings: By resetting too-large snow packs,
            we make it more likely that points will remain only seasonally snow-covered under the new
            atmospheric forcings. (This is particularly true in a coupled run, where starting with a
            too-large snow pack can cool the atmosphere, thus maintaining the too-large snow pack.)

            See also reset_snow_glc_ela, which controls the elevation below which
            glacier columns are reset.

            WARNING: Setting this to .true. will break water conservation for approximately the first
            day of the new run. This is by design: The excess snow is completely removed from the system.

            WARNING: This variable is intended for short test runs, and generally
            should not be used for scientific production runs. By resetting snow
            below a given elevation, you risk forcing the system to evolve
            differently in areas below and above reset_snow_glc_ela.
            """
            pass

        @namelist_item
        def reset_snow_glc_ela(self) -> float:
            """
            Only relevant if reset_snow_glc is .true.

            When resetting snow pack over glacier columns, one can choose to do this over all glacier
            columns, or only those below a certain elevation. A typical use case is to reset only those 
            columns that have a seasonal snow pack in the real world, i.e. SMB less than 0, also known as 
            the equilibrium line altitude (ELA). This parameter sets a single global ELA value. By
            setting this parameter to a large value (i.e. 10000 m), all glacier columns will be reset.

            WARNING: This variable is intended for short test runs, and generally
            should not be used for scientific production runs. By resetting snow
            below a given elevation, you risk forcing the system to evolve
            differently in areas below and above reset_snow_glc_ela.
            """
            pass

        @namelist_item
        def snow_overburden_compaction_method(self) -> str:
            """
            Method used to compute snow overburden compaction
            Anderson1976 -- older method, default in CLM45
            Vionnet2012 --- newer method, default in CLM50
            """
            pass

        @namelist_item
        def upplim_destruct_metamorph(self) -> float:
            """
            Upper Limit on Destructive Metamorphism Compaction [kg/m3]
            """
            pass

        @namelist_item
        def wind_dependent_snow_density(self) -> float:
            """
            If TRUE, the density of new snow depends on wind speed, and there is also
            wind-dependent snow compaction.
            """
            pass

    @namelist_group
    class clm_soilhydrology_inparm():

        @namelist_item
        def h2osfcflag(self) -> int:
            """
            If surface water is active or not
            (deprecated -- will be removed)
            """
            pass

        @namelist_item
        def origflag(self) -> int:
            """
            Use original CLM4 soil hydraulic properties
            (deprecated -- will be removed)
            """
            pass

    @namelist_group
    class clm_soilstate_inparm():

        @namelist_item
        def organic_frac_squared(self) -> bool:
            """
            If TRUE, square the organic fraction when it's used (as was done in CLM4.5)
            Otherwise use the fraction straight up              (the default for CLM5.0)
            """
            pass

    @namelist_group
    class clmu_inparm():

        @namelist_item
        def building_temp_method(self) -> int:
            """
            0 = simpler method (clm4_5)
            1 = prognostic calculation of interior building temp (clm5_0)
            """
            pass

        @namelist_item
        def urban_hac(self) -> str:
            """
            Turn urban air conditioning/heating ON or OFF and add wasteheat:
                OFF          = Air conditioning/heating is OFF in buildings, internal temperature allowed to float freely
                ON           = Air conditioning/heating is ON in buildings, internal temperature constrained
                ON_WASTEHEAT = Air conditioning/heating is ON and waste-heat sent to urban canyon
            """
            pass

        @namelist_item
        def urban_traffic(self) -> bool:
            """
            If TRUE, urban traffic flux will be activated (Currently NOT implemented).
            """
            pass

    @namelist_group
    class cnmresp_inparm():

        @namelist_item
        def br_root(self) -> float:
            """
            CN Maintenence Respiration base rate for roots
            (if NOT set, use the value for br_mr on the params file)
            """
            pass

    @namelist_group
    class cn_general():

        @namelist_item
        def dribble_crophrv_xsmrpool_2atm(self) -> bool:
            """
            Harvest the XSMR pool at crop harvest time to the atmosphere slowly at an exponential rate
            """
            pass

        @namelist_item
        def reseed_dead_plants(self) -> bool:
            """
            Flag to reseed any dead plants on startup from reading the initial conditions file
            """
            pass

    @namelist_group
    class cnfire_inparm():

        @namelist_item
        def fire_method(self) -> str:
            """
            The method type to use for CNFire

            nofire:        Turn fire effects off
            li2014qianfrc: Reference paper Li, et. al.(2014) tuned with QIAN atmospheric forcing
            li2016crufrc:  Reference paper Li, et. al.(2016) tuned with CRU-NCEP atmospheric forcing
            """
            pass

    @namelist_group
    class cnphenology():

        @namelist_item
        def initial_seed_at_planting(self) -> float:
            """
            Initial seed Carbon to use at planting
            (only used when CN is on as well as crop)
            """
            pass

    @namelist_group
    class cnprecision_inparm():

        @namelist_item
        def ccrit(self) -> float:
            """
            Critical threshold for truncation of Carbon (truncate Carbon states 
            to zero below this value)
            """
            pass

        @namelist_item
        def cnegcrit(self) -> float:
            """
            Critical threshold of negative Carbon to die 
            (abort when Carbon states are below this value)
            """
            pass

        @namelist_item
        def ncrit(self) -> float:
            """
            Critical threshold for truncation of Nitrogen 
            (truncate Nitrogen states to zero below this value)
            """
            pass

        @namelist_item
        def nnegcrit(self) -> float:
            """
            Critical threshold of negative Nitrogen to die 
            (abort when Nitrogen states are below this value)
            """
            pass

    @namelist_group
    class cnvegcarbonstate():

        @namelist_item
        def initial_vegC(self) -> float:
            """
            How much Carbon to initialize vegetation pools (leafc/frootc and storage) 
            to when -- Michaelis Menten nitrogen uptake kinetics is on
            """
            pass
        
    @namelist_group
    class crop():

        @namelist_item
        def baset_latvary_intercept(self) -> float:
            """
            Only used when baset_mapping == varytropicsbylat
            Intercept at zero latitude to add to baset from the PFT parameter file
            """
            pass

        @namelist_item
        def baset_latvary_slope(self) -> float:
            """
            Only used when baset_mapping == varytropicsbylat
            Slope with latitude in degrees to vary tropical baset by
            """
            pass

        @namelist_item
        def baset_mapping(self) -> str:
            """
            Type of mapping to use for base temperature for prognostic crop model
            constant = Just use baset from the PFT parameter file
            varytropicsbylat = Vary the tropics by latitude 
            """
            pass      

    @namelist_group
    class dynamic_subgrid():

        @namelist_item
        def do_harvest(self) -> bool:
            """
            If TRUE, apply harvest from flanduse_timeseries file.
            (Only valid for transient runs, where there is a flanduse_timeseries file.)
            (Also, only valid for use_cn = true.)
            """
            pass

        @namelist_item
        def do_transient_crops(self) -> bool:
            """
            If TRUE, apply transient crops from flanduse_timeseries file.
            (Only valid for transient runs, where there is a flanduse_timeseries file.)
            """
            pass

        @namelist_item
        def do_transient_pfts(self) -> bool:
            """
            If TRUE, apply transient natural PFTs from flanduse_timeseries file.
            (Only valid for transient runs, where there is a flanduse_timeseries file.)
            """
            pass

        @namelist_item
        def flanduse_timeseries(self) -> str:
            """
            Full pathname of time varying landuse data file. This causes the land-use types of
            the initial surface dataset to vary over time.
            """
            pass

    @namelist_group
    class friction_velocity():

        @namelist_item
        def zetamaxstable(self) -> float:
            """
            The maximum value to use for zeta under stable conditions
            """
            pass

    @namelist_group
    class irrigation_inparm():

        @namelist_item
        def irrig_depth(self) -> float:
            """
            Soil depth to which we measure for irrigation (m)
            """
            pass

        @namelist_item
        def irrig_length(self) -> int:
            """
            Desired amount of time to irrigate per day (sec).
            Actual time may differ if this is not a multiple of dtime.
            """
            pass

        @namelist_item
        def irrig_min_lai(self) -> float:
            """
            Minimum leaf area index for irrigation to occur
            """
            pass

        @namelist_item
        def irrig_river_volume_threshold(self) -> float:
            """
            Threshold for river water volume below which irrigation is shut off (as a fraction of available river water), if limit_irrigation_if_rof_enabled is .true.
            A threshold of 0 means allow all river water to be used;
            a threshold of 0.1 means allow 90% of the river volume to be used; etc.
            """
            pass

        @namelist_item
        def irrig_start_time(self) -> int:
            """
            Time of day to check whether we need irrigation, seconds (0 = midnight).
            We start applying the irrigation in the time step FOLLOWING this time.
            """
            pass

        @namelist_item
        def irrig_target_smp(self) -> float:
            """
            Target soil matric potential for irrigation (mm).
            When we irrigate, we aim to bring the total soil moisture in the top (irrig_depth) m of soil up to this level.
            """
            pass

        @namelist_item
        def irrig_threshold_fraction(self) -> float:
            """
            Determines soil moisture threshold at which we irrigate.
            If h2osoi_liq_wilting_point is the soil moisture level at wilting point and
            h2osoi_liq_target is the soil moisture level at the target irrigation level
            (given by irrig_target_smp), then the threshold at which we irrigate is
                h2osoi_liq_wilting_point +
                    irrig_threshold_fraction*(h2osoi_liq_target - h2osoi_liq_wilting_point)
            A value of 1 means that we irrigate whenever soil moisture falls below the target.
            A value of 0 means that we only irrigate when soil moisture falls below the wilting point.
            """
            pass

        @namelist_item
        def limit_irrigation_if_rof_enabled(self) -> bool:
            """
            If TRUE, limit irrigation when river storage drops below a threshold.
            Only applies if using an active runoff (ROF) model; otherwise, river storage-based limitation
            is turned off regardless of the setting of this namelist variable.
            """
            pass

    @namelist_group
    class lai_streams():

        @namelist_item
        def lai_mapalgo(self) -> str:
            """
            Mapping method from LAI input file to the model resolution
                bilinear = bilinear interpolation
                nn       = nearest neighbor
                nnoni    = nearest neighbor on the "i" (longitude) axis
                nnonj    = nearest neighbor on the "j" (latitude) axis
                spval    = set to special value
                copy     = copy using the same indices
            """
            pass

        @namelist_item
        def lai_tintalgo(self) -> str:
            """
            Time interpolation method to use with LAI streams
            """
            pass

        @namelist_item
        def model_year_align_lai(self) -> int:
            """
            Simulation year that aligns with stream_year_first_lai value
            """
            pass  

        @namelist_item
        def stream_fldfilename_lai(self) -> str:
            """
            Filename of input stream data for LAI
            """
            pass

        @namelist_item
        def stream_year_first_lai(self) -> int:
            """
            First year to loop over for LAI data
            """
            pass  

        @namelist_item
        def stream_year_last_lai(self) -> int:
            """
            Last year to loop over for LAI data
            """
            pass  

    @namelist_group
    class lifire_inparm():

        @namelist_item
        def boreal_peatfire_c(self) -> float:
            """
            boreal peat fires (/hr)
            """
            pass

        @namelist_item
        def bt_max(self) -> float:
            """
            Saturation BTRAN for ignition (0-1)
            """
            pass

        @namelist_item
        def bt_min(self) -> float:
            """
            Critical BTRAN for ignition (0-1)
            """
            pass

        @namelist_item
        def cli_scale(self) -> float:
            """
            Global constant for deforestation fires (/day)
            """
            pass

        @namelist_item
        def cmb_cmplt_fact(self) -> List[float]:
            """
            Combustion completeness factor (for litter and CWD[Course Woody Debris]) (unitless)
            """
            pass

        @namelist_item
        def cropfire_a1(self) -> float:
            """
            Scalar for cropfire (/hr)
            """
            pass

        @namelist_item
        def lfuel(self) -> float:
            """
            Lower threshold for fuel mass needed for ignition
            """
            pass

        @namelist_item
        def non_boreal_peatfire_c(self) -> float:
            """
            non-boreal peat fires (/hr)
            """
            pass

        @namelist_item
        def occur_hi_gdp_tree(self) -> float:
            """
            Fire occurance for high GDP areas that are tree dominated (fraction)
            """
            pass

        @namelist_item
        def pot_hmn_ign_counts_alpha(self) -> float:
            """
            Potential human ignition counts (/person/month)
            """
            pass

        @namelist_item
        def rh_hgh(self) -> float:
            """
            Saturation RH for ignition (0-100)
            """
            pass

        @namelist_item
        def rh_low(self) -> float:
            """
            Critical RH for ignition (0-100)
            """
            pass
    
        @namelist_item
        def ufuel(self) -> float:
            """
            Upper threshold for fuel mass needed for ignition
            """
            pass

    @namelist_group
    class light_streams():

        @namelist_item
        def lightng_tintalgo(self) -> str:
            """
            Time interpolation method to use with Lightning streams
            """
            pass

        @namelist_item
        def lightngmapalgo(self) -> str:
            """
            Mapping method from Lightning input file to the model resolution
                bilinear = bilinear interpolation
                nn       = nearest neighbor
                nnoni    = nearest neighbor on the "i" (longitude) axis
                nnonj    = nearest neighbor on the "j" (latitude) axis
                spval    = set to special value
                copy     = copy using the same indices
            """
            pass

        @namelist_item
        def model_year_align_lightng(self) -> int:
            """
            Simulation year that aligns with stream_year_first_lightng value
            """
            pass

        @namelist_item
        def stream_fldfilename_lightng(self) -> str:
            """
            Filename of input stream data for Lightning
            """
            pass

        @namelist_item
        def stream_year_first_lightng(self) -> int:
            """
            First year to loop over for Lightning data
            """
            pass

        @namelist_item
        def stream_year_last_lightng(self) -> int:
            """
            Last year to loop over for Lightning data
            """
            pass

    @namelist_group
    class lnd2atm_inparm():

        @namelist_item
        def melt_non_icesheet_ice_runoff(self) -> bool:
            """
            If TRUE, ice runoff generated from non-glacier columns and glacier columns outside icesheet regions
            is converted to liquid, with an appropriate sensible heat flux.
            That is, the atmosphere (rather than the ocean) melts the ice.
            (Exception: ice runoff generated to ensure conservation with dynamic landunits remains as ice.)
            """
            pass

    @namelist_group
    class luna():

        @namelist_item
        def jmaxb1(self) -> float:
            """
            ???
            """
            pass

    @namelist_group
    class ndepdyn_nml():

        @namelist_item
        def model_year_align_ndep(self) -> int:
            """
            Simulation year that aligns with stream_year_first_ndep value
            """
            pass 

        @namelist_item
        def ndep_taxmode(self) -> str:
            """
            Time interpolation mode to determine how to handle data before and after the times in the file
                cycle   = Always cycle over the data
                extend  = Use the first time before the available data, and use the last time after the available data
                limit   = Only use the data within the times available -- abort if the model tries to go outside it
            """
            pass

        @namelist_item
        def ndep_varlist(self) -> str:
            """
            Colon delimited list of variables to read from the streams file for nitrogen deposition
            (Normally just read the single variable NDEP_year or NDEP_month)
            """
            pass  

        @namelist_item
        def ndepmapalgo(self) -> str:
            """
            Mapping method from Nitrogen deposition input file to the model resolution
            bilinear = bilinear interpolation
            nn       = nearest neighbor
            nnoni    = nearest neighbor on the "i" (longitude) axis
            nnonj    = nearest neighbor on the "j" (latitude) axis
            spval    = set to special value
            copy     = copy using the same indices
            """
            pass

        @namelist_item
        def stream_fldfilename_ndep(self) -> str:
            """
            Filename of input stream data for Nitrogen Deposition
            """
            pass

        @namelist_item
        def stream_year_first_ndep(self) -> int:
            """
            First year to loop over for Nitrogen Deposition data
            """
            pass 

        @namelist_item
        def stream_year_last_ndep(self) -> int:
            """
            Last year to loop over for Nitrogen Deposition data
            """
            pass

    @namelist_group
    class nitrif_inparm():

        @namelist_item
        def denitrif_nitrateconc_coefficient(self) -> float:
            """
            Multiplier for nitrate concentration for max denitrification rates
            (ONLY used if use_nitrif_denitrif is enabled)
            """
            pass

        @namelist_item
        def denitrif_nitrateconc_exponent(self) -> float:
            """
            Exponent power for nitrate concentrationfor max denitrification rates
            (ONLY used if use_nitrif_denitrif is enabled)
            """
            pass

        @namelist_item
        def denitrif_respiration_coefficient(self) -> float:
            """
            Multiplier for heterotrophic respiration for max denitrification rates
            (ONLY used if use_nitrif_denitrif is enabled)
            """
            pass

        @namelist_item
        def denitrif_respiration_exponent(self) -> float:
            """
            Exponent power for heterotrophic respiration for max denitrification rates
            (ONLY used if use_nitrif_denitrif is enabled)
            """
            pass

        @namelist_item
        def k_nitr_max(self) -> float:
            """
            Maximum nitrification rate constant (1/s)
            (ONLY used if use_nitrif_denitrif is enabled)
            """
            pass        

    @namelist_group
    class photosyns_inparm():

        @namelist_item
        def leafresp_method(self) -> int:
            """
            Leaf maintencence respiration for canopy top at 25C method to use

            0  Scaled by vcmax25top
            1  Ryan 1991
            2  Atkin 2015
            """
            pass

        @namelist_item
        def light_inhibit(self) -> bool:
            """
            Switch to inihibit photosynthesis in daytime
            Lloyd et al. 2010, &amp; Metcalfe et al. 2012
            """
            pass  

        @namelist_item
        def modifyphoto_and_lmr_forcrop(self) -> bool:
            """
            Modify photosynthesis and leaf maintence respiration for crop
            """
            pass

        @namelist_item
        def rootstem_acc(self) -> bool:
            """
            Switch to turn on root and stem respiratory acclimation
            Atkin, Fisher et al. (2008) and Lombardozzi et al. (2015)
            """
            pass

        @namelist_item
        def stomatalcond_method(self) -> str:
            """
            Stomatal conductance model method to use

            Ball-Berry1987 --- Ball Berry 1987 methodology
            Medlyn2011 ------- Medlyn 2011 methodology
            """
            pass

    @namelist_group
    class popd_streams():

        @namelist_item
        def model_year_align_popdens(self) -> int:
            """
            Simulation year that aligns with stream_year_first_popdens value
            """
            pass

        @namelist_item
        def popdens_tintalgo(self) -> str:
            """
            Time interpolation method to use with human population density streams
            """
            pass

        @namelist_item
        def popdensmapalgo(self) -> str:
            """
            Mapping method from human population density input file to the model resolution
                bilinear = bilinear interpolation
                nn       = nearest neighbor
                nnoni    = nearest neighbor on the "i" (longitude) axis
                nnonj    = nearest neighbor on the "j" (latitude) axis
                spval    = set to special value
                copy     = copy using the same indices
            """
            pass

        @namelist_item
        def stream_fldfilename_popdens(self) -> int:
            """
            Filename of input stream data for human population density
            """
            pass

        @namelist_item
        def stream_year_first_popdens(self) -> int:
            """
            First year to loop over for human population density data
            """
            pass

        @namelist_item
        def stream_year_last_popdens(self) -> int:
            """
            Last year to loop over for human population density data
            """
            pass

    @namelist_group
    class rooting_profile_inparm():

        @namelist_item
        def rooting_profile_method_carbon(self) -> int:
            """
            Index of rooting profile for carbon

            Changes rooting profile from Zeng 2001 double exponential (0) to
            Jackson 1996 single exponential (1) to Koven uniform exponential (2).
            """
            pass

        @namelist_item
        def rooting_profile_method_water(self) -> int:
            """
            Index of rooting profile for water

            Changes rooting profile from Zeng 2001 double exponential (0) to
            Jackson 1996 single exponential (1) to Koven uniform exponential (2).
            """
            pass

    @namelist_group
    class soil_moisture_streams():

        @namelist_item
        def model_year_align_soilm(self) -> int:
            """
            Simulation year that aligns with stream_year_first_soilm value
            """
            pass

        @namelist_item
        def soilm_offset(self) -> int:
            """
            Offset in time coordinate for soil moisture streams (sec)
            """
            pass

        @namelist_item
        def soilm_tintalgo(self) -> str:
            """
            Time interpolation method to use for prescribed soil moisture streams data
            """
            pass

        @namelist_item
        def stream_fldfilename_soilm(self) -> str:
            """
            Filename of input stream data for prescribed soil moisture streams data
            """
            pass 

        @namelist_item
        def stream_year_first_soilm(self) -> int:
            """
            First year to loop over for prescribed soil moisture streams data
            """
            pass

        @namelist_item
        def stream_year_last_soilm(self) -> str:
            """
            Last year to loop over for prescribed soil moisture streams data
            """
            pass

    @namelist_group
    class soil_resis_inparm():

        @namelist_item
        def soil_resis_method(self) -> int:
            """
            Index of evaporative resistance method.

            Changes soil evaporative resistance method from Sakaguchi and Zeng
            2009 Beta function (0) to Swenson and Lawrence 2014 dry surface layer
            formulation (1).
            """
            pass

    @namelist_group
    class soilhydrology_inparm():

        @namelist_item
        def baseflow_scalar(self) -> float:
            """
            Scalar multiplier for base flow rate
            (ONLY used if lower_boundary_condition is not aquifer or table)
            """
            pass

    @namelist_group
    class soilwater_movement_inparm():

        @namelist_item
        def dtmin(self) -> float:
            """
            minimum time step length (seconds) for adaptive time stepping in richards equation
            """
            pass

        @namelist_item
        def expensive(self) -> int:
            """
            ???
            """
            pass

        @namelist_item
        def flux_calculation(self) -> int:
            """
            ???
            """
            pass

        @namelist_item
        def inexpensive(self) -> int:
            """
            ???
            """
            pass

        @namelist_item
        def lower_boundary_condition(self) -> int:
            """
            Index of lower boundary condition for Richards equation.

            lower_boundary_condition = 1 : flux lower boundary condition                                     (use with soilwater_movement_method=adaptive time stepping)
            lower_boundary_condition = 2 : zero-flux lower boundary condition                                (use with soilwater_movement_method=adaptive time stepping)
            lower_boundary_condition = 3 : water table head-based lower boundary condition w/ aquifer layer. (use with soilwater_movement_method=adaptive time stepping)
            lower_boundary_condition = 4 : 11-layer solution w/ aquifer layer                                (only used with soilwater_movement_method=Zeng&amp;Decker 2009)

            TODO(bja, 2015-09) these should be strings so they have meaningful names instead of ints.
            """
            pass

        @namelist_item
        def soilwater_movement_method(self) -> int:
            """
            Index of solution method of Richards equation.

            Change method for richards equation solution and boundary
            conditions.

            CLM 4.5 - soilwater_movement_method = 0 (Zeng and Decker, 2009, method). 
            CLM 5.0 - soilwater_movement_method = 1 (adaptive time stepping moisture form from Martyn Clark).

            1 (adaptive time stepping moisture form
            """
            pass

        @namelist_item
        def upper_boundary_condition(self) -> int:
            """
            Index of upper boundary condition for Richards equation.
            """
            pass

        @namelist_item
        def verySmall(self) -> float:
            """
            a very small number: used to check for sub step completion for adaptive time stepping in richards equation
            """
            pass

        @namelist_item
        def xTolerLower(self) -> float:
            """
            tolerance to double length of substep for adaptive time stepping in richards equation
            """
            pass

        @namelist_item
        def xTolerUpper(self) -> float:
            """
            tolerance to halve length of substep for adaptive time stepping in richards equation
            """
            pass

    @namelist_group
    class urbantv_streams():

        @namelist_item
        def model_year_align_urbantv(self) -> int:
            """
            Simulation year that aligns with stream_year_first_urbantv value
            """
            pass

        @namelist_item
        def stream_fldfilename_urbantv(self) -> str:
            """
            Filename of input stream data for urban time varying
            """
            pass

        @namelist_item
        def stream_year_first_urbantv(self) -> int:
            """
            First year to loop over for urban time varying data
            """
            pass

        @namelist_item
        def stream_year_last_urbantv(self) -> int:
            """
            Last year to loop over for urban time varying data
            """
            pass

        @namelist_item
        def urbantvmapalgo(self) -> str:
            """
            Mapping method from urban time varying input file to the model resolution
                bilinear = bilinear interpolation
                nn       = nearest neighbor
                nnoni    = nearest neighbor on the "i" (longitude) axis
                nnonj    = nearest neighbor on the "j" (latitude) axis
                spval    = set to special value
                copy     = copy using the same indices
            """
            pass
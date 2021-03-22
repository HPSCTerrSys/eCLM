from typing import List
from .namelist import Namelist, namelist_group , namelist_item

class drv_in(Namelist):

    @namelist_group
    class cime_driver_inst():

        @namelist_item
        def ninst_driver(self) -> int:
            """
            Number of CESM driver instances.  Only used if MULTI_DRIVER is TRUE.
            """
            pass

    @namelist_group
    class cime_pes():

        @namelist_item
        def atm_layout(self) -> str:
            """
            Layout of multi-instance atms (if there are more than 1)
            """
            pass

        @namelist_item
        def atm_ntasks(self) -> int:
            """
            the number of mpi tasks assigned to the atm components.
            set by NTASKS_ATM in env_configure.xml.
            """
            pass

        @namelist_item
        def atm_nthreads(self) -> int:
            """
            the number of threads per mpi task for the atm component.
            set by NTHRDS_ATM in env_configure.xml.
            """
            pass

        @namelist_item
        def atm_pestride(self) -> int:
            """
            the mpi global processors stride associated with the mpi tasks for the atm component.
            set by PSTRID_ATM in env_configure.xml.
            """
            pass

        @namelist_item
        def atm_rootpe(self) -> int:
            """
            the global mpi task rank of the root processor assigned to the atm component.
            set by ROOTPE_ATM in env_configure.xml.
            """
            pass

        @namelist_item
        def cpl_ntasks(self) -> int:
            """
            the number of mpi tasks assigned to the cpl components.
            set by NTASKS_CPL in env_configure.xml.
            """
            pass

        @namelist_item
        def cpl_nthreads(self) -> int:
            """
            the number of threads per mpi task for the cpl component.
            set by NTHRDS_CPL in env_configure.xml.
            """
            pass

        @namelist_item
        def cpl_pestride(self) -> int:
            """
            the mpi global processors stride associated with the mpi tasks for the cpl component.
            set by PSTRID_CPL in env_configure.xml.
            """
            pass

        @namelist_item
        def cpl_rootpe(self) -> int:
            """
            the global mpi task rank of the root processor assigned to the cpl component.
            set by ROOTPE_CPL in env_configure.xml.
            """
            pass

        @namelist_item
        def esp_layout(self) -> str:
            """
            Layout of multi-instance external system processor (if there are more than 1)
            """
            pass

        @namelist_item
        def esp_ntasks(self) -> int:
            """
            the number of mpi tasks assigned to the esp components.
            set by NTASKS_ESP in env_configure.xml.
            """
            pass

        @namelist_item
        def esp_nthreads(self) -> int:
            """
            the number of threads per mpi task for the esp component.
            set by NTHRDS_ESP in env_configure.xml.
            """
            pass

        @namelist_item
        def esp_pestride(self) -> int:
            """
            the mpi global processors stride associated with the mpi tasks for the esp component.
            set by PSTRID_ESP in env_configure.xml.
            """
            pass

        @namelist_item
        def esp_rootpe(self) -> int:
            """
            the global mpi task rank of the root processor assigned to the esp component.
            set by ROOTPE_ESP in env_configure.xml.
            """
            pass

        @namelist_item
        def glc_layout(self) -> str:
            """
            Layout of multi-instance glcs (if there are more than 1)
            """
            pass

        @namelist_item
        def glc_ntasks(self) -> int:
            """
            the number of mpi tasks assigned to the glc components.
            set by NTASKS_GLC in env_configure.xml.
            """
            pass

        @namelist_item
        def glc_nthreads(self) -> int:
            """
            the number of threads per mpi task for the glc component.
            set by NTHRDS_GLC in env_configure.xml.
            """
            pass

        @namelist_item
        def glc_pestride(self) -> int:
            """
            the mpi global processors stride associated with the mpi tasks for the glc component.
            set by PSTRID_GLC in env_configure.xml.
            """
            pass

        @namelist_item
        def glc_rootpe(self) -> int:
            """
            the global mpi task rank of the root processor assigned to the glc component.
            set by ROOTPE_GLC in env_configure.xml.
            """
            pass

        @namelist_item
        def ice_layout(self) -> str:
            """
            Layout of multi-instance ices (if there are more than 1)
            """
            pass

        @namelist_item
        def ice_ntasks(self) -> int:
            """
            the number of mpi tasks assigned to the ice components.
            set by NTASKS_ICE in env_configure.xml.
            """
            pass

        @namelist_item
        def ice_nthreads(self) -> int:
            """
            the number of threads per mpi task for the ice component.
            set by NTHRDS_ICE in env_configure.xml.
            """
            pass

        @namelist_item
        def ice_pestride(self) -> int:
            """
            the mpi global processors stride associated with the mpi tasks for the ice component.
            set by PSTRID_ICE in env_configure.xml.
            """
            pass

        @namelist_item
        def ice_rootpe(self) -> int:
            """
            the global mpi task rank of the root processor assigned to the ice component.
            set by ROOTPE_ICE in env_configure.xml.
            """
            pass

        @namelist_item
        def lnd_layout(self) -> str:
            """
            Layout of multi-instance lnds (if there are more than 1)
            """
            pass

        @namelist_item
        def lnd_ntasks(self) -> int:
            """
            the number of mpi tasks assigned to the lnd components.
            set by NTASKS_LND in env_configure.xml.
            """
            pass

        @namelist_item
        def lnd_nthreads(self) -> int:
            """
            the number of threads per mpi task for the lnd component.
            set by NTHRDS_LND in env_configure.xml.
            """
            pass

        @namelist_item
        def lnd_pestride(self) -> int:
            """
            the mpi global processors stride associated with the mpi tasks for the lnd component.
            set by PSTRID_LND in env_configure.xml.
            """
            pass

        @namelist_item
        def lnd_rootpe(self) -> int:
            """
            the global mpi task rank of the root processor assigned to the lnd component.
            set by ROOTPE_LND in env_configure.xml.
            """
            pass

        @namelist_item
        def ocn_layout(self) -> str:
            """
            Layout of multi-instance ocns (if there are more than 1)
            """
            pass

        @namelist_item
        def ocn_ntasks(self) -> int:
            """
            the number of mpi tasks assigned to the ocn components.
            set by NTASKS_OCN in env_configure.xml.
            """
            pass

        @namelist_item
        def ocn_nthreads(self) -> int:
            """
            the number of threads per mpi task for the ocn component.
            set by NTHRDS_OCN in env_configure.xml.
            """
            pass

        @namelist_item
        def ocn_pestride(self) -> int:
            """
            the mpi global processors stride associated with the mpi tasks for the ocn component.
            set by PSTRID_OCN in env_configure.xml.  default: 1
            """
            pass

        @namelist_item
        def ocn_rootpe(self) -> int:
            """
            the global mpi task rank of the root processor assigned to the ocn component.
            set by ROOTPE_OCN in env_configure.xml.
            """
            pass

    @namelist_group
    class esmf_inparm():

        @namelist_item
        def esmf_logfile_kind(self) -> str:
            """
            Specify type of ESMF logging: 
            ESMF_LOGKIND_SINGLE, ESMF_LOGKIND_MULTI, ESMF_LOGKIND_MULTI_ON_ERROR, ESMF_LOGKIND_NONE
            """
            pass

    @namelist_group
    class papi_inparm():
        """
        in perf_mod.F90
        """

        @namelist_item
        def papi_ctr1_str(self) -> str:
            """
            See gptl_papi.c for the list of valid values
            """
            pass

        @namelist_item
        def papi_ctr2_str(self) -> str:
            """
            See gptl_papi.c for the list of valid values
            """
            pass

        @namelist_item
        def papi_ctr3_str(self) -> str:
            """
            See gptl_papi.c for the list of valid values
            """
            pass

        @namelist_item
        def papi_ctr4_str(self) -> str:
            """
            See gptl_papi.c for the list of valid values
            """
            pass

    @namelist_group
    class pio_default_inparm():

        @namelist_item
        def pio_async_interface(self) -> bool:
            """
            future asynchronous IO capability (not currently supported).
            If pio_async_interface is .true. or {component}_PIO_* variable is not set or set to -99
            the component variable will be set using the pio_* value.
            default: .false.
            """
            pass


        @namelist_item
        def pio_blocksize(self) -> int:
            """
            blocksize for pio box rearranger
            """
            pass


        @namelist_item
        def pio_buffer_size_limit(self) -> int:
            """
            pio buffer size limit
            """
            pass

        @namelist_item
        def pio_debug_level(self) -> int:
            """
            pio debug level
            valid values: 0,1,2,3,4,5,6
            """
            pass

        @namelist_item
        def pio_rearr_comm_enable_hs_comp2io(self) -> bool:
            """
            pio rearranger communication option: Enable handshake (comp2io)
            """
            pass

        @namelist_item
        def pio_rearr_comm_enable_hs_io2comp(self) -> bool:
            """
            pio rearranger communication option: Enable handshake (io2comp)
            """
            pass

        @namelist_item
        def pio_rearr_comm_enable_isend_comp2io(self) -> bool:
            """
            pio rearranger communication option: Enable isends (comp2io)
            """
            pass

        @namelist_item
        def pio_rearr_comm_enable_isend_io2comp(self) -> bool:
            """
            pio rearranger communication option: Enable isends (io2comp)
            default: .false.
            """
            pass

        @namelist_item
        def pio_rearr_comm_fcd(self) -> str:
            """
            pio rearranger communication flow control direction.
            """
            pass

        @namelist_item
        def pio_rearr_comm_max_pend_req_comp2io(self) -> int:
            """
            pio rearranger communication max pending req (comp2io)
            """
            pass

        @namelist_item
        def pio_rearr_comm_max_pend_req_io2comp(self) -> int:
            """
            pio rearranger communication max pending req (io2comp)
            """
            pass

        @namelist_item
        def pio_rearr_comm_type(self) -> str:
            """
            pio rearranger communication type.
            valid values: p2p, coll, default
            """
            pass
        
    @namelist_group
    class prof_inparm():

        @namelist_item
        def profile_add_detail(self) -> bool:
            """
            default: .false.
            """
            pass

        @namelist_item
        def profile_barrier(self) -> bool:
            """
            
            """
            pass

        @namelist_item
        def profile_depth_limit(self) -> int:
            """
            
            """
            pass

        @namelist_item
        def profile_detail_limit(self) -> int:
            """
            
            """
            pass

        @namelist_item
        def profile_disable(self) -> bool:
            """
            
            """
            pass

        @namelist_item
        def profile_global_stats(self) -> bool:
            """
            
            """
            pass

        @namelist_item
        def profile_outpe_num(self) -> int:
            """
            default: 1
            """
            pass

        @namelist_item
        def profile_outpe_stride(self) -> int:
            """
            
            """
            pass

        @namelist_item
        def profile_ovhd_measurement(self) -> bool:
            """
            default: .false.
            """
            pass

        @namelist_item
        def profile_papi_enable(self) -> bool:
            """
            default: .false.
            """
            pass

        @namelist_item
        def profile_single_file(self) -> bool:
            """
            
            """
            pass

        @namelist_item
        def profile_timer(self) -> bool:
            """
            
            """
            pass

    @namelist_group
    class seq_cplflds_inparm():

        @namelist_item
        def flds_bgc_oi(self) -> bool:
            """
            If set to .true. BGC fields will be passed back and forth between the ocean and seaice
            via the coupler.
            """
            pass

        @namelist_item
        def flds_co2_dmsa(self) -> bool:
            """
            If CCSM_BGC is set to 'CO2_DMSA', then flds_co2_dmsa will be set to .true. by default.
            """
            pass

        @namelist_item
        def flds_co2a(self) -> bool:
            """
            If set to .true., adds prognostic CO2 and diagnostic CO2 at the lowest
            model level to be sent from the atmosphere to the land and ocean.
            If CCSM_BGC is set to 'CO2A', then flds_co2a will be set to .true. by default
            """
            pass

        @namelist_item
        def flds_co2b(self) -> bool:
            """
            If set to .true., adds prognostic CO2 and diagnostic CO2 at the lowest
            model level to be sent from the atmosphere just to the land, and the
            surface upward flux of CO2 to be sent from the land back to the
            atmosphere.
            If CCSM_BGC is set to 'CO2B', then flds_co2b will be set to .true. by default.
            """
            pass

        @namelist_item
        def flds_co2c(self) -> bool:
            """
            If set to .true., adds prognostic CO2 and diagnostic CO2 at the lowest
            model level to be sent from the atmosphere to the land and ocean, and the
            surface upward flux of CO2 to be sent from the land and the open ocean
            back to the atmosphere.
            If CCSM_BGC is set to 'CO2C', then flds_co2c will be set to .true. by default.
            """
            pass

        @namelist_item
        def flds_wiso(self) -> bool:
            """
            Pass water isotopes between components
            """
            pass

        @namelist_item
        def glc_nec(self) -> int:
            """
            Number of cism elevation classes. Set by the xml variable GLC_NEC in env_run.xml
            """
            pass

        @namelist_item
        def ice_ncat(self) -> int:
            """
            Number of sea ice thickness categories. Set by the xml variable ICE_NCAT in env_build.xml
            """
            pass

        @namelist_item
        def nan_check_component_fields(self) -> bool:
            """
            .true. means that all fields passed to coupler are checked for NaN values
            """
            pass

        @namelist_item
        def seq_flds_i2o_per_cat(self) -> bool:
            """
            .true. if select per ice thickness category fields are passed to the ocean.
            Set by the xml variable CPL_I2O_PER_CAT in env_run.xml
            """
            pass

    @namelist_group
    class seq_cplflds_userspec():

        @namelist_item
        def cplflds_custom(self) -> str:
            """
            New fields that are user specified can be added as namelist variables
            by the user in the cpl namelist seq_flds_user using the namelist variable
            array cplflds_customs. The user specified new fields must follow the
            above naming convention.
            As an example, say you want to add a new state 'foo' that is passed
            from the land to the atm - you would do this as follows
            &seq_flds_user
            cplflds_custom = 'Sa_foo->a2x', 'Sa_foo->x2a'
            /
            This would add the field 'Sa_foo' to the character strings defining the
            attribute vectors a2x and x2a. It is assumed that code would need to be
            introduced in the atm and land components to deal with this new attribute
            vector field.
            Modify user_nl_cpl to edit this.
            """
            pass

    @namelist_group
    class seq_flux_mct_inparm():

        @namelist_item
        def seq_flux_atmocn_minwind(self) -> int:
            """
            minimum wind speed for atmOcn flux calculations
            """
            pass

        @namelist_item
        def seq_flux_mct_albdif(self) -> int:
            """
            Surface albedo for diffuse radiation
            """
            pass

        @namelist_item
        def seq_flux_mct_albdir(self) -> int:
            """
            Surface albedo for direct radiation
            """
            pass

    @namelist_group
    class seq_infodata_inparm():

        @namelist_item
        def aoflux_grid(self) -> str:
            """
            Grid for atm ocn flux calc (untested)
            default: ocn
            """
            pass

        @namelist_item
        def aqua_planet(self) -> bool:
            """
            true => turn on aquaplanet mode in cam
            """
            pass

        @namelist_item
        def aqua_planet_sst(self) -> int:
            """
            1 => default sst mode for aquaplanet in cam
            """
            pass

        @namelist_item
        def atm_gnam(self) -> str:
            """
            ATM_GRID values passed into driver.
            """
            pass

        @namelist_item
        def bfbflag(self) -> bool:
            """
            turns on bfb option in coupler which produce bfb results in the
            coupler on different processor counts.  (default: .false.)
            """
            pass

        @namelist_item
        def brnch_retain_casename(self) -> bool:
            """
            Allow same branch casename as reference casename. If $CASE and $REFCASE are the same and the start_type is
            not startup, then the value of brnch_retain_casename is set to .true.
            """
            pass

        @namelist_item
        def budget_ann(self) -> int:
            """
            sets the diagnotics level of the annual budgets. [0,1,2,3],
            written only if do_budgets variable is .true.,
            0=none,
            1=+net summary budgets,
            2=+detailed lnd/ocn/ice component budgets,
            3=+detailed atm budgets
            default: 1
            """
            pass

        @namelist_item
        def budget_daily(self) -> int:
            """
            sets the diagnotics level of the daily budgets. [0,1,2,3],
            written only if do_budgets variable is .true.,
            0=none,
            1=+net summary budgets,
            2=+detailed lnd/ocn/ice component budgets,
            3=+detailed atm budgets
            default: 0
            """
            pass

        @namelist_item
        def budget_inst(self) -> int:
            """
            sets the diagnotics level of the instantaneous budgets. [0,1,2,3],
            written only if BUDGETS variable is true
            0=none,
            1=+net summary budgets,
            2=+detailed lnd/ocn/ice component budgets,
            3=+detailed atm budgets
            default: 0
            """
            pass

        @namelist_item
        def budget_ltann(self) -> int:
            """
            sets the diagnotics level of the longterm budgets written at the end
            of the year. [0,1,2,3],
            written only if do_budgets variable is .true.,
            0=none,
            1=+net summary budgets,
            2=+detailed lnd/ocn/ice component budgets,
            3=+detailed atm budgets,
            default: 1
            """
            pass

        @namelist_item
        def budget_ltend(self) -> int:
            """
            sets the diagnotics level of the longterm budgets written at the end
            of each run. [0,1,2,3],
            written only if do_budgets variable is .true.,
            0=none,
            1=+net summary budgets,
            2=+detailed lnd/ocn/ice component budgets,
            3=+detailed atm budgets,
            default: 0
            """
            pass

        @namelist_item
        def budget_month(self) -> int:
            """
            sets the diagnotics level of the monthy budgets. [0,1,2,3],
            written only if do_budgets variable is .true.,
            0=none,
            1=+net summary budgets,
            2=+detailed lnd/ocn/ice component budgets,
            3=+detailed atm budgets
            default: 1
            """
            pass

        @namelist_item
        def case_desc(self) -> str:
            """
            case description.
            """
            pass

        @namelist_item
        def case_name(self) -> str:
            """
            case name.
            """
            pass

        @namelist_item
        def cime_model(self) -> str:
            """
            cime model - e3sm or cesm
            """
            pass

        @namelist_item
        def coldair_outbreak_mod(self) -> bool:
            """
            if true use  Mahrt and Sun 1995,MWR modification to surface flux calculation
            """
            pass

        @namelist_item
        def cpl_decomp(self) -> int:
            """
            cpl decomp option (0=default, 1=comp decomp, 2=rearr comp decomp, 3=new single 1d seg
            default: 0
            """
            pass

        @namelist_item
        def cpl_seq_option(self) -> str:
            """
            Set the coupler sequencing.
            """
            pass

        @namelist_item
        def do_budgets(self) -> bool:
            """
            logical that turns on diagnostic budgets, false means budgets will never be written
            """
            pass

        @namelist_item
        def do_histinit(self) -> bool:
            """
            logical to write an extra initial coupler history file
            """
            pass

        @namelist_item
        def drv_threading(self) -> bool:
            """
            turn on run time control of threading per pe per component by the driver
            default: false
            """
            pass

        @namelist_item
        def eps_aarea(self) -> float:
            """
            Error tolerance for differences in atm/land areas in domain checking
            default: 1.0e-07
            """
            pass

        @namelist_item
        def eps_agrid(self) -> float:
            """
            Error tolerance for differences in atm/land lat/lon in domain checking
            default: 1.0e-12
            """
            pass

        @namelist_item
        def eps_amask(self) -> float:
            """
            Error tolerance for differences in atm/land masks in domain checking
            default: 1.0e-13
            """
            pass

        @namelist_item
        def eps_frac(self) -> float:
            """
            Error tolerance for differences in fractions in domain checking
            default: 1.0e-02
            """
            pass

        @namelist_item
        def eps_oarea(self) -> float:
            """
            Error tolerance for differences in ocean/ice lon/lat in domain checking
            default: 1.0e-1
            """
            pass

        @namelist_item
        def eps_ogrid(self) -> float:
            """
            Error tolerance for differences in ocean/ice lon/lat in domain checking
            default: 1.0e-2
            """
            pass

        @namelist_item
        def eps_omask(self) -> float:
            """
            Error tolerance for differences in ocean/ice masks in domain checking
            default: 1.0e-06
            """
            pass

        @namelist_item
        def flux_albav(self) -> bool:
            """
            Only used for C,G compsets: if true, compute albedos to work with daily avg SW down
            """
            pass

        @namelist_item
        def flux_convergence(self) -> float:
            """
            Iterate atmocn flux calculation to this % difference
            Setting this to zero will always do flux_max_iteration
            """
            pass

        @namelist_item
        def flux_diurnal(self) -> bool:
            """
            If true, turn on diurnal cycle in computing atm/ocn fluxes
            default: false
            """
            pass

        @namelist_item
        def flux_epbal(self) -> str:
            """
            Only used for C,G compsets: if ocn, ocn provides EP balance factor for precip
            """
            pass

        @namelist_item
        def flux_max_iteration(self) -> int:
            """
            Iterate atmocn flux calculation a max of this value
            """
            pass

        @namelist_item
        def force_stop_at(self) -> str:
            """
            Force stop at the next month, day, etc when wall_time_limit is hit
            default: month
            """
            pass

        @namelist_item
        def glc_gnam(self) -> str:
            """
            GLC_GRID values passed into driver.
            """
            pass

        @namelist_item
        def glc_renormalize_smb(self) -> str:
            """
            Whether to renormalize the surface mass balance (smb) sent from lnd to glc so that the
            global integral on the glc grid agrees with the global integral on the lnd grid.

            Unlike most fluxes, smb is remapped with bilinear rather than conservative mapping weights,
            so this option is needed for conservation. However, conservation is not required in many
            cases, since we often run glc as a diagnostic (one-way-coupled) component.

            Allowable values are:
            'on': always do this renormalization
            'off': never do this renormalization (see WARNING below)
            'on_if_glc_coupled_fluxes': Determine at runtime whether to do this renormalization.
                Does the renormalization if we're running a two-way-coupled glc that sends fluxes
                to other components (which is the case where we need conservation).
                Does NOT do the renormalization if we're running a one-way-coupled glc, or if
                we're running a glc-only compset (T compsets).
                (In these cases, conservation is not important.)

            Only used if running with a prognostic GLC component.

            WARNING: Setting this to 'off' will break conservation when running with an
            evolving, two-way-coupled glc.
            """
            pass

        @namelist_item
        def gust_fac(self) -> float:
            """
            wind gustiness factor
            """
            pass

        @namelist_item
        def histaux_a2x(self) -> bool:
            """
            turns on coupler history stream for instantaneous atm to coupler fields.
            default: false
            """
            pass

        @namelist_item
        def histaux_a2x1hr(self) -> bool:
            """
            turns on coupler history stream for 1-hour average atm to coupler fields.
            default: false
            """
            pass

        @namelist_item
        def histaux_a2x1hri(self) -> bool:
            """
            turns on coupler history stream for 1-hour instantaneous atm to coupler fields.
            default: false
            """
            pass

        @namelist_item
        def histaux_a2x24hr(self) -> bool:
            """
            turns on coupler history stream for daily average atm to coupler fields.
            default: false
            """
            pass

        @namelist_item
        def histaux_a2x3hr(self) -> bool:
            """
            turns on coupler history stream for 3-hour average atm to coupler fields.
            default: false
            """
            pass

        @namelist_item
        def histaux_a2x3hrp(self) -> bool:
            """
            turns on coupler history stream for 3-hour average atm to coupler precip fields.
            default: false
            """
            pass

        @namelist_item
        def histaux_double_precision(self) -> bool:
            """
            if true, use double-precision rather than single-precision for
            coupler auxiliary history files
            default: false
            """
            pass

        @namelist_item
        def histaux_l2x(self) -> bool:
            """
            turns on coupler history stream for instantaneous land to coupler fields.
            default: false
            """
            pass

        @namelist_item
        def histaux_l2x1yrg(self) -> bool:
            """
            turns on coupler history stream for annual lnd to coupler glc forcing fields.
            default: false
            """
            pass

        @namelist_item
        def histaux_r2x(self) -> bool:
            """
            turns on coupler history stream for average* runoff to coupler fields
            (*despite the lack of an averaging time span in the name).
            Files are written at time-of-day = 00000, and at the end of the run interval,
            even if that time is not 00000.
            Run length less than 24 hours; averaging period is the run length,
            Otherwise; averaging period is 24 hours for files before the last (partial) day,
                        averaging period is the last (partial) day for the last file.
            default: false
            """
            pass

        @namelist_item
        def histavg_atm(self) -> bool:
            """
            writes atm fields in coupler average history files.
            default: true
            """
            pass

        @namelist_item
        def histavg_glc(self) -> bool:
            """
            writes glc fields in coupler average history files.
            default: true
            """
            pass

        @namelist_item
        def histavg_ice(self) -> bool:
            """
            writes ice fields in coupler average history files.
            default: true
            """
            pass

        @namelist_item
        def histavg_lnd(self) -> bool:
            """
            writes lnd fields in coupler average history files.
            default: true
            """
            pass

        @namelist_item
        def histavg_ocn(self) -> bool:
            """
            writes ocn fields in coupler average history files.
            default: true
            """
            pass

        @namelist_item
        def histavg_rof(self) -> bool:
            """
            writes rof fields in coupler average history files.
            default: true
            """
            pass

        @namelist_item
        def histavg_wav(self) -> bool:
            """
            writes wav fields in coupler average history files.
            default: true
            """
            pass

        @namelist_item
        def histavg_xao(self) -> bool:
            """
            writes xao fields in coupler average history files.
            default: true
            """
            pass

        @namelist_item
        def hostname(self) -> str:
            """
            hostname information
            """
            pass

        @namelist_item
        def ice_gnam(self) -> str:
            """
            ICE_GRID values passed into driver.
            """
            pass

        @namelist_item
        def info_debug(self) -> int:
            """
            Level of debug output, 0=minimum, 1=normal, 2=more, 3=too much (default: 1)
            """
            pass

        @namelist_item
        def lnd_gnam(self) -> str:
            """
            LND_GRID values passed into driver.
            """
            pass

        @namelist_item
        def logfilepostfix(self) -> str:
            """
            Ending suffix "postfix" for output log files.
            """
            pass

        @namelist_item
        def max_cplstep_time(self) -> float:
            """
            Abort model if coupler timestep wallclock time exceeds this value, ignored if 0,
            if < 0 then use abs(max_cplstep_time)*cktime as the threshold.
            """
            pass

        @namelist_item
        def mct_usealltoall(self) -> bool:
            """
            mct alltoall mapping flag
            default: false
            """
            pass

        @namelist_item
        def mct_usevector(self) -> bool:
            """
            mct vector flag
            default: false
            """
            pass

        @namelist_item
        def model_doi_url(self) -> str:
            """
            model doi url
            """
            pass

        @namelist_item
        def model_version(self) -> str:
            """
            model version documentation
            """
            pass

        @namelist_item
        def ocn_gnam(self) -> str:
            """
            OCN_GRID values passed into driver.
            """
            pass

        @namelist_item
        def orb_eccen(self) -> float:
            """
            eccentricity of orbit, used when orb_mode is fixed_parameters.
            default: SHR_ORB_UNDEF_REAL (1.e36) (Not currently used in build-namelist)
            """
            pass

        @namelist_item
        def orb_iyear(self) -> int:
            """
            year of orbit, used when orb_mode is fixed_year or variable_year. (default: 1990)
            """
            pass

        @namelist_item
        def orb_iyear_align(self) -> int:
            """
            model year associated with orb_iyear when orb_mode is variable_year. (default: 1990)
            """
            pass

        @namelist_item
        def orb_mode(self) -> str:
            """
            orbital model setting.  this sets how the orbital mode will be
            configured.
            "fixed_year" uses the orb_iyear and other orb inputs are ignored.  In
            this mode, the orbital parameters are constant and based on the year.
            "variable_year" uses the orb_iyear and orb_iyear_align.  In this mode,
            the orbital parameters vary as the model year advances and the model
            year orb_iyear_align has the equivalent orbital year of orb_iyear.
            "fixed_parameters" uses the orb_eccen, orb_mvelp, and orb_obliq to set
            the orbital parameters which then remain constant through the model
            integration. [fixed_year, variable_year, fixed_parameters]  (default: 'fixed_year'.)
            """
            pass

        @namelist_item
        def orb_mvelp(self) -> float:
            """
            location of vernal equinox in longitude degrees, used when orb_mode is fixed_parameters.
            default: SHR_ORB_UNDEF_REAL (1.e36)(Not currently used in build-namelist)
            """
            pass

        @namelist_item
        def orb_obliq(self) -> float:
            """
            obliquity of orbit in degrees, used when orb_mode is fixed_parameters.
            default: SHR_ORB_UNDEF_REAL (1.e36) (Not currently used in build-namelist)
            """
            pass

        @namelist_item
        def outpathroot(self) -> str:
            """
            Root directory for driver output files
            """
            pass

        @namelist_item
        def reprosum_diffmax(self) -> float:
            """
            Tolerance for relative error
            default: -1.0e-8
            """
            pass

        @namelist_item
        def reprosum_recompute(self) -> bool:
            """
            Recompute with non-scalable algorithm if reprosum_diffmax is exceeded.
            default: .false.
            """
            pass

        @namelist_item
        def reprosum_use_ddpdd(self) -> bool:
            """
            Use faster method for reprosum, but one where reproducibility is not always guaranteed.
            default: .false.
            """
            pass

        @namelist_item
        def restart_file(self) -> str:
            """
            Driver restart filename.
            (NOTE: Normally THIS IS NOT USED -- Set with RUN_REFCASE and RUN_REFDATE)
            """
            pass

        @namelist_item
        def rof_gnam(self) -> str:
            """
            ROF_GRID values passed into driver.
            """
            pass

        @namelist_item
        def run_barriers(self) -> bool:
            """
            default: .false.
            """
            pass

        @namelist_item
        def scmlat(self) -> int:
            """
            grid point latitude associated with single column mode.
            if set to -999, ignore this value
            """
            pass

        @namelist_item
        def scmlon(self) -> int:
            """
            grid point longitude associated with single column mode.
            set by PTS_LON in env_run.xml.
            """
            pass

        @namelist_item
        def shr_map_dopole(self) -> bool:
            """
            invoke pole averaging corrections in shr_map_mod weights generation (default: true)
            """
            pass

        @namelist_item
        def single_column(self) -> bool:
            """
            turns on single column mode. set by PTS_MODE in env_case.xml, default: false
            """
            pass

        @namelist_item
        def start_type(self) -> str:
            """
            mode to start the run up, [startup,branch,continue],
            automatically derived from RUN_TYPE in env_run.xml
            """
            pass

        @namelist_item
        def tchkpt_dir(self) -> str:
            """
            location of timing checkpoint output
            """
            pass

        @namelist_item
        def tfreeze_option(self) -> str:
            """
            Freezing point calculation for salt water.
            """
            pass

        @namelist_item
        def timing_dir(self) -> str:
            """
            location of timing output
            """
            pass

        @namelist_item
        def username(self) -> str:
            """
            username documentation
            """
            pass

        @namelist_item
        def vect_map(self) -> str:
            """
            vect_map
            turns on the vector mapping option for u and v vector mapping between
            atm and ocean grids in the coupler.  the options are none, npfix,
            cart3d, cart3d_diag, cart3d_uvw, and cart3d_uvw_diag.  the none option
            results in scalar mapping independently for the u and v field which
            tends to generate large errors near the poles.  npfix is the
            traditional option where the vectors are corrected on the ocean grid
            north of the last latitude line of the atmosphere grid.  the cart3d
            options convert the east (u) and north (v) vectors to 3d (x,y,z)
            triplets, and maps those fields before converting back to the east (u)
            and north (v) directions.  the cart3d ignores the resuling "w"
            velocity.  the cart3d_uvw calculates the resulting u and v vectors by
            preserving the total "u,v,w" speed and the angle of the (u,v) vector.
            the _diag options just add diagnotics to the log file about the vector
            mapping.
            """
            pass

        @namelist_item
        def wall_time_limit(self) -> float:
            """
            Wall time limit for run
            default: -1.0
            """
            pass

        @namelist_item
        def wav_gnam(self) -> float:
            """
            WAV_GRID values passed into driver.
            """
            pass

        @namelist_item
        def wv_sat_scheme(self) -> str:
            """
            Type of water vapor saturation vapor pressure scheme employed. 'GoffGratch' for
            Goff and Gratch (1946); 'MurphyKoop' for Murphy and Koop (2005); 'Bolton' for
            Bolton (1980); 'Flatau' for Flatau, Walko, and Cotton (1992).
            Default: GoffGratch
            """
            pass

        @namelist_item
        def wv_sat_table_spacing(self) -> float:
            """
            Temperature resolution of saturation vapor pressure lookup tables in Kelvin.
            (This is only used if wv_sat_use_tables is .true.)
            Default: 1.0
            """
            pass

        @namelist_item
        def wv_sat_transition_start(self) -> float:
            """
            Width of the liquid-ice transition range in mixed-phase water saturation vapor
            pressure calculations. The range always ends at 0 degrees Celsius, so this
            variable only affects the start of the transition.
            Default: 20K
            WARNING: CAM is tuned to the default value of this variable. Because it affects
            so many different parameterizations, changes to this variable may require a
            significant retuning of CAM's cloud physics to give reasonable results.
            """
            pass

        @namelist_item
        def wv_sat_use_tables(self) -> bool:
            """
            Whether or not to produce lookup tables at init time to use as a cache for
            saturation vapor pressure.
            Default: .false.
            """
            pass

    @namelist_group
    class seq_timemgr_inparm():

        @namelist_item
        def atm_cpl_dt(self) -> int:
            """
            atm coupling interval in seconds
            set via ATM_NCPL in env_run.xml.
            ATM_NCPL is the number of times the atm is coupled per NCPL_BASE_PERIOD
            NCPL_BASE_PERIOD is also set in env_run.xml and is the base period
            associated with NCPL coupling frequency, and has valid values: hour,day,year,decade
            """
            pass

        @namelist_item
        def atm_cpl_offset(self) -> int:
            """
            atm coupling interval offset in seconds default: 0
            """
            pass

        @namelist_item
        def barrier_n(self) -> int:
            """
            Sets model barriers with barrier_option and barrier_ymd (same options as stop_n)
            default: 1
            """
            pass

        @namelist_item
        def barrier_option(self) -> str:
            """
            sets the driver barrier frequency to sync models across all tasks with barrier_n and barrier_ymd
            barrier_option alarms are like restart_option
            default: never
            """
            pass

        @namelist_item
        def barrier_ymd(self) -> int:
            """
            Date in yyyymmdd format, sets model barriers date with barrier_option and barrier_n
            """
            pass

        @namelist_item
        def calendar(self) -> str:
            """
            calendar in use.  [NO_LEAP, GREOGORIAN].
            set by CALENDAR in env_build.xml
            """
            pass

        @namelist_item
        def data_assimilation_atm(self) -> bool:
            """
            Whether Data Assimilation is on for component atm
            """
            pass

        @namelist_item
        def data_assimilation_cpl(self) -> bool:
            """
            Whether Data Assimilation is on for component CPL
            """
            pass

        @namelist_item
        def data_assimilation_glc(self) -> bool:
            """
            Whether Data Assimilation is on for component glc
            """
            pass

        @namelist_item
        def data_assimilation_ice(self) -> bool:
            """
            Whether Data Assimilation is on for component ice
            """
            pass

        @namelist_item
        def data_assimilation_lnd(self) -> bool:
            """
            Whether Data Assimilation is on for component lnd
            """
            pass

        @namelist_item
        def data_assimilation_ocn(self) -> bool:
            """
            Whether Data Assimilation is on for component ocn
            """
            pass

        @namelist_item
        def data_assimilation_rof(self) -> bool:
            """
            Whether Data Assimilation is on for component rof
            """
            pass

        @namelist_item
        def data_assimilation_wav(self) -> bool:
            """
            Whether Data Assimilation is on for component wav
            """
            pass

        @namelist_item
        def end_restart(self) -> bool:
            """
            true => write restarts at end of run
            forces a restart write at the end of the run in addition to any
            setting associated with rest_option.  default=true.  this setting
            will be set to false if restart_option is none or never.
            default: false
            """
            pass

        @namelist_item
        def esp_cpl_dt(self) -> int:
            """
            esp run interval in seconds
            esp_cpl_dt is the number of times the esp is run per NCPL_BASE_PERIOD
            NCPL_BASE_PERIOD is set in env_run.xml and is the base period
            associated with NCPL coupling frequency, nad has valid values: hour,day,year,decade
            default value set by buildnml to be the pause interval if pause is active
            otherwise, it is set to the shortest component coupling time
            """
            pass

        @namelist_item
        def esp_cpl_offset(self) -> int:
            """
            esp coupling interval offset in seconds default: 0
            """
            pass

        @namelist_item
        def esp_run_on_pause(self) -> bool:
            """
            true => ESP component runs after driver 'pause cycle' If any
            component 'pauses' (see PAUSE_OPTION,
            PAUSE_N and DATA_ASSIMILATION_XXX XML
            variables), the ESP component (if present) will be run to
            process the component 'pause' (restart) files and set any
            required 'resume' signals.  If true, esp_cpl_dt and
            esp_cpl_offset settings are ignored.  default: true
            """
            pass

        @namelist_item
        def glc_avg_period(self) -> str:
            """
            Period at which coupler averages fields sent to GLC.
            This supports doing the averaging to GLC less frequently than GLC is called
            (i.e., separating the averaging frequency from the calling frequency).
            This is useful because there are benefits to only averaging the GLC inputs
            as frequently as they are really needed (yearly for CISM), but GLC needs to
            still be called more frequently than that in order to support mid-year restarts.

            Setting glc_avg_period to 'glc_coupling_period' means that the averaging is
            done exactly when the GLC is called (governed by GLC_NCPL).
            """
            pass

        @namelist_item
        def glc_cpl_dt(self) -> int:
            """
            glc coupling interval in seconds
            set via GLC_NCPL in env_run.xml.
            GLC_NCPL is the number of times the glc is coupled per NCPL_BASE_PERIOD
            NCPL_BASE_PERIOD is also set in env_run.xml and is the base period
            associated with NCPL coupling frequency, nad has valid values: hour,day,year,decade
            """
            pass

        @namelist_item
        def glc_cpl_offset(self) -> int:
            """
            glc coupling interval offset in seconds default: 0
            """
            pass

        @namelist_item
        def histavg_n(self) -> int:
            """
            Sets coupler time-average history file frequency (like restart_option)
            set by AVGHIST_N in env_run.xml.
            """
            pass

        @namelist_item
        def histavg_option(self) -> str:
            """
            coupler time average history option (used with histavg_n and histavg_ymd)
            set by AVGHIST_OPTION in env_run.xml.
            histavg_option alarms are:
            [none/never], turns option off
            [nstep/s]   , history snapshot every histavg_n nsteps  , relative to current run start time
            [nsecond/s] , history snapshot every histavg_n nseconds, relative to current run start time
            [nminute/s] , history snapshot every histavg_n nminutes, relative to current run start time
            [nhour/s]   , history snapshot every histavg_n nhours  , relative to current run start time
            [nday/s]    , history snapshot every histavg_n ndays   , relative to current run start time
            [monthly/s] , history snapshot every           month   , relative to current run start time
            [nmonth/s]  , history snapshot every histavg_n nmonths , relative to current run start time
            [nyear/s]   , history snapshot every histavg_n nyears  , relative to current run start time
            [date]      , history snapshot at histavg_ymd value
            [ifdays0]   , history snapshot at histavg_n calendar day value and seconds equal 0
            [end]       , history snapshot at end
            """
            pass

        @namelist_item
        def histavg_ymd(self) -> int:
            """
            date associated with histavg_option date.  yyyymmdd format.
            set by AVGHIST_DATE in env_run.xml.
            """
            pass

        @namelist_item
        def history_n(self) -> int:
            """
            sets coupler snapshot history file frequency (like restart_n)
            set by HIST_N in env_run.xml.
            """
            pass

        @namelist_item
        def history_option(self) -> str:
            """
            coupler history snapshot option (used with history_n and history_ymd)
            set by HIST_OPTION in env_run.xml.
            history_option alarms are:
            [none/never], turns option off
            [nstep/s]   , history snapshot every history_n nsteps  , relative to current run start time
            [nsecond/s] , history snapshot every history_n nseconds, relative to current run start time
            [nminute/s] , history snapshot every history_n nminutes, relative to current run start time
            [nhour/s]   , history snapshot every history_n nhours  , relative to current run start time
            [nday/s]    , history snapshot every history_n ndays   , relative to current run start time
            [monthly/s] , history snapshot every           month   , relative to current run start time
            [nmonth/s]  , history snapshot every history_n nmonths , relative to current run start time
            [nyear/s]   , history snapshot every history_n nyears  , relative to current run start time
            [date]      , history snapshot at history_ymd value
            [ifdays0]   , history snapshot at history_n calendar day value and seconds equal 0
            [end]       , history snapshot at end
            """
            pass

        @namelist_item
        def history_ymd(self) -> int:
            """
            date associated with history_option date.  yyyymmdd format.
            set by HIST_DATE in env_run.xml.
            """
            pass

        @namelist_item
        def ice_cpl_dt(self) -> int:
            """
            ice coupling interval in seconds
            set via ICE_NCPL in env_run.xml.
            ICE_NCPL is the number of times the ice is coupled per NCPL_BASE_PERIOD
            NCPL_BASE_PERIOD is also set in env_run.xml and is the base period
            associated with NCPL coupling frequency, nad has valid values: hour,day,year,decade
            """
            pass

        @namelist_item
        def ice_cpl_offset(self) -> int:
            """
            ice coupling interval offset in seconds default: 0
            """
            pass

        @namelist_item
        def lnd_cpl_dt(self) -> int:
            """
            lnd coupling interval in seconds
            set via LND_NCPL in env_run.xml.
            LND_NCPL is the number of times the lnd is coupled per NCPL_BASE_PERIOD
            NCPL_BASE_PERIOD is also set in env_run.xml and is the base period
            associated with NCPL coupling frequency, nad has valid values: hour,day,year,decade
            """
            pass

        @namelist_item
        def lnd_cpl_offset(self) -> int:
            """
            lnd coupling interval offset in seconds default: 0
            """
            pass

        @namelist_item
        def ocn_cpl_dt(self) -> int:
            """
            ocn coupling interval in seconds
            set via OCN_NCPL in env_run.xml.
            OCN_NCPL is the number of times the ocn is coupled per NCPL_BASE_PERIOD
            NCPL_BASE_PERIOD is also set in env_run.xml and is the base period
            associated with NCPL coupling frequency, nad has valid values: hour,day,year,decade
            """
            pass

        @namelist_item
        def ocn_cpl_offset(self) -> int:
            """
            ocn coupling interval offset in seconds default: 0
            """
            pass

        @namelist_item
        def pause_active_atm(self) -> bool:
            """
            Whether Pause signals are active for component atm
            """
            pass

        @namelist_item
        def pause_active_cpl(self) -> bool:
            """
            Whether Pause signals are active for component CPL
            """
            pass

        @namelist_item
        def pause_active_glc(self) -> bool:
            """
            Whether Pause signals are active for component ocn
            """
            pass

        @namelist_item
        def pause_active_ice(self) -> bool:
            """
            Whether Pause signals are active for component ice
            """
            pass

        @namelist_item
        def pause_active_lnd(self) -> bool:
            """
            Whether Pause signals are active for component lnd
            """
            pass

        @namelist_item
        def pause_active_ocn(self) -> bool:
            """
            Whether Pause signals are active for component ocn
            """
            pass

        @namelist_item
        def pause_active_rof(self) -> bool:
            """
            Whether Pause signals are active for component rof
            """
            pass

        @namelist_item
        def pause_active_wav(self) -> bool:
            """
            Whether Pause signals are active for component wav
            """
            pass

        @namelist_item
        def pause_n(self) -> int:
            """
            Sets the pause frequency with pause_option
            """
            pass

        @namelist_item
        def pause_option(self) -> str:
            """
            sets the pause frequency with pause_n
            pause_option alarms are:
            [none/never], turns option off
            [nstep/s]   , pauses every pause_n nsteps  , relative to start or last pause time
            [nsecond/s] , pauses every pause_n nseconds, relative to start or last pause time
            [nminute/s] , pauses every pause_n nminutes, relative to start or last pause time
            [nhour/s]   , pauses every pause_n nhours  , relative to start or last pause time
            [nday/s]    , pauses every pause_n ndays   , relative to start or last pause time
            [nmonth/s]  , pauses every pause_n nmonths , relative to start or last pause time
            [monthly/s] , pauses every        month    , relative to start or last pause time
            [nyear/s]   , pauses every pause_n nyears  , relative to start or last pause time
            """
            pass

        @namelist_item
        def restart_file(self) -> str:
            """
            Driver restart filename.
            (NOTE: Normally THIS IS NOT USED -- Set with RUN_REFCASE and RUN_REFDATE)
            """
            pass

        @namelist_item
        def restart_n(self) -> int:
            """
            Sets model restart writes with restart_option and restart_ymd (same options as stop_n)
            """
            pass

        @namelist_item
        def restart_option(self) -> str:
            """
            sets the restart frequency with restart_n and restart_ymd
            restart_option alarms are:
            [none/never], turns option off
            [nstep/s]   , restarts every restart_n nsteps  , relative to current run start time
            [nsecond/s] , restarts every restart_n nseconds, relative to current run start time
            [nminute/s] , restarts every restart_n nminutes, relative to current run start time
            [nhour/s]   , restarts every restart_n nhours  , relative to current run start time
            [nday/s]    , restarts every restart_n ndays   , relative to current run start time
            [monthly/s] , restarts every           month   , relative to current run start time
            [nmonth/s]  , restarts every restart_n nmonths , relative to current run start time
            [nyear/s]   , restarts every restart_n nyears  , relative to current run start time
            [date]      , restarts at restart_ymd value
            [ifdays0]   , restarts at restart_n calendar day value and seconds equal 0
            [end]       , restarts at end
            """
            pass

        @namelist_item
        def restart_ymd(self) -> int:
            """
            Date in yyyymmdd format, sets model restart write date with rest_option and restart_n
            default: STOP_N
            """
            pass

        @namelist_item
        def rof_cpl_dt(self) -> int:
            """
            river runoff coupling interval in seconds
            currently set by default to 10800 seconds.
            default: 10800
            """
            pass

        @namelist_item
        def start_tod(self) -> int:
            """
            Start time-of-day in universal time (seconds), should be between zero and 86400
            default: 0
            """
            pass

        @namelist_item
        def start_ymd(self) -> int:
            """
            Run start date in yyyymmdd format, only used for startup and hybrid runs.
            default: 00010101
            """
            pass

        @namelist_item
        def stop_n(self) -> int:
            """
            Sets the run length with stop_option and stop_ymd
            """
            pass

        @namelist_item
        def stop_option(self) -> str:
            """
            sets the run length with stop_n and stop_ymd
            stop_option alarms are:
            [none/never], turns option off
            [nstep/s]   , stops every stop_n nsteps  , relative to current run start time
            [nsecond/s] , stops every stop_n nseconds, relative to current run start time
            [nminute/s] , stops every stop_n nminutes, relative to current run start time
            [nhour/s]   , stops every stop_n nhours  , relative to current run start time
            [nday/s]    , stops every stop_n ndays   , relative to current run start time
            [nmonth/s]  , stops every stop_n nmonths , relative to current run start time
            [monthly/s] , stops every        month   , relative to current run start time
            [nyear/s]   , stops every stop_n nyears  , relative to current run start time
            [date]      , stops at stop_ymd value
            [ifdays0]   , stops at stop_n calendar day value and seconds equal 0
            [end]       , stops at end
            """
            pass

        @namelist_item
        def stop_ymd(self) -> int:
            """
            date in yyyymmdd format, sets the run length with stop_option and stop_n,
            can be in addition to stop_option and stop_n, negative value implies off
            """
            pass

        @namelist_item
        def tprof_n(self) -> int:
            """
            Sets timing output file frequency (like restart_n)
            """
            pass

        @namelist_item
        def tprof_option(self) -> str:
            """
            Sets timing output file frequency (like rest_option but relative to run start date)
            tprof_option alarms are:
            [none/never], turns option off
            [nstep/s]   , every tprof_n nsteps  , relative to current run start time
            [nsecond/s] , every tprof_n nseconds, relative to current run start time
            [nminute/s] , every tprof_n nminutes, relative to current run start time
            [nhour/s]   , every tprof_n nhours  , relative to current run start time
            [nday/s]    , every tprof_n ndays   , relative to current run start time
            [monthly/s] , every         month   , relative to current run start time
            [nmonth/s]  , every tprof_n nmonths , relative to current run start time
            [nyear/s]   , every tprof_n nyears  , relative to current run start time
            [date]      , at tprof_ymd value
            [ifdays0]   , at tprof_n calendar day value and seconds equal 0
            [end]       , at end
            """
            pass

        @namelist_item
        def tprof_ymd(self) -> int:
            """
            yyyymmdd format, sets timing output file date (like restart_date)
            """
            pass

        @namelist_item
        def wav_cpl_dt(self) -> int:
            """
            wav coupling interval in seconds
            set via WAV_NCPL in env_run.xml.
            WAV_NCPL is the number of times the wav is coupled per NCPL_BASE_PERIOD
            NCPL_BASE_PERIOD is also set in env_run.xml and is the base period
            associated with NCPL coupling frequency, nad has valid values: hour,day,year,decade
            """
            pass

        @namelist_item
        def wav_cpl_offset(self) -> int:
            """
            wav coupling interval offset in seconds default: 0
            """
            pass
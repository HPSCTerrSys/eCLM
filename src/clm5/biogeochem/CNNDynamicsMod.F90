module CNNDynamicsMod

  !-----------------------------------------------------------------------
  ! !DESCRIPTION:
  ! Module for mineral nitrogen dynamics (deposition, fixation, leaching)
  ! for coupled carbon-nitrogen code.
  !
  ! !USES:
  use shr_kind_mod                    , only : r8 => shr_kind_r8
  use decompMod                       , only : bounds_type
  use clm_varcon                      , only : dzsoi_decomp, zisoi
  use clm_varpar                       , only : nlevdecomp
  use clm_varctl                       , only : manure_fmet, manure_fcel, manure_flig, &
                                                manure_injection_depth  ! tboas: cfert_inparm params
  use clm_varctl                       , only : manure_freq_years, manure_apply_month, &
                                                manure_apply_day  ! tboas: timing/frequency params
  use clm_varctl                      , only : use_nitrif_denitrif, use_vertsoilc, nfix_timeconst
  use clm_varctl                       , only : use_cfert, use_crop  ! tboas: use_cfert for organic C fert
  use subgridAveMod                   , only : p2c
  use atm2lndType                     , only : atm2lnd_type
  use CNVegStateType                  , only : cnveg_state_type
  use CNVegCarbonFluxType             , only : cnveg_carbonflux_type
  use CNVegNitrogenStateType	      , only : cnveg_nitrogenstate_type
  use CNVegNitrogenFluxType	      , only : cnveg_nitrogenflux_type
  use SoilBiogeochemStateType         , only : soilbiogeochem_state_type
  use SoilBiogeochemNitrogenStateType , only : soilbiogeochem_nitrogenstate_type
  use SoilBiogeochemNitrogenFluxType  , only : soilbiogeochem_nitrogenflux_type
  use WaterStateType                  , only : waterstate_type
  use WaterFluxType                   , only : waterflux_type
  use CropType                        , only : crop_type
  use ColumnType                      , only : col                
  use PatchType                       , only : patch                
  use perf_mod                        , only : t_startf, t_stopf
  !
  implicit none
  private
  !
  ! !PUBLIC MEMBER FUNCTIONS:
  public :: CNNDynamicsReadNML          ! Read in namelist for Mineral Nitrogen Dynamics
  public :: CNNDeposition               ! Update N deposition rate from atm forcing
  public :: CNNFixation                 ! Update N Fixation rate
  public :: CNNFert                     ! Update N fertilizer for crops
  public :: CNCSoilFert          ! tboas: route organic C fertilizer into litter pools
  public :: CNSoyfix                    ! N Fixation for soybeans
  public :: CNFreeLivingFixation        ! N free living fixation

  !
  ! !PRIVATE DATA MEMBERS:
  type, private :: params_type
     real(r8) :: freelivfix_intercept   ! intercept of line of free living fixation with annual ET
     real(r8) :: freelivfix_slope_wET   ! slope of line of free living fixation with annual ET
  end type params_type
  type(params_type) :: params_inst
  ! tboas: litter partitioning fractions for manure C (metabolic / cellulose / lignin)
  ! Based on typical farmyard manure composition (10% lignin, ~60% metabolic, ~30% cellulose)
  ! tboas: manure_fmet/fcel/flig and manure_injection_depth imported from clm_varctl via use statement below
  !-----------------------------------------------------------------------

contains

  !-----------------------------------------------------------------------
  subroutine CNNDynamicsReadNML( NLFilename )
    !
    ! !DESCRIPTION:
    ! Read the namelist for Mineral Nitrogen Dynamics
    !
    ! !USES:
    use fileutils      , only : getavu, relavu, opnfil
    use shr_nl_mod     , only : shr_nl_find_group_name
    use spmdMod        , only : masterproc, mpicom
    use shr_mpi_mod    , only : shr_mpi_bcast
    use clm_varctl     , only : iulog
    use shr_log_mod    , only : errMsg => shr_log_errMsg
    use abortutils     , only : endrun
    !
    character(len=*), intent(in) :: NLFilename
    !
    integer  :: ierr, unitn

    character(len=*), parameter :: subname = 'CNNDynamicsReadNML'
    character(len=*), parameter :: nmlname = 'mineral_nitrogen_dynamics'
    !-----------------------------------------------------------------------
    real(r8) :: freelivfix_intercept
    real(r8) :: freelivfix_slope_wET
    namelist /mineral_nitrogen_dynamics/ freelivfix_slope_wET, freelivfix_intercept



    freelivfix_intercept = 0.0117_r8
    freelivfix_slope_wET = 0.0006_r8
    if (masterproc) then
       unitn = getavu()
       write(iulog,*) 'Read in '//nmlname//'  namelist'
       call opnfil (NLFilename, unitn, 'F')
       call shr_nl_find_group_name(unitn, nmlname, status=ierr)
       if (ierr == 0) then
          read(unitn, nml=mineral_nitrogen_dynamics, iostat=ierr)
          if (ierr /= 0) then
             call endrun(msg="ERROR reading "//nmlname//"namelist"//errmsg(__FILE__, __LINE__))
          end if
       else
          call endrun(msg="ERROR could NOT find "//nmlname//"namelist"//errmsg(__FILE__, __LINE__))
       end if
       call relavu( unitn )
    end if

    call shr_mpi_bcast (freelivfix_intercept, mpicom)
    call shr_mpi_bcast (freelivfix_slope_wET, mpicom)

    if (masterproc) then
       write(iulog,*) ' '
       write(iulog,*) nmlname//' settings:'
       write(iulog,nml=mineral_nitrogen_dynamics)
       write(iulog,*) ' '
    end if
    params_inst%freelivfix_intercept = freelivfix_intercept
    params_inst%freelivfix_slope_wET = freelivfix_slope_wET

  end subroutine CNNDynamicsReadNML

  !-----------------------------------------------------------------------
  subroutine CNNDeposition( bounds, &
       atm2lnd_inst, soilbiogeochem_nitrogenflux_inst )
    !
    type(bounds_type)        , intent(in)    :: bounds  
    type(atm2lnd_type)       , intent(in)    :: atm2lnd_inst
    type(soilbiogeochem_nitrogenflux_type) , intent(inout) :: soilbiogeochem_nitrogenflux_inst
    !
    integer :: g,c
    !-----------------------------------------------------------------------
    
    associate(                                                                & 
         forc_ndep    => atm2lnd_inst%forc_ndep_grc                            , &
         ndep_to_sminn => soilbiogeochem_nitrogenflux_inst%ndep_to_sminn_col   &
         )
      
      do c = bounds%begc, bounds%endc
         g = col%gridcell(c)
         ndep_to_sminn(c) = forc_ndep(g)

      end do

    end associate

  end subroutine CNNDeposition

  !-----------------------------------------------------------------------
  subroutine CNFreeLivingFixation(num_soilc, filter_soilc, &
       waterflux_inst, soilbiogeochem_nitrogenflux_inst)


    use clm_time_manager , only : get_days_per_year, get_step_size
    use shr_sys_mod      , only : shr_sys_flush
    use clm_varcon       , only : secspday, spval
 
    integer                                 , intent(in)    :: num_soilc
    integer                                 , intent(in)    :: filter_soilc(:)
   
    type(soilbiogeochem_nitrogenflux_type) , intent(inout) :: soilbiogeochem_nitrogenflux_inst 
    type(waterflux_type)                   , intent(inout) :: waterflux_inst 
    !
    integer  :: c,fc
    real(r8) :: dayspyr, secs_per_year

       associate(                                                                        &
         AnnET           => waterflux_inst%AnnET                                       , &
         freelivfix_slope => params_inst%freelivfix_slope_wET                          , &
         freelivfix_inter => params_inst%freelivfix_intercept                          , &
         ffix_to_sminn   => soilbiogeochem_nitrogenflux_inst%ffix_to_sminn_col        &
                ) 
       
       dayspyr = get_days_per_year()
       secs_per_year = dayspyr*24_r8*3600_r8

       do fc = 1,num_soilc
           c = filter_soilc(fc)
         ffix_to_sminn(c) = (freelivfix_slope*(max(0._r8,AnnET(c))*secs_per_year) + freelivfix_inter)/secs_per_year

       end do

  end associate
  end subroutine CNFreeLivingFixation

  !-----------------------------------------------------------------------
  subroutine CNNFixation(num_soilc, filter_soilc, &
       cnveg_carbonflux_inst, soilbiogeochem_nitrogenflux_inst)
    use clm_time_manager , only : get_days_per_year, get_step_size
    use shr_sys_mod      , only : shr_sys_flush
    use clm_varcon       , only : secspday, spval
    use CNSharedParamsMod    , only: use_fun
    integer                                , intent(in)    :: num_soilc
    integer                                , intent(in)    :: filter_soilc(:)
    type(cnveg_carbonflux_type)            , intent(inout) :: cnveg_carbonflux_inst
    type(soilbiogeochem_nitrogenflux_type) , intent(inout) :: soilbiogeochem_nitrogenflux_inst 
    !
    integer  :: c,fc
    real(r8) :: t, dayspyr
    !-----------------------------------------------------------------------

    associate(                                                                & 
         cannsum_npp  => cnveg_carbonflux_inst%annsum_npp_col          , &
         col_lag_npp  => cnveg_carbonflux_inst%lag_npp_col             , &
         nfix_to_sminn => soilbiogeochem_nitrogenflux_inst%nfix_to_sminn_col &
         )

      dayspyr = get_days_per_year()

      if ( nfix_timeconst > 0._r8 .and. nfix_timeconst < 500._r8 ) then
         do fc = 1,num_soilc
            c = filter_soilc(fc)         

            if (col_lag_npp(c) /= spval) then
               t = (1.8_r8 * (1._r8 - exp(-0.003_r8 * col_lag_npp(c)*(secspday * dayspyr))))/(secspday * dayspyr)  
               nfix_to_sminn(c) = max(0._r8,t)
            else
               nfix_to_sminn(c) = 0._r8
            endif
         end do
      else
         do fc = 1,num_soilc
            c = filter_soilc(fc)

            t = (1.8_r8 * (1._r8 - exp(-0.003_r8 * cannsum_npp(c))))/(secspday * dayspyr)
            nfix_to_sminn(c) = max(0._r8,t)
         end do
      endif
      if(use_fun)then
        nfix_to_sminn(c) = 0.0_r8
      end if

    end associate

  end subroutine CNNFixation
 
  !-----------------------------------------------------------------------
  subroutine CNNFert(bounds, num_soilc, filter_soilc, &
       cnveg_nitrogenflux_inst, soilbiogeochem_nitrogenflux_inst)
    !
    type(bounds_type)                      , intent(in)    :: bounds  
    integer                                , intent(in)    :: num_soilc
    integer                                , intent(in)    :: filter_soilc(:)
    type(cnveg_nitrogenflux_type)          , intent(in)    :: cnveg_nitrogenflux_inst
    type(soilbiogeochem_nitrogenflux_type) , intent(inout) :: soilbiogeochem_nitrogenflux_inst 
    !
    integer :: c,fc
    !-----------------------------------------------------------------------

    associate(                                                                  &   
         fert         => cnveg_nitrogenflux_inst%fert_patch                        , &
         fert_to_sminn => soilbiogeochem_nitrogenflux_inst%fert_to_sminn_col       &
         )
      
      call p2c(bounds, num_soilc, filter_soilc, &
           fert(bounds%begp:bounds%endp), &
           fert_to_sminn(bounds%begc:bounds%endc))
    end associate
  end subroutine CNNFert

  !-----------------------------------------------------------------------
  subroutine CNCSoilFert(bounds, num_soilc, filter_soilc, cnveg_carbonflux_inst, &
       cnveg_nitrogenflux_inst)
    !
    ! !DESCRIPTION: tboas
    ! Route patch-level organic C fertilizer (fertC_patch) from manure application
    ! into the surface litter pools at column level.
    ! Manure C is partitioned between metabolic, cellulose, and lignin litter pools
    ! using fixed fractions (manure_fmet / manure_fcel / manure_flig).
    ! Only active when use_cfert = .true. and use_crop = .true.
    !
    ! phenology_c_to_litr_*_col live in cnveg_carbonflux_type (not soilbiogeochem).
    ! Inputs are at patch level (gC/m2/s); outputs enter at column level,
    ! surface decomp layer (j=1) only.
    !
    type(bounds_type)            , intent(in)    :: bounds
    integer                      , intent(in)    :: num_soilc
    integer                      , intent(in)    :: filter_soilc(:)
    type(cnveg_carbonflux_type)  , intent(inout) :: cnveg_carbonflux_inst
    type(cnveg_nitrogenflux_type), intent(inout) :: cnveg_nitrogenflux_inst  ! tboas-fix
    !
    ! LOCAL VARIABLES
    integer  :: fc, c, pi, p
    real(r8) :: fertC_col   ! column-level sum of fertC_patch (area-weighted, gC/m2/s)
    real(r8) :: fertN_col   ! tboas-fix: organic manure N accompanying fertC_col (gN/m2/s)
    !-----------------------------------------------------------------------

    if (.not. use_cfert .or. .not. use_crop) return

    associate( &
         fertC_patch               => cnveg_carbonflux_inst%fertC_patch                    , & ! Input:  patch-level organic C fert flux (gC/m2/s)
         fertN_patch               => cnveg_nitrogenflux_inst%fertN_patch                  , & ! Input:  patch-level organic N fert flux (gN/m2/s)  tboas-fix
         wtcol                     => patch%wtcol                                           , & ! Input:  patch weight on column
         phenology_c_to_litr_met_c => cnveg_carbonflux_inst%phenology_c_to_litr_met_c_col  , & ! Output: litter metabolic pool (gC/m3/s)
         phenology_c_to_litr_cel_c => cnveg_carbonflux_inst%phenology_c_to_litr_cel_c_col  , & ! Output: litter cellulose pool (gC/m3/s)
         phenology_c_to_litr_lig_c => cnveg_carbonflux_inst%phenology_c_to_litr_lig_c_col  , & ! Output: litter lignin pool (gC/m3/s)
         ! tboas-fix: the manure N that travels with the manure C
         phenology_n_to_litr_met_n => cnveg_nitrogenflux_inst%phenology_n_to_litr_met_n_col , & ! Output: litter metabolic pool (gN/m3/s)
         phenology_n_to_litr_cel_n => cnveg_nitrogenflux_inst%phenology_n_to_litr_cel_n_col , & ! Output: litter cellulose pool (gN/m3/s)
         phenology_n_to_litr_lig_n => cnveg_nitrogenflux_inst%phenology_n_to_litr_lig_n_col   & ! Output: litter lignin pool (gN/m3/s)
         )

      do fc = 1, num_soilc
         c = filter_soilc(fc)
         fertC_col = 0.0_r8
         fertN_col = 0.0_r8

         ! Aggregate patch-level fertC/fertN to column (area-weighted)
         do pi = 1, col%npatches(c)
            p = col%patchi(c) + pi - 1
            if (patch%active(p)) then
               fertC_col = fertC_col + fertC_patch(p) * wtcol(p)
               fertN_col = fertN_col + fertN_patch(p) * wtcol(p)  ! tboas-fix
            end if
         end do

         ! Route into surface litter pools (layer j=1), volumetric units gC/m3/s
         ! tboas: distribute manure C over layers down to manure_injection_depth
         ! If manure_injection_depth=0 (default), apply to surface layer only (j=1)
         ! tboas-fix: the organic manure N travels with the manure C, so the litter
         ! pools receive both at manure_CN_ratio and the N is mineralised by the
         ! decomposition cascade rather than being injected into the mineral pool a
         ! second time (which is what the pre-fix code effectively did).

         if (manure_injection_depth <= 0.0_r8) then
            phenology_c_to_litr_met_c(c,1) = phenology_c_to_litr_met_c(c,1) + &
                 fertC_col * manure_fmet / dzsoi_decomp(1)
            phenology_c_to_litr_cel_c(c,1) = phenology_c_to_litr_cel_c(c,1) + &
                 fertC_col * manure_fcel / dzsoi_decomp(1)
            phenology_c_to_litr_lig_c(c,1) = phenology_c_to_litr_lig_c(c,1) + &
                 fertC_col * manure_flig / dzsoi_decomp(1)
            phenology_n_to_litr_met_n(c,1) = phenology_n_to_litr_met_n(c,1) + &
                 fertN_col * manure_fmet / dzsoi_decomp(1)
            phenology_n_to_litr_cel_n(c,1) = phenology_n_to_litr_cel_n(c,1) + &
                 fertN_col * manure_fcel / dzsoi_decomp(1)
            phenology_n_to_litr_lig_n(c,1) = phenology_n_to_litr_lig_n(c,1) + &
                 fertN_col * manure_flig / dzsoi_decomp(1)
         else
            ! Distribute proportionally over layers within injection depth
            ! Weight by dzsoi_decomp so total flux integrates to fertC_col [gC/m2/s]
            block
               integer  :: j
               real(r8) :: depth_top, layer_wt, total_wt
               total_wt = 0.0_r8
               depth_top = 0.0_r8
               do j = 1, nlevdecomp
                  if (depth_top >= manure_injection_depth) exit
                  total_wt  = total_wt + dzsoi_decomp(j)
                  depth_top = depth_top + dzsoi_decomp(j)
               end do
               if (total_wt <= 0.0_r8) total_wt = dzsoi_decomp(1)  ! guard
               depth_top = 0.0_r8
               do j = 1, nlevdecomp
                  if (depth_top >= manure_injection_depth) exit
                  layer_wt = dzsoi_decomp(j) / total_wt
                  phenology_c_to_litr_met_c(c,j) = phenology_c_to_litr_met_c(c,j) + &
                       fertC_col * manure_fmet * layer_wt / dzsoi_decomp(j)
                  phenology_c_to_litr_cel_c(c,j) = phenology_c_to_litr_cel_c(c,j) + &
                       fertC_col * manure_fcel * layer_wt / dzsoi_decomp(j)
                  phenology_c_to_litr_lig_c(c,j) = phenology_c_to_litr_lig_c(c,j) + &
                       fertC_col * manure_flig * layer_wt / dzsoi_decomp(j)
                  phenology_n_to_litr_met_n(c,j) = phenology_n_to_litr_met_n(c,j) + &
                       fertN_col * manure_fmet * layer_wt / dzsoi_decomp(j)
                  phenology_n_to_litr_cel_n(c,j) = phenology_n_to_litr_cel_n(c,j) + &
                       fertN_col * manure_fcel * layer_wt / dzsoi_decomp(j)
                  phenology_n_to_litr_lig_n(c,j) = phenology_n_to_litr_lig_n(c,j) + &
                       fertN_col * manure_flig * layer_wt / dzsoi_decomp(j)
                  depth_top = depth_top + dzsoi_decomp(j)
               end do
            end block
         end if

      end do

    end associate

  end subroutine CNCSoilFert

  !-----------------------------------------------------------------------
  subroutine CNSoyfix (bounds, num_soilc, filter_soilc, num_soilp, filter_soilp, &
       waterstate_inst, crop_inst, cnveg_state_inst, cnveg_nitrogenflux_inst , &
       soilbiogeochem_state_inst, soilbiogeochem_nitrogenstate_inst, soilbiogeochem_nitrogenflux_inst)
    !
    use pftconMod, only : ntmp_soybean, nirrig_tmp_soybean, ntrp_soybean, nirrig_trp_soybean
    !
    type(bounds_type)                       , intent(in)    :: bounds  
    integer                                , intent(in)    :: num_soilc
    integer                                , intent(in)    :: filter_soilc(:)
    integer                                , intent(in)    :: num_soilp
    integer                                , intent(in)    :: filter_soilp(:)
    type(waterstate_type)                   , intent(in)    :: waterstate_inst
    type(crop_type)                         , intent(in)    :: crop_inst
    type(cnveg_state_type)                  , intent(in)    :: cnveg_state_inst
    type(cnveg_nitrogenflux_type)           , intent(inout) :: cnveg_nitrogenflux_inst
    type(soilbiogeochem_state_type)         , intent(in)    :: soilbiogeochem_state_inst
    type(soilbiogeochem_nitrogenstate_type) , intent(in)    :: soilbiogeochem_nitrogenstate_inst
    type(soilbiogeochem_nitrogenflux_type)  , intent(inout) :: soilbiogeochem_nitrogenflux_inst 
    !
    integer :: fp,p,c
    real(r8) :: fxw,fxn,fxg,fxr
    real(r8) :: soy_ndemand
    real(r8):: GDDfrac
    real(r8):: sminnthreshold1, sminnthreshold2
    real(r8):: GDDfracthreshold1, GDDfracthreshold2
    real(r8):: GDDfracthreshold3, GDDfracthreshold4
    !-----------------------------------------------------------------------

    associate(                                                                      & 
         wf            => waterstate_inst%wf_col                                         , &
         hui           => crop_inst%gddplant_patch                                        , &
         croplive      => crop_inst%croplive_patch                                        , &
         gddmaturity   => cnveg_state_inst%gddmaturity_patch                              , &
         plant_ndemand => cnveg_nitrogenflux_inst%plant_ndemand_patch                     , &
         soyfixn       => cnveg_nitrogenflux_inst%soyfixn_patch                           , &
         fpg           => soilbiogeochem_state_inst%fpg_col                               , &
         sminn         => soilbiogeochem_nitrogenstate_inst%sminn_col                     , &
         soyfixn_to_sminn => soilbiogeochem_nitrogenflux_inst%soyfixn_to_sminn_col        &
         )

      sminnthreshold1 = 30._r8
      sminnthreshold2 = 10._r8
      GDDfracthreshold1 = 0.15_r8
      GDDfracthreshold2 = 0.30_r8
      GDDfracthreshold3 = 0.55_r8
      GDDfracthreshold4 = 0.75_r8

      do fp = 1,num_soilp
         p = filter_soilp(fp)
         c = patch%column(p)


         if (croplive(p) .and. &
              (patch%itype(p) == ntmp_soybean .or. &
               patch%itype(p) == nirrig_tmp_soybean .or. &
               patch%itype(p) == ntrp_soybean .or. &
               patch%itype(p) == nirrig_trp_soybean) ) then


            if (fpg(c) < 1._r8) then
               soy_ndemand = 0._r8
               soy_ndemand = plant_ndemand(p) - plant_ndemand(p)*fpg(c)


               fxw = 0._r8
               fxw = wf(c)/0.85_r8


               if (sminn(c) > sminnthreshold1) then
                  fxn = 0._r8
               else if (sminn(c) > sminnthreshold2 .and. sminn(c) <= sminnthreshold1) then
                  fxn = 1.5_r8 - .005_r8 * (sminn(c) * 10._r8)
               else if (sminn(c) <= sminnthreshold2) then
                  fxn = 1._r8
               end if


               GDDfrac = hui(p) / gddmaturity(p)

               if (GDDfrac <= GDDfracthreshold1) then
                  fxg = 0._r8
               else if (GDDfrac > GDDfracthreshold1 .and. GDDfrac <= GDDfracthreshold2) then
                  fxg = 6.67_r8 * GDDfrac - 1._r8
               else if (GDDfrac > GDDfracthreshold2 .and. GDDfrac <= GDDfracthreshold3) then
                  fxg = 1._r8
               else if (GDDfrac > GDDfracthreshold3 .and. GDDfrac <= GDDfracthreshold4) then
                  fxg = 3.75_r8 - 5._r8 * GDDfrac
               else
                  fxg = 0._r8
               end if


               fxr = min(1._r8, fxw, fxn) * fxg 
               fxr = max(0._r8, fxr)
               soyfixn(p) =  fxr * soy_ndemand
               soyfixn(p) = min(soyfixn(p), soy_ndemand)

            else

               soyfixn(p) = 0._r8

            end if

         else

            soyfixn(p) = 0._r8

         end if
      end do

      call p2c(bounds, num_soilc, filter_soilc, &
           soyfixn(bounds%begp:bounds%endp), &
           soyfixn_to_sminn(bounds%begc:bounds%endc))

    end associate

  end subroutine CNSoyfix

end module CNNDynamicsMod

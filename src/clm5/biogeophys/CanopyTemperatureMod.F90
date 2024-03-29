module CanopyTemperatureMod

  !------------------------------------------------------------------------------
  ! !DESCRIPTION:
  ! CanopyFluxes calculates the leaf temperature and the leaf fluxes,
  ! transpiration, photosynthesis and  updates the dew accumulation due to evaporation.
  ! CanopyTemperature performs calculation of leaf temperature and surface fluxes.
  ! SoilFluxes then determines soil/snow and ground temperatures and updates the surface 
  ! fluxes for the new ground temperature.

  !
  ! !USES:
  use shr_sys_mod          , only : shr_sys_flush
  use shr_kind_mod         , only : r8 => shr_kind_r8
  use shr_log_mod          , only : errMsg => shr_log_errMsg
  use shr_const_mod        , only : SHR_CONST_PI
  use decompMod            , only : bounds_type
  use abortutils           , only : endrun
  use clm_varctl           , only : iulog, use_fates
  use PhotosynthesisMod    , only : Photosynthesis, PhotosynthesisTotal, Fractionation
  use SurfaceResistanceMod , only : calc_soilevap_resis
  use pftconMod            , only : pftcon
  use atm2lndType          , only : atm2lnd_type
  use CanopyStateType      , only : canopystate_type
  use EnergyFluxType       , only : energyflux_type
  use FrictionVelocityMod  , only : frictionvel_type
  use SoilStateType        , only : soilstate_type
  use TemperatureType      , only : temperature_type
  use WaterfluxType        , only : waterflux_type
  use WaterstateType       , only : waterstate_type
  use LandunitType         , only : lun                
  use ColumnType           , only : col                
  use PatchType            , only : patch                
  !
  ! !PUBLIC TYPES:
  implicit none
  save
  !
  ! !PUBLIC MEMBER FUNCTIONS:
  public :: CanopyTemperature  
  !------------------------------------------------------------------------------

contains

  !------------------------------------------------------------------------------
  subroutine CanopyTemperature(bounds, &
       num_nolakec, filter_nolakec, num_nolakep, filter_nolakep, &
       clm_fates, &
       atm2lnd_inst, canopystate_inst, soilstate_inst, frictionvel_inst, &
       waterstate_inst, waterflux_inst, energyflux_inst, temperature_inst )
    !
    ! !DESCRIPTION:
    ! This is the main subroutine to execute the calculation of leaf temperature
    ! and surface fluxes. Subroutine SoilFluxes then determines soil/snow and ground
    ! temperatures and updates the surface fluxes for the new ground temperature.
    !
    ! Calling sequence is:
    ! Biogeophysics1:           surface biogeophysics driver
    !  -> QSat:                 saturated vapor pressure, specific humidity, and
    !                           derivatives at ground surface and derivatives at
    !                           leaf surface using updated leaf temperature
    ! Leaf temperature
    ! Foliage energy conservation is given by the foliage energy budget
    ! equation:
    !                Rnet - Hf - LEf = 0
    ! The equation is solved by Newton-Raphson iteration, in which this
    ! iteration includes the calculation of the photosynthesis and
    ! stomatal resistance, and the integration of turbulent flux profiles.
    ! The sensible and latent heat transfer between foliage and atmosphere
    ! and ground is linked by the equations:
    !                Ha = Hf + Hg and Ea = Ef + Eg
    !
    ! !USES:
    use QSatMod            , only : QSat
    use clm_varcon         , only : denh2o, denice, roverg, hvap, hsub, zlnd, zsno, tfrz, spval 
    use column_varcon      , only : icol_roof, icol_sunwall, icol_shadewall
    use column_varcon      , only : icol_road_imperv, icol_road_perv
    use landunit_varcon    , only : istice_mec, istwet, istsoil, istdlak, istcrop, istdlak
    use clm_varpar         , only : nlevgrnd, nlevurb, nlevsno, nlevsoi
    use clm_varctl         , only : use_fates
    use CLMFatesInterfaceMod, only : hlm_fates_interface_type
    
    !
    ! !ARGUMENTS:
    type(bounds_type)      , intent(in)    :: bounds    
    integer                , intent(in)    :: num_nolakec         ! number of column non-lake points in column filter
    integer                , intent(in)    :: filter_nolakec(:)   ! column filter for non-lake points
    integer                , intent(in)    :: num_nolakep         ! number of column non-lake points in patch filter
    integer                , intent(in)    :: filter_nolakep(:)   ! patch filter for non-lake points
    type(hlm_fates_interface_type), intent(inout)  :: clm_fates
    type(atm2lnd_type)     , intent(in)    :: atm2lnd_inst
    type(canopystate_type) , intent(inout) :: canopystate_inst
    type(soilstate_type)   , intent(inout) :: soilstate_inst
    type(frictionvel_type) , intent(inout) :: frictionvel_inst
    type(waterstate_type)  , intent(inout) :: waterstate_inst
    type(waterflux_type)   , intent(inout) :: waterflux_inst
    type(energyflux_type)  , intent(inout) :: energyflux_inst
    type(temperature_type) , intent(inout) :: temperature_inst
    !
    ! !LOCAL VARIABLES:
    integer  :: g,l,c,p      ! indices
    integer  :: j            ! soil/snow level index
    integer  :: fp           ! lake filter patch index
    integer  :: fc           ! lake filter column index
    real(r8) :: qred         ! soil surface relative humidity
    real(r8) :: avmuir       ! ir inverse optical depth per unit leaf area
    real(r8) :: eg           ! water vapor pressure at temperature T [pa]
    real(r8) :: qsatg        ! saturated humidity [kg/kg]
    real(r8) :: degdT        ! d(eg)/dT
    real(r8) :: qsatgdT      ! d(qsatg)/dT
    real(r8) :: fac          ! soil wetness of surface layer
    real(r8) :: psit         ! negative potential of soil
    real(r8) :: hr           ! alpha soil
    real(r8) :: hr_road_perv ! alpha soil for urban pervious road
    real(r8) :: wx           ! partial volume of ice and water of surface layer
    real(r8) :: fac_fc       ! soil wetness of surface layer relative to field capacity
    real(r8) :: eff_porosity ! effective porosity in layer
    real(r8) :: vol_ice      ! partial volume of ice lens in layer
    real(r8) :: vol_liq      ! partial volume of liquid water in layer
    real(r8) :: fh2o_eff(bounds%begc:bounds%endc) ! effective surface water fraction (i.e. seen by atm)
    !------------------------------------------------------------------------------

    associate(                                                          & 
         snl              =>    col%snl                               , & ! Input:  [integer  (:)   ] number of snow layers                     
         dz               =>    col%dz                                , & ! Input:  [real(r8) (:,:) ] layer depth (m)                        
         zii              =>    col%zii                               , & ! Output: [real(r8) (:)   ] convective boundary height [m]           
         z_0_town         =>    lun%z_0_town                          , & ! Input:  [real(r8) (:)   ] momentum roughness length of urban landunit (m)
         z_d_town         =>    lun%z_d_town                          , & ! Input:  [real(r8) (:)   ] displacement height of urban landunit (m)
         urbpoi           =>    lun%urbpoi                            , & ! Input:  [logical  (:)   ] true => landunit is an urban point       

         z0mr             =>    pftcon%z0mr                           , & ! Input:  ratio of momentum roughness length to canopy top height (-)
         displar          =>    pftcon%displar                        , & ! Input:  ratio of displacement height to canopy top height (-)

         forc_hgt_t       =>    atm2lnd_inst%forc_hgt_t_grc           , & ! Input:  [real(r8) (:)   ] observational height of temperature [m]  
         forc_u           =>    atm2lnd_inst%forc_u_grc               , & ! Input:  [real(r8) (:)   ] atmospheric wind speed in east direction (m/s)
         forc_v           =>    atm2lnd_inst%forc_v_grc               , & ! Input:  [real(r8) (:)   ] atmospheric wind speed in north direction (m/s)
         forc_hgt_u       =>    atm2lnd_inst%forc_hgt_u_grc           , & ! Input:  [real(r8) (:)   ] observational height of wind [m]         
         forc_hgt_q       =>    atm2lnd_inst%forc_hgt_q_grc           , & ! Input:  [real(r8) (:)   ] observational height of specific humidity [m]
         forc_pbot        =>    atm2lnd_inst%forc_pbot_downscaled_col , & ! Input:  [real(r8) (:)   ] atmospheric pressure (Pa)                
         forc_q           =>    atm2lnd_inst%forc_q_downscaled_col    , & ! Input:  [real(r8) (:)   ] atmospheric specific humidity (kg/kg)    
         forc_t           =>    atm2lnd_inst%forc_t_downscaled_col    , & ! Input:  [real(r8) (:)   ] atmospheric temperature (Kelvin)         
         forc_th          =>    atm2lnd_inst%forc_th_downscaled_col   , & ! Input:  [real(r8) (:)   ] atmospheric potential temperature (Kelvin)


         frac_h2osfc      =>    waterstate_inst%frac_h2osfc_col       , & ! Input:  [real(r8) (:)   ] fraction of ground covered by surface water (0 to 1)
         frac_sno_eff     =>    waterstate_inst%frac_sno_eff_col      , & ! Input:  [real(r8) (:)   ] eff. fraction of ground covered by snow (0 to 1)
         frac_sno         =>    waterstate_inst%frac_sno_col          , & ! Input:  [real(r8) (:)   ] fraction of ground covered by snow (0 to 1)
         h2osoi_ice       =>    waterstate_inst%h2osoi_ice_col        , & ! Input:  [real(r8) (:,:) ] ice lens (kg/m2)                       
         h2osoi_liq       =>    waterstate_inst%h2osoi_liq_col        , & ! Input:  [real(r8) (:,:) ] liquid water (kg/m2)                   
         qg_snow          =>    waterstate_inst%qg_snow_col           , & ! Output: [real(r8) (:)   ] specific humidity at snow surface [kg/kg]
         qg_soil          =>    waterstate_inst%qg_soil_col           , & ! Output: [real(r8) (:)   ] specific humidity at soil surface [kg/kg]
         qg               =>    waterstate_inst%qg_col                , & ! Output: [real(r8) (:)   ] ground specific humidity [kg/kg]         
         qg_h2osfc        =>    waterstate_inst%qg_h2osfc_col         , & ! Output: [real(r8) (:)   ]  specific humidity at h2osfc surface [kg/kg]
         dqgdT            =>    waterstate_inst%dqgdT_col             , & ! Output: [real(r8) (:)   ] d(qg)/dT
#ifdef COUP_OAS_PFL
         pfl_psi          =>    waterstate_inst%pfl_psi_col           , & ! Input:  [real(r8) (:,:) ] COUP_OAS_PFL
#endif
         qflx_evap_tot    =>    waterflux_inst%qflx_evap_tot_patch    , & ! Output: [real(r8) (:)   ] qflx_evap_soi + qflx_evap_can + qflx_tran_veg
         qflx_evap_veg    =>    waterflux_inst%qflx_evap_veg_patch    , & ! Output: [real(r8) (:)   ] vegetation evaporation (mm H2O/s) (+ = to atm)
         qflx_tran_veg    =>    waterflux_inst%qflx_tran_veg_patch    , & ! Output: [real(r8) (:)   ] vegetation transpiration (mm H2O/s) (+ = to atm)
         
         htvp             =>    energyflux_inst%htvp_col              , & ! Output: [real(r8) (:)   ] latent heat of vapor of water (or sublimation) [j/kg]
         cgrnd            =>    energyflux_inst%cgrnd_patch           , & ! Output: [real(r8) (:)   ] deriv. of soil energy flux wrt to soil temp [w/m2/k]
         cgrnds           =>    energyflux_inst%cgrnds_patch          , & ! Output: [real(r8) (:)   ] deriv. of soil sensible heat flux wrt soil temp [w/m2/k]
         cgrndl           =>    energyflux_inst%cgrndl_patch          , & ! Output: [real(r8) (:)   ] deriv. of soil latent heat flux wrt soil temp [w/m**2/k]
         eflx_sh_tot      =>    energyflux_inst%eflx_sh_tot_patch     , & ! Output: [real(r8) (:)   ] total sensible heat flux (W/m**2) [+ to atm]
         eflx_sh_tot_r    =>    energyflux_inst%eflx_sh_tot_r_patch   , & ! Output: [real(r8) (:)   ] rural total sensible heat flux (W/m**2) [+ to atm]
         eflx_lh_tot_u    =>    energyflux_inst%eflx_lh_tot_u_patch   , & ! Output: [real(r8) (:)   ] urban total latent heat flux (W/m**2)  [+ to atm]
         eflx_lh_tot      =>    energyflux_inst%eflx_lh_tot_patch     , & ! Output: [real(r8) (:)   ] total latent heat flux (W/m**2)  [+ to atm]
         eflx_lh_tot_r    =>    energyflux_inst%eflx_lh_tot_r_patch   , & ! Output: [real(r8) (:)   ] rural total latent heat flux (W/m**2)  [+ to atm]
         eflx_sh_tot_u    =>    energyflux_inst%eflx_sh_tot_u_patch   , & ! Output: [real(r8) (:)   ] urban total sensible heat flux (W/m**2) [+ to atm]
         eflx_sh_veg      =>    energyflux_inst%eflx_sh_veg_patch     , & ! Output: [real(r8) (:)   ] sensible heat flux from leaves (W/m**2) [+ to atm]

         forc_hgt_t_patch =>    frictionvel_inst%forc_hgt_t_patch     , & ! Input:  [real(r8) (:)   ] observational height of temperature at patch level [m]
         forc_hgt_q_patch =>    frictionvel_inst%forc_hgt_q_patch     , & ! Input:  [real(r8) (:)   ] observational height of specific humidity at patch level [m]
         z0m              =>    frictionvel_inst%z0m_patch            , & ! Output: [real(r8) (:)   ] momentum roughness length (m)            
         z0mv             =>    frictionvel_inst%z0mv_patch           , & ! Output: [real(r8) (:)   ] roughness length over vegetation, momentum [m]
         z0hv             =>    frictionvel_inst%z0hv_patch           , & ! Output: [real(r8) (:)   ] roughness length over vegetation, sensible heat [m]
         z0qv             =>    frictionvel_inst%z0qv_patch           , & ! Output: [real(r8) (:)   ] roughness length over vegetation, latent heat [m]
         z0hg             =>    frictionvel_inst%z0hg_col             , & ! Output: [real(r8) (:)   ] roughness length over ground, sensible heat [m]
         z0mg             =>    frictionvel_inst%z0mg_col             , & ! Output: [real(r8) (:)   ] roughness length over ground, momentum [m]
         z0qg             =>    frictionvel_inst%z0qg_col             , & ! Output: [real(r8) (:)   ] roughness length over ground, latent heat [m]
         forc_hgt_u_patch =>    frictionvel_inst%forc_hgt_u_patch     , & ! Output: [real(r8) (:)   ] observational height of wind at patch level [m]

         frac_veg_nosno   =>    canopystate_inst%frac_veg_nosno_patch , & ! Input:  [integer  (:)   ] fraction of vegetation not covered by snow (0 OR 1) [-]
         elai             =>    canopystate_inst%elai_patch           , & ! Input:  [real(r8) (:)   ] one-sided leaf area index with burying by snow
         esai             =>    canopystate_inst%esai_patch           , & ! Input:  [real(r8) (:)   ] one-sided stem area index with burying by snow
         htop             =>    canopystate_inst%htop_patch           , & ! Input:  [real(r8) (:)   ] canopy top (m)                           
         displa           =>    canopystate_inst%displa_patch         , & ! Output: [real(r8) (:)   ] displacement height (m)                  

         smpmin           =>    soilstate_inst%smpmin_col             , & ! Input:  [real(r8) (:)   ] restriction for min of soil potential (mm)
         sucsat           =>    soilstate_inst%sucsat_col             , & ! Input:  [real(r8) (:,:) ] minimum soil suction (mm)              
         watsat           =>    soilstate_inst%watsat_col             , & ! Input:  [real(r8) (:,:) ] volumetric soil water at saturation (porosity)
         watfc            =>    soilstate_inst%watfc_col              , & ! Input:  [real(r8) (:,:) ] volumetric soil water at field capacity
         watdry           =>    soilstate_inst%watdry_col             , & ! Input:  [real(r8) (:,:) ] volumetric soil moisture corresponding to no restriction on ET from urban pervious surface
         watopt           =>    soilstate_inst%watopt_col             , & ! Input:  [real(r8) (:,:) ] volumetric soil moisture corresponding to no restriction on ET from urban pervious surface
         bsw              =>    soilstate_inst%bsw_col                , & ! Input:  [real(r8) (:,:) ] Clapp and Hornberger "b"               
         rootfr_road_perv =>    soilstate_inst%rootfr_road_perv_col   , & ! Input:  [real(r8) (:,:) ] fraction of roots in each soil layer for urban pervious road
         rootr_road_perv  =>    soilstate_inst%rootr_road_perv_col    , & ! Input:  [real(r8) (:,:) ] effective fraction of roots in each soil layer for urban pervious road
         soilalpha        =>    soilstate_inst%soilalpha_col          , & ! Output: [real(r8) (:)   ] factor that reduces ground saturated specific humidity (-)
         soilalpha_u      =>    soilstate_inst%soilalpha_u_col        , & ! Output: [real(r8) (:)   ] Urban factor that reduces ground saturated specific humidity (-)
         
         t_h2osfc         =>    temperature_inst%t_h2osfc_col         , & ! Input:  [real(r8) (:)   ] surface water temperature               
         t_soisno         =>    temperature_inst%t_soisno_col         , & ! Input:  [real(r8) (:,:) ] soil temperature (Kelvin)              
         beta             =>    temperature_inst%beta_col             , & ! Output: [real(r8) (:)   ] coefficient of convective velocity [-]   
         emg              =>    temperature_inst%emg_col              , & ! Output: [real(r8) (:)   ] ground emissivity                        
         emv              =>    temperature_inst%emv_patch            , & ! Output: [real(r8) (:)   ] vegetation emissivity                    
         t_h2osfc_bef     =>    temperature_inst%t_h2osfc_bef_col     , & ! Output: [real(r8) (:)   ] saved surface water temperature         
         t_grnd           =>    temperature_inst%t_grnd_col           , & ! Output: [real(r8) (:)   ] ground temperature (Kelvin)              
         thv              =>    temperature_inst%thv_col              , & ! Output: [real(r8) (:)   ] virtual potential temperature (kelvin)   
         thm              =>    temperature_inst%thm_patch            , & ! Output: [real(r8) (:)   ] intermediate variable (forc_t+0.0098*forc_hgt_t_patch)
         tssbef           =>    temperature_inst%t_ssbef_col            & ! Output: [real(r8) (:,:) ] soil/snow temperature before update    
         )

      do j = -nlevsno+1, nlevgrnd
         do fc = 1,num_nolakec
            c = filter_nolakec(fc)
            if ((col%itype(c) == icol_sunwall .or. col%itype(c) == icol_shadewall &
                 .or. col%itype(c) == icol_roof) .and. j > nlevurb) then
               tssbef(c,j) = spval 
            else
               tssbef(c,j) = t_soisno(c,j)
            end if
            ! record t_h2osfc prior to updating
            t_h2osfc_bef(c) = t_h2osfc(c)   
         end do
      end do

      ! calculate moisture stress/resistance for soil evaporation
      call calc_soilevap_resis(bounds, num_nolakec, filter_nolakec, soilstate_inst, waterstate_inst, temperature_inst)

      do fc = 1,num_nolakec
         c = filter_nolakec(fc)
         l = col%landunit(c)

         if (col%itype(c) == icol_road_perv) then
            hr_road_perv = 0._r8
         end if

         ! begin calculations that relate only to the column level
         ! Ground and soil temperatures from previous time step

         ! ground temperature is weighted average of exposed soil, snow, and h2osfc
         if (snl(c) < 0) then
            t_grnd(c) = frac_sno_eff(c) * t_soisno(c,snl(c)+1) &
                 + (1.0_r8 - frac_sno_eff(c) - frac_h2osfc(c)) * t_soisno(c,1) &
                 + frac_h2osfc(c) * t_h2osfc(c)
         else
            t_grnd(c) = (1 - frac_h2osfc(c)) * t_soisno(c,1) + frac_h2osfc(c) * t_h2osfc(c)
         endif

         ! Saturated vapor pressure, specific humidity and their derivatives
         ! at ground surface
         qred = 1._r8
         if (lun%itype(l)/=istwet .AND. lun%itype(l)/=istice_mec) then

            if (lun%itype(l) == istsoil .or. lun%itype(l) == istcrop) then
               wx   = (h2osoi_liq(c,1)/denh2o+h2osoi_ice(c,1)/denice)/dz(c,1)
               fac  = min(1._r8, wx/watsat(c,1))
               fac  = max( fac, 0.01_r8 )
#ifdef COUP_OAS_PFL
               ! clm3.5/bld/usr.src/Biogeophysics1Mod.F90
               if (pfl_psi(c,1)>= 0.0_r8)  psit = 0._r8
               if (pfl_psi(c,1) < 0.0_r8)  psit = pfl_psi(c,1)
#else
               psit = -sucsat(c,1) * fac ** (-bsw(c,1))
               psit = max(smpmin(c), psit)
#endif
               ! modify qred to account for h2osfc
               hr   = exp(psit/roverg/t_soisno(c,1))
               qred = (1._r8 - frac_sno(c) - frac_h2osfc(c))*hr &
                    + frac_sno(c) + frac_h2osfc(c)
               soilalpha(c) = qred

            else if (col%itype(c) == icol_road_perv) then
               ! Pervious road depends on water in total soil column
               do j = 1, nlevsoi
                  if (t_soisno(c,j) >= tfrz) then
                     vol_ice = min(watsat(c,j), h2osoi_ice(c,j)/(dz(c,j)*denice))
                     eff_porosity = watsat(c,j)-vol_ice
                     vol_liq = min(eff_porosity, h2osoi_liq(c,j)/(dz(c,j)*denh2o))
                     fac = min( max(vol_liq-watdry(c,j),0._r8) / (watopt(c,j)-watdry(c,j)), 1._r8 )
                  else
                     fac = 0._r8
                  end if
                  rootr_road_perv(c,j) = rootfr_road_perv(c,j)*fac
                  hr_road_perv = hr_road_perv + rootr_road_perv(c,j)
               end do
               ! Allows for sublimation of snow or dew on snow
               qred = (1.-frac_sno(c))*hr_road_perv + frac_sno(c)

               ! Normalize root resistances to get layer contribution to total ET
               if (hr_road_perv > 0._r8) then
                  do j = 1, nlevsoi
                     rootr_road_perv(c,j) = rootr_road_perv(c,j)/hr_road_perv
                  end do
               end if
               soilalpha_u(c) = qred

            else if (col%itype(c) == icol_sunwall .or. col%itype(c) == icol_shadewall) then
               qred = 0._r8
               soilalpha_u(c) = spval

            else if (col%itype(c) == icol_roof .or. col%itype(c) == icol_road_imperv) then
               qred = 1._r8
               soilalpha_u(c) = spval
            end if

         else
            soilalpha(c) = spval

         end if

         ! compute humidities individually for snow, soil, h2osfc for vegetated landunits
         if (lun%itype(l) == istsoil .or. lun%itype(l) == istcrop) then

            call QSat(t_soisno(c,snl(c)+1), forc_pbot(c), eg, degdT, qsatg, qsatgdT)
            if (qsatg > forc_q(c) .and. forc_q(c) > qsatg) then
               qsatg = forc_q(c)
               qsatgdT = 0._r8
            end if

            qg_snow(c) = qsatg
            dqgdT(c) = frac_sno(c)*qsatgdT

            call QSat(t_soisno(c,1) , forc_pbot(c), eg, degdT, qsatg, qsatgdT)
            if (qsatg > forc_q(c) .and. forc_q(c) > hr*qsatg) then
               qsatg = forc_q(c)
               qsatgdT = 0._r8
            end if
            qg_soil(c) = hr*qsatg
            dqgdT(c) = dqgdT(c) + (1._r8 - frac_sno(c) - frac_h2osfc(c))*hr*qsatgdT

            ! to be consistent with hs_top values in SoilTemp, set qg_snow to qg_soil for snl = 0 case
            ! this ensures hs_top_snow will equal hs_top_soil
            if (snl(c) >= 0) then
               qg_snow(c) = qg_soil(c)
               dqgdT(c) = (1._r8 - frac_h2osfc(c))*hr*dqgdT(c)
            endif

            call QSat(t_h2osfc(c), forc_pbot(c), eg, degdT, qsatg, qsatgdT)
            if (qsatg > forc_q(c) .and. forc_q(c) > qsatg) then
               qsatg = forc_q(c)
               qsatgdT = 0._r8
            end if
            qg_h2osfc(c) = qsatg
            dqgdT(c) = dqgdT(c) + frac_h2osfc(c) * qsatgdT

            !          qg(c) = frac_sno(c)*qg_snow(c) + (1._r8 - frac_sno(c) - frac_h2osfc(c))*qg_soil(c) &
            qg(c) = frac_sno_eff(c)*qg_snow(c) + (1._r8 - frac_sno_eff(c) - frac_h2osfc(c))*qg_soil(c) &
                 + frac_h2osfc(c) * qg_h2osfc(c)

         else
            call QSat(t_grnd(c), forc_pbot(c), eg, degdT, qsatg, qsatgdT)
            qg(c) = qred*qsatg
            dqgdT(c) = qred*qsatgdT

            if (qsatg > forc_q(c) .and. forc_q(c) > qred*qsatg) then
               qg(c) = forc_q(c)
               dqgdT(c) = 0._r8
            end if

            qg_snow(c) = qg(c)
            qg_soil(c) = qg(c)
            qg_h2osfc(c) = qg(c)
         endif

         ! Ground emissivity - only calculate for non-urban landunits 
         ! Urban emissivities are currently read in from data file

         if (.not. urbpoi(l)) then
            if (lun%itype(l)==istice_mec) then
               emg(c) = 0.97_r8
            else
               emg(c) = (1._r8-frac_sno(c))*0.96_r8 + frac_sno(c)*0.97_r8
            end if
         end if

         ! Latent heat. We arbitrarily assume that the sublimation occurs
         ! only as h2osoi_liq = 0

         htvp(c) = hvap
         if (h2osoi_liq(c,snl(c)+1) <= 0._r8 .and. h2osoi_ice(c,snl(c)+1) > 0._r8) htvp(c) = hsub

         ! Ground roughness lengths over non-lake columns (includes bare ground, ground
         ! underneath canopy, wetlands, etc.)

         if (frac_sno(c) > 0._r8) then
            z0mg(c) = zsno
         else
            z0mg(c) = zlnd
         end if
         z0hg(c) = z0mg(c)            ! initial set only
         z0qg(c) = z0mg(c)            ! initial set only

         ! Potential, virtual potential temperature, and wind speed at the
         ! reference height

         beta(c) = 1._r8
         zii(c)  = 1000._r8
         thv(c)  = forc_th(c)*(1._r8+0.61_r8*forc_q(c))

      end do ! (end of columns loop)


      ! Set roughness and displacement
      ! Note that FATES passes back z0m and displa at the end
      ! of its dynamics call.  If and when crops are
      ! enabled simultaneously with FATES, we will 
      ! have to apply a filter here.
      if(use_fates) then
         call clm_fates%TransferZ0mDisp(bounds,frictionvel_inst,canopystate_inst)
      end if

      do fp = 1,num_nolakep
         p = filter_nolakep(fp)
         if( .not.(patch%is_fates(p))) then
            z0m(p)    = z0mr(patch%itype(p)) * htop(p)
            displa(p) = displar(patch%itype(p)) * htop(p)
         end if
      end do

      ! Initialization
      do fp = 1,num_nolakep
         p = filter_nolakep(fp)

         ! Initial set (needed for history tape fields)

         eflx_sh_tot(p) = 0._r8
         l = patch%landunit(p)
         if (urbpoi(l)) then
            eflx_sh_tot_u(p) = 0._r8
         else if (lun%itype(l) == istsoil .or. lun%itype(l) == istcrop) then 
            eflx_sh_tot_r(p) = 0._r8
         end if
         eflx_lh_tot(p) = 0._r8
         if (urbpoi(l)) then
            eflx_lh_tot_u(p) = 0._r8
         else if (lun%itype(l) == istsoil .or. lun%itype(l) == istcrop) then 
            eflx_lh_tot_r(p) = 0._r8
         end if
         eflx_sh_veg(p) = 0._r8
         qflx_evap_tot(p) = 0._r8
         qflx_evap_veg(p) = 0._r8
         qflx_tran_veg(p) = 0._r8

         ! Initial set for calculation

         cgrnd(p)  = 0._r8
         cgrnds(p) = 0._r8
         cgrndl(p) = 0._r8

         ! Vegetation Emissivity

         avmuir = 1._r8
         emv(p) = 1._r8-exp(-(elai(p)+esai(p))/avmuir)

         ! Roughness lengths over vegetation

         z0mv(p)   = z0m(p)
         z0hv(p)   = z0mv(p)
         z0qv(p)   = z0mv(p)
      end do

      ! Make forcing height a patch-level quantity that is the atmospheric forcing 
      ! height plus each patch's z0m+displa
      do p = bounds%begp,bounds%endp
         if (patch%active(p)) then
            g = patch%gridcell(p)
            l = patch%landunit(p)
            c = patch%column(p)
            if (lun%itype(l) == istsoil .or. lun%itype(l) == istcrop) then
               if (frac_veg_nosno(p) == 0) then
                  forc_hgt_u_patch(p) = forc_hgt_u(g) + z0mg(c) + displa(p)
                  forc_hgt_t_patch(p) = forc_hgt_t(g) + z0mg(c) + displa(p)
                  forc_hgt_q_patch(p) = forc_hgt_q(g) + z0mg(c) + displa(p)
               else
                  forc_hgt_u_patch(p) = forc_hgt_u(g) + z0m(p) + displa(p)
                  forc_hgt_t_patch(p) = forc_hgt_t(g) + z0m(p) + displa(p)
                  forc_hgt_q_patch(p) = forc_hgt_q(g) + z0m(p) + displa(p)
               end if
            else if (lun%itype(l) == istwet .or. lun%itype(l) == istice_mec) then
               forc_hgt_u_patch(p) = forc_hgt_u(g) + z0mg(c)
               forc_hgt_t_patch(p) = forc_hgt_t(g) + z0mg(c)
               forc_hgt_q_patch(p) = forc_hgt_q(g) + z0mg(c)
               ! Appropriate momentum roughness length will be added in LakeFLuxesMod.
            else if (lun%itype(l) == istdlak) then
               forc_hgt_u_patch(p) = forc_hgt_u(g)
               forc_hgt_t_patch(p) = forc_hgt_t(g)
               forc_hgt_q_patch(p) = forc_hgt_q(g)
            else if (urbpoi(l)) then
               forc_hgt_u_patch(p) = forc_hgt_u(g) + z_0_town(l) + z_d_town(l)
               forc_hgt_t_patch(p) = forc_hgt_t(g) + z_0_town(l) + z_d_town(l)
               forc_hgt_q_patch(p) = forc_hgt_q(g) + z_0_town(l) + z_d_town(l)
            end if
         end if
      end do

      do fp = 1,num_nolakep
         p = filter_nolakep(fp)
         c = patch%column(p)

         thm(p)  = forc_t(c) + 0.0098_r8*forc_hgt_t_patch(p)
      end do

    end associate

  end subroutine CanopyTemperature

end module CanopyTemperatureMod

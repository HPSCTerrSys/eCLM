module oas_sendReceiveMod
  use shr_kind_mod     , only: r8 => shr_kind_r8
  use clm_time_manager , only: get_nstep, get_step_size
  use decompMod        , only: bounds_type
  use clm_varpar       , only: nlevgrnd
  use clm_varctl       , only: iulog
  use oas_vardefMod
  use mod_oasis
  implicit none
  save
  private

#ifdef COUP_OAS_PFL
  public  :: oas_send
  public  :: oas_receive
#endif

#ifdef COUP_OAS_ICON
  public  :: oas_send_icon
  public  :: oas_receive_icon
#endif 

contains

#ifdef COUP_OAS_PFL
  subroutine oas_receive(bounds, seconds_elapsed, atm2lnd_inst)
    use atm2lndType, only: atm2lnd_type

    type(bounds_type),  intent(in)    :: bounds
    integer          ,  intent(in)    :: seconds_elapsed
    type(atm2lnd_type), intent(inout) :: atm2lnd_inst
    integer                           :: info

    call oasis_get(oas_psi_id, seconds_elapsed, atm2lnd_inst%pfl_psi_grc, info)
    call oasis_get(oas_sat_id, seconds_elapsed, atm2lnd_inst%pfl_h2osoi_liq_grc, info)

  end subroutine oas_receive

  subroutine oas_send(bounds, seconds_elapsed, lnd2atm_inst)
    use lnd2atmType, only : lnd2atm_type
    use spmdMod,     only : mpicom
    use shr_mpi_mod, only: shr_mpi_barrier

    type(bounds_type),  intent(in)    :: bounds
    integer          ,  intent(in)    :: seconds_elapsed
    type(lnd2atm_type), intent(inout) :: lnd2atm_inst

    integer                           :: info
    
    call oasis_put(oas_et_loss_id, seconds_elapsed, lnd2atm_inst%qflx_parflow_grc, info)
    
  end subroutine oas_send
#endif

#ifdef COUP_OAS_ICON
  subroutine oas_receive_icon(bounds, seconds_elapsed, atm2lnd_inst)
    use atm2lndType, only: atm2lnd_type

    type(bounds_type),  intent(in)    :: bounds
    integer          ,  intent(in)    :: seconds_elapsed
    type(atm2lnd_type), intent(inout) :: atm2lnd_inst
    real(kind=r8),      allocatable   :: buffer(:,:)
    integer                           :: num_grid_points
    integer                           :: info
    integer                           :: g


    num_grid_points = (bounds%endg - bounds%begg) + 1
    allocate(buffer(num_grid_points, 1))

    !    call oasis_get(oas_id_t, seconds_elapsed, oas_rcv_meta(:,:,oas_id_t), info)
    call oasis_get(oas_id_t,  seconds_elapsed, atm2lnd_inst%forc_t_not_downscaled_grc, info)
    call oasis_get(oas_id_u,  seconds_elapsed, atm2lnd_inst%forc_u_grc, info)
    call oasis_get(oas_id_v,  seconds_elapsed, atm2lnd_inst%forc_v_grc, info)
    call oasis_get(oas_id_qv, seconds_elapsed, atm2lnd_inst%forc_q_not_downscaled_grc, info)
    call oasis_get(oas_id_ht, seconds_elapsed, atm2lnd_inst%forc_hgt_grc, info)
    call oasis_get(oas_id_pr, seconds_elapsed, atm2lnd_inst%forc_pbot_not_downscaled_grc, info)
    call oasis_get(oas_id_rs, seconds_elapsed, atm2lnd_inst%forc_solad_grc(:,1), info)
    call oasis_get(oas_id_fs, seconds_elapsed, atm2lnd_inst%forc_solai_grc(:,1), info)
    call oasis_get(oas_id_lw, seconds_elapsed, atm2lnd_inst%forc_lwrad_not_downscaled_grc, info)
    call oasis_get(oas_id_cr, seconds_elapsed, atm2lnd_inst%forc_rain_not_downscaled_grc, info)
    call oasis_get(oas_id_gr, seconds_elapsed, atm2lnd_inst%forc_snow_not_downscaled_grc, info)

    !SPo: some postprocessing of atm2lnd is missing; may better use x2l 

    do g=bounds%begg,bounds%endg
       atm2lnd_inst%forc_solad_grc(g,1) = 0.5_r8 * atm2lnd_inst%forc_solad_grc(g,1)
       atm2lnd_inst%forc_solad_grc(g,2) = atm2lnd_inst%forc_solad_grc(g,1)
       atm2lnd_inst%forc_solai_grc(g,1) = 0.5_r8 * atm2lnd_inst%forc_solai_grc(g,1)
       atm2lnd_inst%forc_solai_grc(g,2) = atm2lnd_inst%forc_solai_grc(g,1)
       atm2lnd_inst%forc_solar_grc(g)   =  atm2lnd_inst%forc_solad_grc(g,2) + atm2lnd_inst%forc_solad_grc(g,1) &
                                        +  atm2lnd_inst%forc_solai_grc(g,2) + atm2lnd_inst%forc_solai_grc(g,1)
    enddo

  end subroutine oas_receive_icon

  subroutine oas_send_icon(bounds, seconds_elapsed, lnd2atm_inst)
    use lnd2atmType, only : lnd2atm_type
    use spmdMod,     only : mpicom
    use shr_mpi_mod, only: shr_mpi_barrier

    type(bounds_type),  intent(in)    :: bounds
    integer          ,  intent(in)    :: seconds_elapsed
    type(lnd2atm_type), intent(inout) :: lnd2atm_inst
    real(kind=r8),      allocatable   :: aux_buffer(:,:)
    integer                           :: num_grid_points
    integer                           :: info

    num_grid_points = (bounds%endg - bounds%begg) + 1
    allocate(aux_buffer(num_grid_points, 1))

     call oasis_put(oas_id_it, seconds_elapsed,lnd2atm_inst%t_rad_grc, info)         ! "CLM_INFRA"
     call oasis_put(oas_id_ad, seconds_elapsed,lnd2atm_inst%albd_grc(:,1), info)     ! "CLM_ALBED"
     call oasis_put(oas_id_ai, seconds_elapsed,lnd2atm_inst%albi_grc(:,1), info)     ! "CLM_ALBEI"
     call oasis_put(oas_id_tx, seconds_elapsed,lnd2atm_inst%taux_grc, info)          ! "CLM_TAUX"
     call oasis_put(oas_id_ty, seconds_elapsed,lnd2atm_inst%tauy_grc, info)          ! "CLM_TAUY"
     call oasis_put(oas_id_sh, seconds_elapsed,lnd2atm_inst%eflx_sh_tot_grc, info)   ! "CLM_SHFLX"
     call oasis_put(oas_id_lh, seconds_elapsed,lnd2atm_inst%eflx_lh_tot_grc, info)   ! "CLM_LHFLX"
     call oasis_put(oas_id_st, seconds_elapsed,lnd2atm_inst%t_sf_grc, info)          ! "CLM_TGRND"

  end subroutine oas_send_icon
#endif

end module oas_sendReceiveMod

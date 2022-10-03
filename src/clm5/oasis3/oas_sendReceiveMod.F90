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

  public  :: oas_send
  public  :: oas_receive
  
contains

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

end module oas_sendReceiveMod

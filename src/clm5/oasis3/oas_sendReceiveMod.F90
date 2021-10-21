module oas_sendReceiveMod
  use shr_kind_mod     , only: r8 => shr_kind_r8
  use clm_time_manager , only: get_nstep, get_step_size
  use decompMod        , only: bounds_type
  use clm_varpar       , only: nlevsoi
  use oas_vardefMod
  use mod_oasis
  implicit none
  save
  private

  public  :: oas_send
  public  :: oas_receive
  
contains

  subroutine oas_receive(bounds, atm2lnd_inst)
    use atm2lndType, only: atm2lnd_type

    type(bounds_type),  intent(in)    :: bounds
    type(atm2lnd_type), intent(inout) :: atm2lnd_inst
    real(kind=r8),      allocatable   :: buffer(:)
    integer                           :: num_grid_points
    integer                           :: dtime, seconds_elapsed
    integer                           :: i, ierror

    num_grid_points = (bounds%endg - bounds%begg) + 1
    allocate(buffer(num_grid_points))

    dtime = get_step_size() ! timestep size [seconds]
    seconds_elapsed = dtime * (get_nstep() - 1)

    do i = 1, nlevsoi
      call oasis_get(psi(i)%id, seconds_elapsed, buffer, ierror)
      atm2lnd_inst%parflow_psi_grc(:,i) = buffer
    end do
  end subroutine oas_receive

  subroutine oas_send(bounds, lnd2atm_inst)
    use lnd2atmType, only : lnd2atm_type

    type(bounds_type),  intent(in)    :: bounds
    type(lnd2atm_type), intent(inout) :: lnd2atm_inst
    real(kind=r8),      allocatable   :: buffer(:)
    integer                           :: num_grid_points
    integer                           :: dtime, seconds_elapsed
    integer                           :: i, ierror

    num_grid_points = (bounds%endg - bounds%begg) + 1
    allocate(buffer(num_grid_points))

    dtime = get_step_size() ! timestep size [seconds]
    seconds_elapsed = dtime * get_nstep()

    do i = 1, nlevsoi
      buffer = lnd2atm_inst%qflx_parflow_grc(:,i)
      call oasis_put(et_loss(i)%id, seconds_elapsed, buffer, ierror)
    end do
  end subroutine oas_send

end module oas_sendReceiveMod

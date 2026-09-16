module pfl2lndType

  !-----------------------------------------------------------------------
  ! !DESCRIPTION:
  ! Handle pfl2lnd, lnd2pfl mapping
  !
  ! !USES:
  use shr_kind_mod  , only : r8 => shr_kind_r8
  use shr_infnan_mod, only : nan => shr_infnan_nan, assignment(=)
  use shr_log_mod   , only : errMsg => shr_log_errMsg
  use clm_varpar    , only : numrad, ndst, nlevgrnd, nlevsoi !ndst = number of dust bins.
  use clm_varcon    , only : spval
  use clm_varctl    , only : iulog
  use decompMod     , only : bounds_type
  use abortutils    , only : endrun
  !
  ! !PUBLIC TYPES:
  implicit none
  private
  save
  !
  ! !PUBLIC DATA TYPES:

  !----------------------------------------------------
  ! parflow -> land variables structure
  !
  !----------------------------------------------------
  type, public :: pfl2lnd_type

     ! parflow->lnd not downscaled
     real(r8), pointer :: pfl_psi_grc                   (:,:) => null() ! Parflow soil matrix potential [mm]
     real(r8), pointer :: pfl_h2osoi_liq_grc            (:,:) => null() ! Parflow H2O soil liquid       [mm]
     real(r8), pointer :: pfl_porosity_grc              (:,:) => null() ! Parflow porosity              [m^3/m^3]

   contains

     procedure, public  :: Init
     procedure, private :: InitAllocate
     procedure, private :: InitHistory
     !procedure, public  :: Restart
     procedure, public  :: Clean

  end type pfl2lnd_type

  character(len=*), parameter, private :: sourcefile = &
       __FILE__
  !----------------------------------------------------

contains

  !------------------------------------------------------------------------
  subroutine Init(this, bounds)

    class(pfl2lnd_type) :: this
    type(bounds_type), intent(in) :: bounds

    call this%InitAllocate(bounds)
    call this%InitHistory(bounds)

  end subroutine Init

  !------------------------------------------------------------------------
  subroutine InitAllocate(this, bounds)
    !
    ! !DESCRIPTION:
    ! Initialize atm2lnd derived type
    !
    ! !ARGUMENTS:
    class(pfl2lnd_type) :: this
    type(bounds_type), intent(in) :: bounds
    !
    ! !LOCAL VARIABLES:
    real(r8) :: ival  = 0.0_r8  ! initial value
    integer  :: begg, endg
    !------------------------------------------------------------------------

    begg = bounds%begg; endg= bounds%endg

    ! parflow->lnd
    allocate(this%pfl_psi_grc                   (begg:endg,1:nlevgrnd)); this%pfl_psi_grc            (:,:) = spval
    allocate(this%pfl_h2osoi_liq_grc            (begg:endg,1:nlevgrnd)); this%pfl_h2osoi_liq_grc     (:,:) = spval
    allocate(this%pfl_porosity_grc              (begg:endg,1:nlevgrnd)); this%pfl_porosity_grc       (:,:) = spval

  end subroutine InitAllocate

  !------------------------------------------------------------------------
  subroutine InitHistory(this, bounds)
    use histFileMod, only : hist_addfld1d, hist_addfld2d
    !
    ! !ARGUMENTS:
    class(pfl2lnd_type) :: this
    type(bounds_type), intent(in) :: bounds
    !
    ! !LOCAL VARIABLES:
    integer  :: begg, endg
    !---------------------------------------------------------------------

    begg = bounds%begg; endg= bounds%endg

    this%pfl_psi_grc(begg:endg, :) = spval
    call hist_addfld2d (fname='PFL_PSI_GRC', units='mm', type2d='levgrnd', &
      avgflag='A', long_name='Parflow pressure head (gridcell)', &
      ptr_lnd=this%pfl_psi_grc, default='inactive')

    this%pfl_h2osoi_liq_grc(begg:endg, :) = spval
    call hist_addfld2d (fname='PFL_SOILLIQ_GRC', units='mm', type2d='levgrnd', &
      avgflag='A', long_name='Parflow H2O soil liquid (gridcell)', &
      ptr_lnd=this%pfl_h2osoi_liq_grc, default='inactive')

    this%pfl_porosity_grc(begg:endg, :) = spval
    call hist_addfld2d (fname='PFL_POROSITY_GRC', units='m^3/m^3', type2d='levgrnd', &
      avgflag='A', long_name='Parflow porosity (gridcell)', &
      ptr_lnd=this%pfl_porosity_grc, default='inactive')
  end subroutine InitHistory

  !------------------------------------------------------------------------
  !subroutine Restart()
    !
    ! Any Parflow fields that need to be in the restart file?
    ! This empty subroutine is a reminder to revisit this question in the future.
    !
  !end subroutine Restart

  !-----------------------------------------------------------------------
  subroutine Clean(this)
    !
    ! ARGUMENTS:
    class(pfl2lnd_type), intent(inout) :: this
    !
    ! LOCAL VARIABLES:

    character(len=*), parameter :: subname = 'Clean'
    !-----------------------------------------------------------------------
    deallocate(this%pfl_psi_grc)
    deallocate(this%pfl_h2osoi_liq_grc)
    deallocate(this%pfl_porosity_grc)

  end subroutine Clean


end module pfl2lndType

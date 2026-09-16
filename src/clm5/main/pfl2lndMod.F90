module pfl2lndMod

  !-----------------------------------------------------------------------
  ! !DESCRIPTION:
  ! Handle Parflow fields
  !
  ! !USES:
  use shr_kind_mod   , only : r8 => shr_kind_r8
  use shr_infnan_mod , only : nan => shr_infnan_nan, assignment(=)
  use shr_log_mod    , only : errMsg => shr_log_errMsg
  use clm_varpar     , only : nlevgrnd
  use clm_varctl     , only : iulog
  use abortutils     , only : endrun
  use decompMod      , only : bounds_type
  use filterMod      , only : clumpfilter
  use ColumnType     , only : col

  !
  ! !PUBLIC TYPES:
  implicit none
  private
  save
  !
  ! !PUBLIC MEMBER FUNCTIONS:
  public :: downscale_parflow_fields
  public :: import_parflow_porosity

  character(len=*), parameter, private :: sourcefile = &
       __FILE__
  !-----------------------------------------------------------------------

contains

  !-----------------------------------------------------------------------
  subroutine downscale_parflow_fields(bounds, filter, pfl2lnd_inst, waterstate_inst)
    !
    ! !DESCRIPTION:
    ! Downscale Parflow fields from gridcell to column.
    !
    use pfl2lndType       , only : pfl2lnd_type
    use WaterStateType    , only : waterstate_type
    !
    ! !ARGUMENTS:
    type(bounds_type)     , intent(in)    :: bounds
    type(clumpfilter)     , intent(inout) :: filter
    type(pfl2lnd_type)    , intent(inout) :: pfl2lnd_inst
    type(waterstate_type) , intent(inout) :: waterstate_inst
    !
    ! !LOCAL VARIABLES:
    integer :: f, c, g         ! indices
    integer :: clo, cc

    character(len=*), parameter :: subname = 'downscale_parflow_fields'
    !-----------------------------------------------------------------------

    associate(&
         ! Gridcell-level non-downscaled fields:
         pfl_psi_g          => pfl2lnd_inst%pfl_psi_grc           , & ! Grid-level ParFlow pressure head       [mm]
         pfl_h2osoi_liq_g   => pfl2lnd_inst%pfl_h2osoi_liq_grc    , & ! Grid-level ParFlow soil liquid water   [mm]
         pfl_psi_c          => waterstate_inst%pfl_psi_col        , & ! Column-level ParFlow pressure head     [mm]
         pfl_h2osoi_liq_c   => waterstate_inst%pfl_h2osoi_liq_col   & ! Column-level ParFlow soil liquid water [mm]
         )

     do f = 1, filter%num_nolakec
       c = filter%nolakec(f)
       if (col%hydrologically_active(c)) then
          g = col%gridcell(c)
          pfl_psi_c(c,:) = pfl_psi_g(g,:)
          pfl_h2osoi_liq_c(c,:) = pfl_h2osoi_liq_g(g,:)
       end if
     end do
    end associate
  end subroutine downscale_parflow_fields

  !-----------------------------------------------------------------------
  subroutine import_parflow_porosity(bounds, filter, pfl2lnd_inst, soilstate_inst)
    !
    ! !DESCRIPTION:
    ! Downscale Parflow fields from gridcell to column.
    !
    use pfl2lndType       , only : pfl2lnd_type
    use SoilStateType     , only : soilstate_type
    !
    ! !ARGUMENTS:
    type(bounds_type)     , intent(in)    :: bounds
    type(clumpfilter)     , intent(inout) :: filter
    type(pfl2lnd_type)    , intent(inout) :: pfl2lnd_inst
    type(soilstate_type)  , intent(inout) :: soilstate_inst
    !
    ! !LOCAL VARIABLES:
    integer :: f, c, g         ! indices
    integer :: clo, cc

    character(len=*), parameter :: subname = 'downscale_parflow_fields'
    !-----------------------------------------------------------------------

    associate(&
         ! Gridcell-level non-downscaled fields:
         pfl_porosity_g     => pfl2lnd_inst%pfl_porosity_grc    , & ! Grid-level ParFlow porosity [m^3/m^3]
         watsat             => soilstate_inst%watsat_col          & ! Column-level eCLM porosity  [m^3/m^3]
         )

    ! Parflow overwrites watsat values initialized earlier from SoilStateInitTimeConst.
     do c = bounds%begc,bounds%endc
      g = col%gridcell(c)
      watsat(c,:) = pfl_porosity_g(g,:)
     end do

    end associate
  end subroutine import_parflow_porosity
end module pfl2lndMod
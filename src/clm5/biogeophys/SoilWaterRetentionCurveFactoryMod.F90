module SoilWaterRetentionCurveFactoryMod

  !---------------------------------------------------------------------------
  ! !DESCRIPTION:
  ! Factory to create an instance of soil_water_retention_curve_type. This module figures
  ! out the particular type to return.
  !
  ! !USES:
  use abortutils          , only : endrun
  use shr_log_mod         , only : errMsg => shr_log_errMsg
  use clm_varctl          , only : iulog, soil_water_retention_method
  implicit none
  save
  private
  !
  ! !PUBLIC ROUTINES:
  public :: create_soil_water_retention_curve  ! create an object of class soil_water_retention_curve_type

  character(len=*), parameter, private :: sourcefile = &
       __FILE__

contains

  !-----------------------------------------------------------------------
  function create_soil_water_retention_curve() result(soil_water_retention_curve)
    !
    ! !DESCRIPTION:
    ! Create and return an object of soil_water_retention_curve_type. The particular type
    ! is determined based on a namelist parameter.
    !
    ! !USES:
    use SoilWaterRetentionCurveMod, only : soil_water_retention_curve_type
    use SoilWaterRetentionCurveClappHornberg1978Mod, only : soil_water_retention_curve_clapp_hornberg_1978_type
    use SoilWaterRetentionCurveVanGenuchten1980Mod, only : soil_water_retention_curve_vangenuchten_1980_type
    !
    ! !ARGUMENTS:
    class(soil_water_retention_curve_type), allocatable :: soil_water_retention_curve  ! function result
    !
    ! !LOCAL VARIABLES:

    ! The method is set from the clm_inparm namelist group via clm_varctl
    ! (soil_water_retention_method). It defaults to "clapphornberg_1978", which
    ! reproduces the previous hard-coded behaviour.
    character(len=256) :: method

    character(len=*), parameter :: subname = 'create_soil_water_retention_curve'
    !-----------------------------------------------------------------------

    method = trim(soil_water_retention_method)

    select case (trim(method))
       
    case ("clapphornberg_1978")
       allocate(soil_water_retention_curve, &
            source=soil_water_retention_curve_clapp_hornberg_1978_type())

    case ("vangenuchten_1980")
       allocate(soil_water_retention_curve, &
            source=soil_water_retention_curve_vangenuchten_1980_type())

    case default
       write(iulog,*) subname//' ERROR: unknown method: ', method
       call endrun(msg=errMsg(sourcefile, __LINE__))

    end select

  end function create_soil_water_retention_curve

end module SoilWaterRetentionCurveFactoryMod

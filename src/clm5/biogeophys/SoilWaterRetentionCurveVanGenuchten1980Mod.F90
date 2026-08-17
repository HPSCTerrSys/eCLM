module SoilWaterRetentionCurveVanGenuchten1980Mod

  !---------------------------------------------------------------------------
  ! !DESCRIPTION:
  ! Implementation of soil_water_retention_curve_type using the van Genuchten
  ! (1980) retention curve with the Mualem (1976) conductivity model.
  !
  !   Se  = (s - sres) / (1 - sres)                      effective saturation
  !   Se  = [1 + (alpha*|psi|)^n]^(-m),   m = 1 - 1/n    retention
  !   hk  = hksat * Se^L * [1 - (1 - Se^(1/m))^m]^2      Mualem, L = 0.5
  !
  ! where s is the relative saturation theta/watsat that CLM passes in, and
  ! sres = watres/watsat is the residual relative saturation.
  !
  ! !USES:
  use shr_kind_mod   , only : r8 => shr_kind_r8
  use SoilWaterRetentionCurveMod, only : soil_water_retention_curve_type
  implicit none
  save
  private
  !
  ! !PUBLIC TYPES:
  public :: soil_water_retention_curve_vangenuchten_1980_type
  
  type, extends(soil_water_retention_curve_type) :: &
       soil_water_retention_curve_vangenuchten_1980_type
     private
   contains
     procedure :: soil_hk              ! compute hydraulic conductivity
     procedure :: soil_suction         ! compute soil suction potential
     procedure :: soil_suction_inverse ! compute relative saturation at which soil suction is equal to a target value
  end type soil_water_retention_curve_vangenuchten_1980_type

  interface soil_water_retention_curve_vangenuchten_1980_type
     ! initialize a new soil_water_retention_curve_vangenuchten_1980_type object
     module procedure constructor  
  end interface soil_water_retention_curve_vangenuchten_1980_type

  ! Effective saturation is limited from both ends.
  real(r8), parameter :: se_min = 1.e-4_r8
  real(r8), parameter :: se_max = 1._r8 - 1.e-8_r8

  ! Mualem pore-connectivity exponent
  real(r8), parameter :: mualem_l = 0.5_r8

contains

  !-----------------------------------------------------------------------
  type(soil_water_retention_curve_vangenuchten_1980_type) function constructor()
    !
    ! !DESCRIPTION:
    ! Creates an object of type soil_water_retention_curve_vangenuchten_1980_type.
    ! For now, this is simply a place-holder.
    !-----------------------------------------------------------------------

  end function constructor

  !-----------------------------------------------------------------------
  subroutine soil_hk(this, c, j, s, imped, soilstate_inst, hk, dhkds)
    !
    ! !DESCRIPTION:
    ! Compute hydraulic conductivity
    !
    ! !USES:
    use SoilStateType  , only : soilstate_type
    !
    ! !ARGUMENTS:
    class(soil_water_retention_curve_vangenuchten_1980_type), intent(in) :: this
    integer,  intent(in)             :: c        !column index
    integer,  intent(in)             :: j        !level index
    real(r8), intent(in)             :: s        !relative saturation, [0, 1]
    real(r8), intent(in)             :: imped    !ice impedance
    type(soilstate_type), intent(in) :: soilstate_inst
    real(r8), intent(out)            :: hk       !hydraulic conductivity [mm/s]
    real(r8), optional, intent(out)  :: dhkds    !d[hk]/ds   [mm/s]
    !
    ! !LOCAL VARIABLES:
    real(r8) :: sres      ! residual relative saturation [-]
    real(r8) :: se        ! effective saturation [-]
    real(r8) :: m         ! van Genuchten m = 1 - 1/n
    real(r8) :: sem       ! se**(1/m)
    real(r8) :: a         ! 1 - (1 - se**(1/m))**m
    real(r8) :: dads      ! d[a]/d[se]

    character(len=*), parameter :: subname = 'soil_hk'
    !-----------------------------------------------------------------------

    associate(&
         hksat  => soilstate_inst%hksat_col(c,j)  , & ! Input: [real(r8) (:,:) ] hydraulic conductivity at saturation (mm H2O /s)
         watsat => soilstate_inst%watsat_col(c,j) , & ! Input: [real(r8) (:,:) ] volumetric soil water at saturation (porosity)
         watres => soilstate_inst%watres_col(c,j) , & ! Input: [real(r8) (:,:) ] residual soil water content
         nvg    => soilstate_inst%nsw_col(c,j)      & ! Input: [real(r8) (:,:) ] van Genuchten "n"
         )

    m    = 1._r8 - 1._r8/nvg
    sres = min(watres/watsat, 1._r8 - se_min)
    se   = min(max((s - sres)/(1._r8 - sres), se_min), se_max)

    sem = se**(1._r8/m)
    a   = 1._r8 - (1._r8 - sem)**m

    hk = imped*hksat * se**mualem_l * a*a

    if (present(dhkds)) then
       dads = (1._r8 - sem)**(m - 1._r8) * se**(1._r8/m - 1._r8)
       dhkds = imped*hksat * ( mualem_l*se**(mualem_l - 1._r8) * a*a &
                             + se**mualem_l * 2._r8*a*dads ) / (1._r8 - sres)
    endif

    end associate 

  end subroutine soil_hk

  !-----------------------------------------------------------------------
  subroutine soil_suction(this, c, j, s, soilstate_inst, smp, dsmpds)
    !j, 
    ! !DESCRIPTION:
    ! Compute soil suction potential
    !
    ! !USES:
    use SoilStateType  , only : soilstate_type
    !
    ! !ARGUMENTS:
    class(soil_water_retention_curve_vangenuchten_1980_type), intent(in) :: this
    integer,  intent(in)             :: c       !column index
    integer,  intent(in)             :: j        !level index
    real(r8), intent(in)             :: s        !relative saturation, [0, 1]
    type(soilstate_type), intent(in) :: soilstate_inst
    real(r8), intent(out)            :: smp      !soil suction, negative, [mm]
    real(r8), optional, intent(out)  :: dsmpds   !d[smp]/ds, [mm]
    !
    ! !LOCAL VARIABLES:
    real(r8) :: sres      ! residual relative saturation [-]
    real(r8) :: se        ! effective saturation [-]
    real(r8) :: m         ! van Genuchten m = 1 - 1/n
    real(r8) :: u         ! se**(-1/m) - 1

    character(len=*), parameter :: subname = 'soil_suction'
    !-----------------------------------------------------------------------

    associate(&
         watsat => soilstate_inst%watsat_col(c,j)    , & ! Input: [real(r8) (:,:) ] volumetric soil water at saturation (porosity)
         watres => soilstate_inst%watres_col(c,j)    , & ! Input: [real(r8) (:,:) ] residual soil water content
         alpha  => soilstate_inst%alphasw_col(c,j)   , & ! Input: [real(r8) (:,:) ] van Genuchten "alpha" [1/mm]
         nvg    => soilstate_inst%nsw_col(c,j)         & ! Input: [real(r8) (:,:) ] van Genuchten "n"
         )

    m    = 1._r8 - 1._r8/nvg
    sres = min(watres/watsat, 1._r8 - se_min)
    se   = min(max((s - sres)/(1._r8 - sres), se_min), se_max)

    u = se**(-1._r8/m) - 1._r8

    ! suction potential, negative; -> 0 as se -> 1 (no air-entry pressure)
    smp = -(u**(1._r8/nvg))/alpha

    if (present(dsmpds)) then
       dsmpds = se**(-1._r8/m - 1._r8) * u**(1._r8/nvg - 1._r8) &
                / (alpha*nvg*m*(1._r8 - sres))
    endif

    end associate

  end subroutine soil_suction

  !-----------------------------------------------------------------------
  subroutine soil_suction_inverse(this, c, j, smp_target, soilstate_inst, s_target)
    !
    ! !DESCRIPTION:
    ! Compute relative saturation at which soil suction is equal to a target value.
    ! This is done by inverting the soil_suction equation to solve for s.
    !
    ! !USES:
    use SoilStateType  , only : soilstate_type
    !
    ! !ARGUMENTS:
    class(soil_water_retention_curve_vangenuchten_1980_type), intent(in) :: this
    integer,  intent(in)             :: c       !column index
    integer,  intent(in)             :: j        !level index
    type(soilstate_type), intent(in) :: soilstate_inst
    real(r8) , intent(in)  :: smp_target ! target soil suction, negative [mm]
    real(r8) , intent(out) :: s_target   ! relative saturation at which smp = smp_target [0,1]
    !
    ! !LOCAL VARIABLES:
    real(r8) :: sres      ! residual relative saturation [-]
    real(r8) :: se        ! effective saturation [-]
    real(r8) :: m         ! van Genuchten m = 1 - 1/n

    character(len=*), parameter :: subname = 'soil_suction_inverse'
    !-----------------------------------------------------------------------

    associate(&
         watsat => soilstate_inst%watsat_col(c,j)    , & ! Input: [real(r8) (:,:) ] volumetric soil water at saturation (porosity)
         watres => soilstate_inst%watres_col(c,j)    , & ! Input: [real(r8) (:,:) ] residual soil water content
         alpha  => soilstate_inst%alphasw_col(c,j)   , & ! Input: [real(r8) (:,:) ] van Genuchten "alpha" [1/mm]
         nvg    => soilstate_inst%nsw_col(c,j)         & ! Input: [real(r8) (:,:) ] van Genuchten "n"
         )

    m    = 1._r8 - 1._r8/nvg
    sres = min(watres/watsat, 1._r8 - se_min)

    se = (1._r8 + (alpha*abs(smp_target))**nvg)**(-m)

    ! back to relative saturation theta/watsat
    s_target = sres + (1._r8 - sres)*se

    end associate

  end subroutine soil_suction_inverse

end module SoilWaterRetentionCurveVanGenuchten1980Mod

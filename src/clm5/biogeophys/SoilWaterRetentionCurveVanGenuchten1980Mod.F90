module SoilWaterRetentionCurveVanGenuchten1980Mod

  !---------------------------------------------------------------------------
  ! !DESCRIPTION:
  ! Implementation of soil_water_retention_curve_type using the Clapp-Hornberg 1978
  ! parameterizations.
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
    
    character(len=*), parameter :: subname = 'soil_hk'
    !-----------------------------------------------------------------------
    
    associate(& 
         hksat             =>    soilstate_inst%hksat_col(c,j)          , & ! Input:  [real(r8) (:,:) ]  hydraulic conductivity at saturation (mm H2O /s)
         bsw               =>    soilstate_inst%bsw_col(c,j)              & ! Input:  [real(r8) (:,:) ]  Clapp and Hornberger "b"                        
         )


    !compute hydraulic conductivity
    hk=imped*hksat*s**(2._r8*bsw+3._r8)

    !compute the derivative
    if(present(dhkds))then
       dhkds=(2._r8*bsw+3._r8)*hk/s
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
    ! Local variables
    real(r8) :: alpha, n, m, Se, ssat, sres

    
    character(len=*), parameter :: subname = 'soil_suction'
    !-----------------------------------------------------------------------
    
!    associate(& 
!         bsw               =>    soilstate_inst%bsw_col(c,j)            , & ! Input:  [real(r8) (:,:) ]  Clapp and Hornberger "b"                       
!         sucsat            =>    soilstate_inst%sucsat_col(c,j)           & ! Input:  [real(r8) (:,:) ]  minimum soil suction (mm)                       
!         )

    associate(&
         alpha => soilstate_inst%alphasw_col(c,j), & ! van Genuchten parameter [1/mm]
         n     => soilstate_inst%nsw_col(c,j)      & ! van Genuchten shape parameter
         )
    m = 1._r8 - 1._r8/n
    sres = 0.08_r8
    ssat = 1.0_r8

    ! Effective saturation
    Se = max(sres, min(ssat, s))

    ! Compute soil suction (negative)
    smp = - ( (Se**(-1._r8/m) - 1._r8)**(1._r8/n) ) / alpha

    ! Optional derivative d[smp]/ds
    if (present(dsmpds)) then
        dsmpds = - (1._r8 / (alpha * n * m)) * Se**(-1._r8/m - 1._r8) * &
                 (Se**(-1._r8/m) - 1._r8)**(1._r8/n - 1._r8)
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
    real(r8) :: alpha, n, m, ssat, sres
    real(r8) :: psi_abs
    
    character(len=*), parameter :: subname = 'soil_suction_inverse'
    !-----------------------------------------------------------------------
    
!    associate(& 
!         bsw               =>    soilstate_inst%bsw_col(c,j)            , & ! Input:  [real(r8) (:,:) ]  Clapp and Hornberger "b"                        
!         sucsat            =>    soilstate_inst%sucsat_col(c,j)           & ! Input:  [real(r8) (:,:) ]  minimum soil suction (mm)                       
!         )

      associate(&
          alpha => soilstate_inst%alphasw_col(c,j), &
          n     => soilstate_inst%nsw_col(c,j)      &
      )
      m = 1._r8 - 1._r8/n
      sres = 0.08_r8
      ssat = 1.0_r8


      ! Use absolute value of smp_target since smp is negative
      psi_abs = abs(smp_target)

      ! Compute relative saturation by inverting van Genuchten
      s_target = (1._r8 + (alpha * psi_abs)**n)**(-m)

      ! Clip to valid range
      s_target = max(sres, min(ssat, s_target))

    end associate 

  end subroutine soil_suction_inverse

end module SoilWaterRetentionCurveVanGenuchten1980Mod



module RosettaVanGenuchtenMod

  !---------------------------------------------------------------------------
  ! !DESCRIPTION:
  ! van Genuchten (1980) retention parameters by USDA soil texture class, taken
  ! from the ROSETTA class-average lookup table (Schaap, Leij & van Genuchten
  ! 2001, J. Hydrol. 251:163-176).
  !
  ! These are the same values ParFlow uses for its Geom.TCxx.Saturation.* keys.
  ! The texture classification below reproduces the classifier used. This was 
  ! used to build ParFlow's indicator field. Deriving eCLM's parameters from 
  ! the same table and classifier makes the two models' retention curves consistent.
  !
  ! This is just done for the prototype. Final version may be better to read in
  ! the parameters as static fields.
  ! 
  ! NOTE ON UNITS: Alpha is returned in [1/mm] because CLM carries soil matric
  ! potential in mm. The ROSETTA table tabulates alpha in [1/cm]; the conversion
  !  to [1/cm] is applied once here so that no caller has to think about it.
  !
  use shr_kind_mod, only : r8 => shr_kind_r8
  implicit none
  save
  private
  !
  ! !PUBLIC ROUTINES:
  public :: usda_texture_class     ! USDA texture class from sand/silt/clay percentages
  public :: rosetta_class_params   ! ROSETTA van Genuchten parameters for a texture class

  ! ROSETTA class averages, indexed by USDA texture class 1..12.
  ! Order: sand, loamy sand, sandy loam, loam, silt loam, silt,
  !        sandy clay loam, clay loam, silty clay loam, sandy clay,
  !        silty clay, clay
  integer, parameter, public :: nusda = 12

  real(r8), parameter :: ros_thetar(nusda) = &                  ! residual water content [m3/m3]
       (/ 0.053_r8, 0.049_r8, 0.039_r8, 0.061_r8, 0.065_r8, 0.050_r8, &
          0.063_r8, 0.079_r8, 0.090_r8, 0.117_r8, 0.111_r8, 0.098_r8 /)

  real(r8), parameter :: ros_thetas(nusda) = &                  ! saturated water content [m3/m3]
       (/ 0.375_r8, 0.390_r8, 0.387_r8, 0.399_r8, 0.439_r8, 0.489_r8, &
          0.384_r8, 0.442_r8, 0.482_r8, 0.385_r8, 0.481_r8, 0.459_r8 /)

  real(r8), parameter :: ros_alpha_cm(nusda) = &                ! alpha [1/cm]
       (/ 0.0352_r8, 0.0348_r8, 0.0267_r8, 0.0111_r8, 0.0051_r8, 0.0066_r8, &
          0.0211_r8, 0.0158_r8, 0.0084_r8, 0.0334_r8, 0.0162_r8, 0.0150_r8 /)

  real(r8), parameter :: ros_n(nusda) = &                       ! shape parameter n [-]
       (/ 3.18_r8, 1.75_r8, 1.45_r8, 1.47_r8, 1.66_r8, 1.68_r8, &
          1.33_r8, 1.42_r8, 1.52_r8, 1.21_r8, 1.32_r8, 1.25_r8 /)

contains

  !-----------------------------------------------------------------------
  integer function usda_texture_class(sand, silt, clay)
    !
    ! !DESCRIPTION:
    ! USDA soil texture class (1..12) from sand/silt/clay percentages.
    ! Reproduces the classifier used to build ParFlow's TC01..TC12 indicator
    ! field, so that a given soil lands in the same class in both models.
    !
    ! Returns 0 if the fractions do not sum to 100 % (caller decides what to do).
    !
    ! !ARGUMENTS:
    real(r8), intent(in) :: sand   ! % sand
    real(r8), intent(in) :: silt   ! % silt
    real(r8), intent(in) :: clay   ! % clay
    !-----------------------------------------------------------------------

    usda_texture_class = 0
    if ((sand + silt + clay) >= 100.1_r8 .or. (sand + silt + clay) <= 99.9_r8) return

    if     ( (silt + 1.5_r8*clay) < 15._r8 ) then
       usda_texture_class = 1    ! sand
    elseif ( (silt + 1.5_r8*clay) >= 15._r8 .and. (silt + 2._r8*clay) < 30._r8 ) then
       usda_texture_class = 2    ! loamy sand
    elseif ( clay >= 7._r8 .and. clay < 20._r8 .and. sand > 52._r8 .and. &
             (silt + 2._r8*clay) >= 30._r8 ) then
       usda_texture_class = 3    ! sandy loam (1)
    elseif ( clay < 7._r8 .and. silt < 50._r8 .and. (silt + 2._r8*clay) >= 30._r8 ) then
       usda_texture_class = 3    ! sandy loam (2)
    elseif ( clay >= 7._r8 .and. clay < 27._r8 .and. silt >= 28._r8 .and. &
             silt < 50._r8 .and. sand <= 52._r8 ) then
       usda_texture_class = 4    ! loam
    elseif ( silt >= 50._r8 .and. clay >= 12._r8 .and. clay < 27._r8 ) then
       usda_texture_class = 5    ! silt loam (1)
    elseif ( silt >= 50._r8 .and. silt < 80._r8 .and. clay < 12._r8 ) then
       usda_texture_class = 5    ! silt loam (2)
    elseif ( silt >= 80._r8 .and. clay < 12._r8 ) then
       usda_texture_class = 6    ! silt
    elseif ( clay >= 20._r8 .and. clay < 35._r8 .and. silt < 28._r8 .and. sand > 45._r8 ) then
       usda_texture_class = 7    ! sandy clay loam
    elseif ( clay >= 27._r8 .and. clay < 40._r8 .and. sand > 20._r8 .and. sand <= 45._r8 ) then
       usda_texture_class = 8    ! clay loam
    elseif ( clay >= 27._r8 .and. clay < 40._r8 .and. sand <= 20._r8 ) then
       usda_texture_class = 9    ! silty clay loam
    elseif ( clay >= 35._r8 .and. sand > 45._r8 ) then
       usda_texture_class = 10   ! sandy clay
    elseif ( clay >= 40._r8 .and. silt >= 40._r8 ) then
       usda_texture_class = 11   ! silty clay
    elseif ( clay >= 40._r8 .and. sand <= 45._r8 .and. silt < 40._r8 ) then
       usda_texture_class = 12   ! clay
    endif

  end function usda_texture_class

  !-----------------------------------------------------------------------
  subroutine rosetta_class_params(sand, clay, alpha, n, sres)
    !
    ! !DESCRIPTION:
    ! ROSETTA class-average van Genuchten parameters for the texture implied by
    ! the given sand and clay percentages.
    !
    ! sres is returned as a RELATIVE saturation (theta_r/theta_s), not a water
    ! content, so that it can be combined with CLM's own watsat rather than
    ! ROSETTA's theta_s. This is the same quantity ParFlow stores as
    ! Geom.TCxx.Saturation.SRes.
    !
    ! Falls back to loam (class 4) for textures that cannot be classified, which
    ! only happens where sand+clay exceed 100 % in the input dataset.
    !
    ! !ARGUMENTS:
    real(r8), intent(in)  :: sand    ! % sand
    real(r8), intent(in)  :: clay    ! % clay
    real(r8), intent(out) :: alpha   ! van Genuchten alpha [1/mm]
    real(r8), intent(out) :: n       ! van Genuchten n [-]
    real(r8), intent(out) :: sres    ! residual RELATIVE saturation [-]
    !
    ! !LOCAL VARIABLES:
    integer  :: itex
    real(r8) :: silt
    !-----------------------------------------------------------------------

    silt = max(0._r8, 100._r8 - sand - clay)
    itex = usda_texture_class(sand, silt, clay)
    if (itex < 1 .or. itex > nusda) itex = 4    ! unclassifiable -> loam

    alpha = ros_alpha_cm(itex) * 0.1_r8         ! [1/cm] -> [1/mm]
    n     = ros_n(itex)
    sres  = ros_thetar(itex) / ros_thetas(itex)

  end subroutine rosetta_class_params

end module RosettaVanGenuchtenMod

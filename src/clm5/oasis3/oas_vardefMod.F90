module oas_vardefMod
  implicit none
  save

! #ifdef COUP_OAS_PFL
  integer :: oas_psi_id, oas_et_loss_id, oas_sat_id
! #endif

! #ifdef COUP_OAS_ICON
  INTEGER               :: oas_comp_id
  CHARACTER(len=4)      :: oas_comp_name="eCLM"
  TYPE :: t_oas_field
    CHARACTER(len = 8)  :: clpname
    INTEGER             :: vid
  END TYPE t_oas_field
  TYPE(t_oas_field), DIMENSION(8)  :: oas_snd_meta
  TYPE(t_oas_field), DIMENSION(11)  :: oas_rcv_meta

! #endif 

end module oas_vardefMod

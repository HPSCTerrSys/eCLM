module oas_vardefMod
  implicit none
  save
  
  ! Type for coupling field information
  type :: oas_var
    character(len=12) :: name  ! Name of the coupling field
    integer           :: id    ! Id of the field
  end type oas_var

  ! Sent fields
  type(oas_var), allocatable :: et_loss(:) ! soil ET loss

  ! Received fields from Parflow
  type(oas_var), allocatable :: watsat(:)  ! water saturation
  type(oas_var), allocatable :: psi(:)     ! pressure head

end module oas_vardefMod
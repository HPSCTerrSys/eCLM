module oas_vardefMod
  implicit none
  save
  
  ! Type for coupling field information
  type :: FLD_CPL
    logical           :: laction ! To be coupled or not
    character(len=12) :: clname  ! Name of the coupling field
    character(len=3)  :: ref     ! Type of the coupling field
    character(len=1)  :: clgrid  ! Grid type
    integer           :: nid     ! Id of the field
    integer           :: level   ! # of soil layer
  end type FLD_CPL

  integer, parameter  :: MAX_OAS_CPL_FIELDS = 200
  integer, parameter  :: MAX_SOIL_LAYERS = 10
  type(FLD_CPL)       :: ssnd(MAX_OAS_CPL_FIELDS), srcv(MAX_OAS_CPL_FIELDS) ! send and receive coupling fields 
  
end module oas_vardefMod
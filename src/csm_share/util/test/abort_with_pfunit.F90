module abort_with_pfunit_mod
   use shr_abort_mod, only: set_abort_method
   implicit none
   private

   public :: abort_unit_test
   public :: initialize_abort

contains

   subroutine abort_unit_test(error_msg, error_code)
      use funit, only: pFUnit_throw => throw

      character(len=*), intent(in), optional :: error_msg
      integer         , intent(in), optional :: error_code

      character(len=:), allocatable :: message_

      if (present(error_msg)) then
         message_ = "pFUnit test aborted: "//trim(error_msg)
      else
         message_ = "pFUnit test aborted."
      end if
      call pFUnit_throw(message_)

   end subroutine abort_unit_test

   subroutine initialize_abort()
      call set_abort_method(abort_unit_test)
   end subroutine initialize_abort

end module abort_with_pfunit_mod

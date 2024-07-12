# Finds the MCT library.
# This will define the following variables:
#
#   MCT_FOUND       - True if the system has the MCT library.
#   MCT_INCLUDE_DIR - Include directories needed to use MCT.
#   MCT_LIBRARIES   - Libraries needed to link to MCT.
#

find_path(MCT_INCLUDE_DIR
  NAMES mct_mod.mod
  PATH_SUFFIXES mct lib/mct build/lib/mct
)
find_library(MCT_LIBRARY
  NAMES mct
  PATH_SUFFIXES lib
)
find_library(MPEU_LIBRARY
  NAMES mpeu
  PATH_SUFFIXES lib
)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(MCT DEFAULT_MSG
    MCT_INCLUDE_DIR
    MCT_LIBRARY
    MPEU_LIBRARY
)

if(MCT_FOUND)
   set(MCT_LIBRARIES ${MCT_LIBRARY} ${MPEU_LIBRARY})
endif()
unset(MCT_LIBRARY)
unset(MPEU_LIBRARY)
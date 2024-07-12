# Finds the OASIS3-MCT library.
# This will define the following variables:
#
#   OASIS3MCT_FOUND        - True if the system has the MCT library.
#   OASIS3MCT_INCLUDE_DIRS - Include directories needed to use MCT.
#   OASIS3MCT_LIBRARIES    - Libraries needed to link to MCT.
#   OASIS3MCT::OASIS3MCT   -  A target to use with `target_link_libraries`.


find_path(PSMILE_INCLUDE_DIR NAMES mod_oasis.mod PATH_SUFFIXES psmile.MPI1 lib/psmile.MPI1 build/lib/psmile.MPI1)
find_path(MCT_INCLUDE_DIR NAMES oas_mct_mod.mod PATH_SUFFIXES mct lib/mct build/lib/mct)
find_path(SCRIP_INCLUDE_DIR NAMES remap_conservative.mod PATH_SUFFIXES scrip lib/scrip build/lib/scrip)

find_library(PSMILE_LIB NAMES psmile.MPI1 PATH_SUFFIXES lib)
find_library(MCT_LIB NAMES mct PATH_SUFFIXES lib)
find_library(MPEU_LIB NAMES mpeu PATH_SUFFIXES lib)
find_library(SCRIP_LIB NAMES scrip PATH_SUFFIXES lib)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(OASIS3MCT DEFAULT_MSG
    PSMILE_INCLUDE_DIR
    MCT_INCLUDE_DIR
    SCRIP_INCLUDE_DIR
    PSMILE_LIB
    MCT_LIB
    MPEU_LIB
    SCRIP_LIB
)

if(OASIS3MCT_FOUND)
   set(OASIS3MCT_LIBRARIES ${PSMILE_LIB} ${MCT_LIB} ${MPEU_LIB} ${SCRIP_LIB})
   set(OASIS3MCT_INCLUDE_DIRS ${PSMILE_INCLUDE_DIR} ${MCT_INCLUDE_DIR} ${SCRIP_INCLUDE_DIR})
   if(NOT TARGET OASIS3MCT::OASIS3MCT)
      add_library(OASIS3MCT::OASIS3MCT INTERFACE IMPORTED)
      target_include_directories(OASIS3MCT::OASIS3MCT INTERFACE ${OASIS3MCT_INCLUDE_DIRS})
      target_link_libraries(OASIS3MCT::OASIS3MCT INTERFACE ${OASIS3MCT_LIBRARIES})
      target_link_options(OASIS3MCT::OASIS3MCT INTERFACE "-fopenmp") #TODO: see if this could be moved to SetBuildOptions.cmake
   endif()
endif()

unset(PSMILE_INCLUDE_DIR)
unset(MCT_INCLUDE_DIR)
unset(SCRIP_INCLUDE_DIR)
unset(PSMILE_LIB)
unset(MCT_LIB)
unset(MPEU_LIB)
unset(SCRIP_LIB)
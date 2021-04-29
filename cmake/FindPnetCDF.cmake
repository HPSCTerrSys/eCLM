# Finds the PnetCDF library. Defines the following variables:
#
#  PnetCDF_FOUND: Whether NetCDF was found or not.
#  PnetCDF_INCLUDE_DIR: Include directory necessary to use NetCDF.
#  PnetCDF_LIBRARIES: Libraries necessary to use NetCDF.
#  PnetCDF_VERSION: The version of NetCDF found.
#  PnetCDF::PnetCDF: A target to use with `target_link_libraries`.
#

# Find PnetCDF using pkg-tools.
find_package(PkgConfig QUIET)
if(PkgConfig_FOUND)
    pkg_check_modules(PnetCDF QUIET pnetcdf IMPORTED_TARGET)
    if (PnetCDF_FOUND)
        set(PnetCDF_INCLUDE_DIR "${PnetCDF_INCLUDEDIR}")
        add_library(PnetCDF::PnetCDF INTERFACE IMPORTED)
        target_link_libraries(PnetCDF::PnetCDF INTERFACE PkgConfig::PnetCDF)
    endif()
endif()

# If not found, manually search for Pnetcdf include and library files.
if (NOT PnetCDF_FOUND)
    find_path(PnetCDF_INCLUDE_DIR NAMES pnetcdf.mod)
    find_library(PnetCDF_LIBRARIES NAMES pnetcdf)
endif()

find_package_handle_standard_args(PnetCDF
   REQUIRED_VARS PnetCDF_INCLUDE_DIR PnetCDF_LIBRARIES
   VERSION_VAR PnetCDF_VERSION)
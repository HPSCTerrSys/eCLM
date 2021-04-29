# Finds the NetCDF Fortran library. Defines the following variables:
#
#  NetCDF_FOUND: Whether NetCDF was found or not.
#  NetCDF_INCLUDE_DIR: Include directory necessary to use NetCDF.
#  NetCDF_LIBRARIES: Libraries necessary to use NetCDF.
#  NetCDF_VERSION: The version of NetCDF found.
#  NetCDF_HAS_PARALLEL: Whether or not NetCDF was found with parallel IO support.
#  NetCDF::NetCDF: A target to use with `target_link_libraries`.
#

find_package(PkgConfig QUIET)
include(FindPackageHandleStandardArgs)

# Detect NetCDF_HAS_PARALLEL feature from the netCDF C library.
# Try to find CMake-built netCDF-C.
find_package(_NetCDF_C NAMES netCDF)
if(_NetCDF_C_FOUND)
   set(NetCDF_HAS_PARALLEL "${netCDF_HAS_PARALLEL}")
   get_filename_component(_NetCDF_C_CONFIG_DIR ${_NetCDF_C_CONFIG} DIRECTORY)
endif()

# If netCDF-C was not found, try finding it using pkg-config.
if (NOT DEFINED NetCDF_HAS_PARALLEL AND PkgConfig_FOUND)
   pkg_check_modules(_NetCDF_C QUIET netcdf IMPORTED_TARGET)
   if (_NetCDF_C_FOUND)
      # Regex copied from https://github.com/Kitware/VTK/blob/181e6ba2/CMake/FindNetCDF.cmake#L13
      file(STRINGS "${_NetCDF_C_INCLUDEDIR}/netcdf_meta.h" _netcdf_lines
         REGEX "#define[ \t]+NC_HAS_PARALLEL[ \t]")
      string(REGEX REPLACE ".*NC_HAS_PARALLEL[ \t]*([0-1]+).*" "\\1" NetCDF_HAS_PARALLEL "${_netcdf_lines}")
   endif()
endif()

if (NOT DEFINED NetCDF_HAS_PARALLEL)
   message(WARNING "NetCDF C library was not found. Assuming NetCDF_HAS_PARALLEL=FALSE ...")
   set(NetCDF_HAS_PARALLEL FALSE)
endif()

# Try to find CMake-built netCDF-Fortran.
find_package(_NetCDF_F90 QUIET NAMES netCDF-Fortran HINTS ${_NetCDF_C_CONFIG_DIR})
if(_NetCDF_F90_FOUND AND TARGET netCDF::netcdff)
   get_target_property(NetCDF_INCLUDE_DIR netCDF::netcdff INTERFACE_INCLUDE_DIRECTORIES)
   set(NetCDF_LIBRARIES netCDF::netcdff)
   set(NetCDF_VERSION "${_NetCDF_F90_VERSION}")
elseif(PkgConfig_FOUND)
   # Try finding netCDF-Fortran using pkg-config.
   pkg_check_modules(_NetCDF_F90 QUIET netcdf-fortran IMPORTED_TARGET)
   if (_NetCDF_F90_FOUND)
      set(NetCDF_INCLUDE_DIR "${_NetCDF_F90_INCLUDEDIR}")
      set(NetCDF_LIB_DIR "${_NetCDF_F90_LIBDIR}")
      set(NetCDF_LIBRARIES "${_NetCDF_F90_LIBRARIES}")
      set(NetCDF_VERSION "${_NetCDF_F90_VERSION}")
   endif()
endif()

find_package_handle_standard_args(NetCDF
   REQUIRED_VARS NetCDF_INCLUDE_DIR NetCDF_LIBRARIES
   VERSION_VAR NetCDF_VERSION)

if(NetCDF_FOUND AND NOT TARGET NetCDF::NetCDFF)
   add_library(NetCDF::NetCDFF INTERFACE IMPORTED)
   target_include_directories(NetCDF::NetCDFF INTERFACE ${NetCDF_INCLUDE_DIR})
   target_link_libraries(NetCDF::NetCDFF INTERFACE ${NetCDF_LIBRARIES})
   if(DEFINED NetCDF_LIB_DIR)
      target_link_directories(NetCDF::NetCDFF INTERFACE ${NetCDF_LIB_DIR})
   endif()
endif()

unset(_NetCDF_C_DIR)
unset(_NetCDF_C_FOUND)
unset(_NetCDF_C_CONFIG_DIR)
unset(_NetCDF_F90_DIR)
unset(_NetCDF_F90_FOUND)
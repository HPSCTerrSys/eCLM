# Finds the NetCDF C and Fortran libraries. If found, the CMake target
# NetCDF::NetCDFF will be created and the following variables will be defined:
#
# - NetCDF_FOUND
# - NetCDF_C_INCLUDEDIR
# - NetCDF_HAS_PARALLEL
# - NetCDF_F90_INCLUDEDIR
# - NetCDF_F90_LIBRARIES
#
# Basic usage:
#
#  find_package(NetCDF)
#  if(NetCDF_FOUND)
#     target_link_libraries(mylibrary PUBLIC NetCDF::NetCDFF)
#  endif()
#

find_package(PkgConfig QUIET)
include(FindPackageHandleStandardArgs)

set(NetCDF_HAS_PARALLEL FALSE)

# Try to find netCDF-C via CMake config files
find_package(NetCDF_C QUIET NAMES netCDF)
if(NetCDF_C_FOUND)
   get_target_property(NetCDF_C_INCLUDEDIR netCDF::netcdf INTERFACE_INCLUDE_DIRECTORIES)
   set(NetCDF_HAS_PARALLEL "${netCDF_HAS_PARALLEL}")
   get_filename_component(NetCDF_C_CONFIG_DIR ${NetCDF_C_CONFIG} DIRECTORY)
elseif(PkgConfig_FOUND)
   # If not found, try to find again via pkg-config
   pkg_check_modules(NetCDF_C QUIET netcdf IMPORTED_TARGET)
   if (NetCDF_C_FOUND)
      # Extract NC_HAS_PARALLEL value from netcdf_meta.h. Copied from https://github.com/Kitware/VTK/blob/181e6ba2/CMake/FindNetCDF.cmake#L13
      file(STRINGS "${NetCDF_C_INCLUDEDIR}/netcdf_meta.h" _netcdf_lines
          REGEX "#define[ \t]+NC_HAS_PARALLEL[ \t]")
      string(REGEX REPLACE ".*NC_HAS_PARALLEL[ \t]*([0-1]+).*" "\\1" NetCDF_HAS_PARALLEL "${_netcdf_lines}")
   endif()
endif()


if (NetCDF_C_FOUND)
   message(STATUS "Found NetCDF_C version ${NetCDF_C_VERSION}")
   if (NetCDF_HAS_PARALLEL)
      message(STATUS "NetCDF C built with parallel I/O support.")
      # parallel I/O explained here: https://github.com/Unidata/netcdf-c/blob/v4.7.0/INSTALL.md#building-with-parallel-io-support-build_parallel
   endif()
endif()

# Try to find netCDF-Fortran via CMake config files
find_package(NetCDF_F90 QUIET NAMES netCDF-Fortran HINTS ${NetCDF_C_CONFIG_DIR})
if(NetCDF_F90_FOUND AND TARGET netCDF::netcdff)
   get_target_property(NetCDF_F90_INCLUDEDIR netCDF::netcdff INTERFACE_INCLUDE_DIRECTORIES)
   set(NetCDF_F90_LIBRARIES netCDF::netcdff)
elseif(PkgConfig_FOUND)
   # If not found, try to find again via pkg-config
   pkg_check_modules(NetCDF_F90 QUIET netcdf-fortran IMPORTED_TARGET)
   if (NetCDF_F90_FOUND)
      # instead of includedir, fmoddir contains the actual path to netcdf.mod 
      pkg_get_variable(NetCDF_F90_INCLUDEDIR netcdf-fortran fmoddir)
   endif()
endif()

find_package_handle_standard_args(NetCDF
   REQUIRED_VARS NetCDF_C_INCLUDEDIR NetCDF_F90_INCLUDEDIR NetCDF_F90_LIBRARIES
   VERSION_VAR NetCDF_F90_VERSION)

if(NetCDF_FOUND AND NOT TARGET NetCDF::NetCDFF)
   add_library(NetCDF::NetCDFF INTERFACE IMPORTED)
   target_include_directories(NetCDF::NetCDFF INTERFACE ${NetCDF_C_INCLUDEDIR} ${NetCDF_F90_INCLUDEDIR})
   target_link_libraries(NetCDF::NetCDFF INTERFACE ${NetCDF_F90_LIBRARIES})
   if(DEFINED NetCDF_C_LIBDIR)
      target_link_directories(NetCDF::NetCDFF INTERFACE ${NetCDF_C_LIBDIR})
   endif()
   if(DEFINED NetCDF_F90_LIBDIR)
      target_link_directories(NetCDF::NetCDFF INTERFACE ${NetCDF_F90_LIBDIR})
   endif()
endif()

unset(NetCDF_C_DIR)
unset(NetCDF_C_FOUND)
unset(NetCDF_C_CONFIG_DIR)
unset(NetCDF_F90_DIR)
unset(NetCDF_F90_FOUND)
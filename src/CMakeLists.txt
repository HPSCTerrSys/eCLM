cmake_minimum_required (VERSION 3.16.3)
project (eCLM LANGUAGES C Fortran)

# Set internal build variables (i.e. non-model related options)
get_filename_component(ECLM_ROOT ${CMAKE_SOURCE_DIR} DIRECTORY)
list(APPEND CMAKE_MODULE_PATH "${ECLM_ROOT}/cmake")
set(GENF90 ${CMAKE_MODULE_PATH}/genf90.pl)

# Set machine-specific build options
include(SetBuildOptions)

# Set default model options
option(COUP_OAS_ICON "Couple eCLM with ICON" OFF)
option(COUP_OAS_PFL "Couple eCLM with ParFlow" OFF)

# eCLM subcomponents
add_subdirectory(externals)
add_subdirectory(csm_share)
add_subdirectory(clm5)
add_subdirectory(stub_comps)
if(COUP_OAS_ICON)
    add_subdirectory(icon_atm)
else()
    add_subdirectory(datm)
endif()
add_subdirectory(mosart)
add_subdirectory(eclm)

# Make sure that the required libraries are always found 
# independent from  LD_LIBRARY_PATH and the install location. 
# https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/RPATH-handling#always-full-rpath
set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
list(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${CMAKE_INSTALL_PREFIX}/lib" isSystemDir)
if("${isSystemDir}" STREQUAL "-1")
    set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
endif("${isSystemDir}" STREQUAL "-1")
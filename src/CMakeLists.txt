cmake_minimum_required (VERSION 3.16.3)
project (eCLM LANGUAGES C Fortran)


get_filename_component(ECLM_ROOT ${CMAKE_SOURCE_DIR} DIRECTORY)
list(APPEND CMAKE_MODULE_PATH "${ECLM_ROOT}/cmake")
set(GENF90 ${CMAKE_MODULE_PATH}/genf90.pl)

include(SetBuildOptions)

if (USE_PDAF)
  set(CMAKE_Fortran_MODULE_DIRECTORY ${CMAKE_BINARY_DIR}/eCLM)
  set(CMAKE_Fortran_MODULE_DIRECTORY_MCT ${CMAKE_BINARY_DIR}/externals/mct/include)
  set(CMAKE_Fortran_MODULE_DIRECTORY_GPTL ${CMAKE_BINARY_DIR}/externals/gptl/include)
endif()

option(ENABLE_TESTS "Enable unit tests." OFF)
if (ENABLE_TESTS)
  find_package(PFUNIT REQUIRED)
  enable_testing()
  message(STATUS "Found pFUnit v${PFUNIT_VERSION}")
  message(STATUS "Unit tests enabled.")
endif()

add_subdirectory(externals)
add_subdirectory(csm_share)
add_subdirectory(clm5)
add_subdirectory(stub_comps)
add_subdirectory(datm)
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

if (USE_PDAF)
  install(DIRECTORY ${CMAKE_Fortran_MODULE_DIRECTORY}
          DESTINATION ${CMAKE_INSTALL_PREFIX}/include)
  install(DIRECTORY ${CMAKE_Fortran_MODULE_DIRECTORY_MCT}
          DESTINATION ${CMAKE_INSTALL_PREFIX}/include/eCLM/externals/mct)
  install(DIRECTORY ${CMAKE_Fortran_MODULE_DIRECTORY_GPTL}
          DESTINATION ${CMAKE_INSTALL_PREFIX}/include/eCLM/externals/gptl)
endif()

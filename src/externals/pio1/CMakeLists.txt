project(pio C Fortran)
add_library(${PROJECT_NAME} STATIC)

find_file(TESTFILE NAMES TryCSizeOf.f90 PATHS ${CMAKE_MODULE_PATH} NO_DEFAULT_PATH)
get_filename_component(TESTFILEPATH ${TESTFILE} PATH)

target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_BINARY_DIR})

try_compile(WITH_CSIZEOF ${CMAKE_CURRENT_BINARY_DIR}/tryCompileCSIZEOF
                        ${TESTFILEPATH}/TryCSizeOf.f90)

if(${WITH_CSIZEOF} STREQUAL FALSE)
    message(STATUS "PIO: Fortran compiler does not support c_sizeof function")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NO_C_SIZEOF)
endif()

option(PIO_BIG_ENDIAN "Specify that the machine is big endian" test)
if ("${PIO_BIG_ENDIAN}" STREQUAL "test")
  include(TestBigEndian)
  TestBigEndian(PIO_BIG_ENDIAN_TEST)
  if(PIO_BIG_ENDIAN_TEST)
    set(PIO_BIG_ENDIAN ON  CACHE BOOL "")
  else()
    set(PIO_BIG_ENDIAN OFF CACHE BOOL "")
  endif()
else()
  set(PIO_BIG_ENDIAN ${PIO_BIG_ENDIAN} CACHE BOOL "")
endif()

if (PIO_FILESYSTEM_HINTS STREQUAL "lustre")
  message(STATUS "PIO: Using lustre filesystem hints")
  target_compile_definitions(${PROJECT_NAME} PRIVATE PIO_LUSTRE_HINTS)
elseif(PIO_FILESYSTEM_HINTS STREQUAL "gpfs")
  message(STATUS "PIO: Using gpfs filesystem hints")
  target_compile_definitions(${PROJECT_NAME} PRIVATE PIO_GPFS_HINTS)
elseif(NOT "${PIO_FILESYSTEM_HINTS}" STREQUAL "")
  message(WARNING "PIO: ${PIO_FILESYSTEM_HINTS} not valid option for PIO_FILESYSTEM_HINTS; use gpfs or lustre.")
endif()

find_package(NetCDF)
if(NetCDF_FOUND)
  message(STATUS "PIO: Building with netcdf support ")
  target_compile_definitions(${PROJECT_NAME} PUBLIC _NETCDF)
  if (${NetCDF_HAS_PARALLEL})
    target_compile_definitions(${PROJECT_NAME} PUBLIC _NETCDF4)
  endif()
  target_link_libraries(${PROJECT_NAME} PUBLIC NetCDF::NetCDFF)
else()
  message(STATUS "PIO: Building without netcdf support")
  target_compile_definitions(${PROJECT_NAME} PUBLIC _NONETCDF)
endif()

# PNetcdf is optional but used by default
option(WITH_PNETCDF "Whether to build with PnetCDF" TRUE)
if (${WITH_PNETCDF})
  find_package(PnetCDF REQUIRED)
else()
  message(WARNING "Warning: Not building with PNetcdf - cannot run all regression tests.")
endif()
if(PnetCDF_FOUND)
  message(STATUS "PIO: Building with pnetcdf support ")
  target_compile_definitions(${PROJECT_NAME} PUBLIC _PNETCDF)
  target_link_libraries(${PROJECT_NAME} PUBLIC PnetCDF::PnetCDF)
else()
  message(STATUS "PIO: Building without pnetcdf support ")
  target_compile_definitions(${PROJECT_NAME} PUBLIC _NOPNETCDF)
endif()

option(PIO_USE_MPIIO "Enable support for MPI-IO (default auto detect)" ON)
if (PIO_USE_MPIIO)
  try_compile(MPIIO_SUCCESS ${CMAKE_CURRENT_BINARY_DIR}/tryCompileMPIIO
                            ${TESTFILEPATH}/TryMPIIO.f90)
  if (${MPIIO_SUCCESS})
    message(STATUS "PIO: MPIIO detected and enabled.")
    target_compile_definitions(${PROJECT_NAME} PUBLIC USEMPIIO)
  else()
    message(STATUS "PIO: MPIIO not detected and therefore disabled.")
    target_compile_definitions(${PROJECT_NAME} PUBLIC USEMPIIO)
    set(PIO_USE_MPIIO FALSE)
  endif()
endif()

target_compile_definitions(${PROJECT_NAME} PRIVATE _NOUSEMCT)

option(PIO_USE_BOX  "" ON)
if(PIO_USE_BOX)
  target_compile_definitions(${PROJECT_NAME} PRIVATE _USEBOX)
else()
  target_compile_definitions(${PROJECT_NAME} PRIVATE _NOUSEBOX)
endif()

option(PIO_USE_MPIMOD "Use Fortran MPI module (default auto detect)" ON)
if (PIO_USE_MPIMOD)
  try_compile(MPIMOD_SUCCESS ${CMAKE_CURRENT_BINARY_DIR}/tryCompileMPIMod
                             ${TESTFILEPATH}/TryMPIMod.f90)
  if (${MPIMOD_SUCCESS})
    message(STATUS "PIO: MPI Fortran module detected and enabled.")
  else()
    message(STATUS "PIO: MPI Fortran module not detected and therefore disabled.")
    set(PIO_USE_MPIMOD FALSE)
  endif()
endif()

if (NOT ${PIO_USE_MPIMOD})
  target_compile_definitions(${PROJECT_NAME} PRIVATE NO_MPIMOD)
endif()

option(PIO_BUILD_TIMING  "Enable timing library (GPTL) usage in PIO." OFF)
if(${PIO_BUILD_TIMING})
  message(STATUS "PIO: Timing library enabled")
  target_compile_definitions(${PROJECT_NAME} PRIVATE TIMING)
  target_link_libraries(${PROJECT_NAME} PRIVATE gptl)
endif()

set(SRCS_C      topology.c)

set(SRCS_F90    calcdecomp.F90
                calcdisplace_mod.F90
                ionf_mod.F90
                nf_mod.F90
                pio.F90
                pio_kinds.F90
                pio_mpi_utils.F90
                pio_msg_callbacks.F90
                pio_msg_mod.F90
                pio_nf_utils.F90
                pio_support.F90
                pio_types.F90
                pio_utils.F90
                piolib_mod.F90)

set(TEMPSRCF90  pionfatt_mod.F90
                pionfread_mod.F90
                pionfwrite_mod.F90
                pionfput_mod.F90
                pionfget_mod.F90
                alloc_mod.F90
                box_rearrange.F90
                rearrange.F90
                iompi_mod.F90
                piodarray.F90
                pio_spmd_utils.F90
                pio_msg_getput_callbacks.F90)

foreach(tempfile IN LISTS TEMPSRCF90)
  add_custom_command(
    OUTPUT ${tempfile}
    COMMAND ${GENF90} ${CMAKE_CURRENT_SOURCE_DIR}/${tempfile}.in > ${tempfile}
    DEPENDS  ${tempfile}.in
  )
endforeach()

target_sources(${PROJECT_NAME} PRIVATE ${SRCS_F90} ${SRCS_C} ${TEMPSRCF90})

install (TARGETS ${PROJECT_NAME} ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
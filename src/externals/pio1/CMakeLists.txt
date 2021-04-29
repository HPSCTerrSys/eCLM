PROJECT(pio C Fortran)
ADD_LIBRARY(${PROJECT_NAME} STATIC)

find_file( TESTFILE NAMES TryCSizeOf.f90 PATHS ${CMAKE_MODULE_PATH} NO_DEFAULT_PATH)
get_filename_component( TESTFILEPATH ${TESTFILE} PATH)


target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_BINARY_DIR})

#SET(bld_PIO_DEFINITIONS)

TRY_COMPILE(WITH_CSIZEOF ${CMAKE_CURRENT_BINARY_DIR}/tryCompileCSIZEOF
                        ${TESTFILEPATH}/TryCSizeOf.f90)
#MESSAGE(STATUS "c_sizeof test ${WITH_CSIZEOF}")
IF(${WITH_CSIZEOF} STREQUAL FALSE)
    MESSAGE(STATUS "Fortran compiler does not support c_sizeof function")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NO_C_SIZEOF)
endif()

OPTION(PIO_BIG_ENDIAN "Specify that the machine is big endian" test)
IF ("${PIO_BIG_ENDIAN}" STREQUAL "test")
  INCLUDE(TestBigEndian)
  TestBigEndian(PIO_BIG_ENDIAN_TEST)
  IF(PIO_BIG_ENDIAN_TEST)
    SET(PIO_BIG_ENDIAN ON  CACHE BOOL "")
  ELSE()
    SET(PIO_BIG_ENDIAN OFF CACHE BOOL "")
  ENDIF()
ELSE()
  SET(PIO_BIG_ENDIAN ${PIO_BIG_ENDIAN} CACHE BOOL "")
ENDIF()


IF (PIO_FILESYSTEM_HINTS STREQUAL "lustre")
  MESSAGE(STATUS "PIO using lustre filesystem hints")
  target_compile_definitions(${PROJECT_NAME} PRIVATE PIO_LUSTRE_HINTS)
ELSEIF(PIO_FILESYSTEM_HINTS STREQUAL "gpfs")
  MESSAGE(STATUS "PIO using gpfs filesystem hints")
  target_compile_definitions(${PROJECT_NAME} PRIVATE PIO_GPFS_HINTS)
ELSEIF(NOT "${PIO_FILESYSTEM_HINTS}" STREQUAL "")
  MESSAGE(WARNING "${PIO_FILESYSTEM_HINTS} not valid option for PIO_FILESYSTEM_HINTS; use gpfs or lustre.")
ENDIF()

find_package(NetCDF)
if(NetCDF_FOUND)
  message(STATUS "Building PIO with netcdf support ")
  target_compile_definitions(${PROJECT_NAME} PUBLIC _NETCDF)
  if (${NetCDF_HAS_PARALLEL})
    target_compile_definitions(${PROJECT_NAME} PUBLIC _NETCDF4)
  endif()
  target_link_libraries(${PROJECT_NAME} PUBLIC NetCDF::NetCDFF)
else()
  message(STATUS "Building PIO without netcdf support")
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
  message(STATUS "Building PIO with pnetcdf support ")
  target_compile_definitions(${PROJECT_NAME} PUBLIC _PNETCDF)
  target_link_libraries(${PROJECT_NAME} PUBLIC PnetCDF::PnetCDF)
else()
  message(STATUS "Building PIO without pnetcdf support ")
  target_compile_definitions(${PROJECT_NAME} PUBLIC _NOPNETCDF)
endif()

OPTION(PIO_USE_MPIIO "Enable support for MPI-IO (default auto detect)" ON)
IF (PIO_USE_MPIIO)
  TRY_COMPILE(MPIIO_SUCCESS ${CMAKE_CURRENT_BINARY_DIR}/tryCompileMPIIO
                            ${TESTFILEPATH}/TryMPIIO.f90)
  IF (${MPIIO_SUCCESS})
    MESSAGE(STATUS "MPIIO detected and enabled.")
  ELSE()
    MESSAGE(STATUS "MPIIO not detected and therefore disabled.")
    SET(PIO_USE_MPIIO FALSE)
  ENDIF()
ENDIF()
IF (${PIO_USE_MPIIO})
  target_compile_definitions(${PROJECT_NAME} PUBLIC USEMPIIO)
ENDIF()

target_compile_definitions(${PROJECT_NAME} PRIVATE _NOUSEMCT)

OPTION(PIO_USE_BOX  "" ON)
if(PIO_USE_BOX)
  target_compile_definitions(${PROJECT_NAME} PRIVATE _USEBOX)
else()
  target_compile_definitions(${PROJECT_NAME} PRIVATE _NOUSEBOX)
endif()

OPTION(PIO_USE_MPIMOD "Use Fortran MPI module (default auto detect)" ON)
IF (PIO_USE_MPIMOD)
  TRY_COMPILE(MPIMOD_SUCCESS ${CMAKE_CURRENT_BINARY_DIR}/tryCompileMPIMod
                             ${TESTFILEPATH}/TryMPIMod.f90)
  IF (${MPIMOD_SUCCESS})
    MESSAGE(STATUS "MPI Fortran module detected and enabled.")
  ELSE()
    MESSAGE(STATUS "MPI Fortran module not detected and therefore disabled.")
    SET(PIO_USE_MPIMOD FALSE)
  ENDIF()
ENDIF()

IF (NOT ${PIO_USE_MPIMOD})
  target_compile_definitions(${PROJECT_NAME} PRIVATE NO_MPIMOD)
ENDIF()
OPTION(PIO_BUILD_TIMING  "" OFF)

if(${PIO_BUILD_TIMING})
  if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/../timing)
    target_compile_definitions(${PROJECT_NAME} PRIVATE TIMING -I ${CMAKE_CURRENT_BINARY_DIR}/timing)
    ADD_SUBDIRECTORY(../timing timing)
  endif()
endif()

SET(SRCS_C topology.c)

SET(SRCS_F90 pio.F90 pio_kinds.F90 nf_mod.F90  ionf_mod.F90 pio_types.F90
             piolib_mod.F90 pio_mpi_utils.F90 pio_nf_utils.F90 pio_utils.F90
             pio_support.F90                                calcdisplace_mod.F90
	     calcdecomp.F90 pio_msg_mod.F90 pio_msg_callbacks.F90)

SET(TEMPSRCF90    pionfatt_mod.F90
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
	                        pio_msg_getput_callbacks.F90
        )

FOREACH(tempfile IN LISTS TEMPSRCF90)
ADD_CUSTOM_COMMAND(
	OUTPUT ${tempfile}
	COMMAND ${GENF90} ${CMAKE_CURRENT_SOURCE_DIR}/${tempfile}.in > ${tempfile}
	DEPENDS  ${tempfile}.in
)
ENDFOREACH()
if("${CMAKE_Fortran_COMPILER_ID}" STREQUAL "GNU")
   SET(CMAKE_Fortran_FLAGS	"${CMAKE_Fortran_FLAGS} -ffree-line-length-none")
endif()

target_sources(${PROJECT_NAME} PRIVATE ${SRCS_F90} ${SRCS_C} ${TEMPSRCF90})

if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/../unittests)
  ADD_SUBDIRECTORY(../unittests unittests)
endif()
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/../testpio)
  ADD_SUBDIRECTORY(../testpio testpio)
endif()

install (TARGETS ${PROJECT_NAME} ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
cmake_minimum_required (VERSION 3.16.3)

project(externals)

include(ExternalProject)
set(SHARED_LIBS ${CMAKE_CURRENT_BINARY_DIR}/shared)
file(MAKE_DIRECTORY ${SHARED_LIBS}/include ${SHARED_LIBS}/lib)

ExternalProject_Add(gptl
    PREFIX            gptl
    SOURCE_DIR        ${CMAKE_CURRENT_SOURCE_DIR}/gptl
    BUILD_IN_SOURCE   FALSE
    CONFIGURE_COMMAND echo "" > ${CMAKE_CURRENT_BINARY_DIR}/gptl/Macros.make
    BUILD_COMMAND     ""
    INSTALL_COMMAND   make install -f ${CMAKE_CURRENT_SOURCE_DIR}/gptl/Makefile
                      MACFILE=${CMAKE_CURRENT_BINARY_DIR}/gptl/Macros.make
                      MPICC=${CMAKE_C_COMPILER}
                      MPIFC=${CMAKE_Fortran_COMPILER}
                      GPTL_DIR=${CMAKE_CURRENT_SOURCE_DIR}/gptl 
                      SHAREDPATH=${SHARED_LIBS}       
)

ExternalProject_Add(mct
    PREFIX            mct
    SOURCE_DIR        ${CMAKE_CURRENT_SOURCE_DIR}/mct
    BUILD_IN_SOURCE   TRUE
    CONFIGURE_COMMAND ./configure 
                      --prefix=${SHARED_LIBS} 
                      --exec-prefix=${SHARED_LIBS}
                      CC=${CMAKE_C_COMPILER}
                      FC=${CMAKE_Fortran_COMPILER}
    INSTALL_COMMAND   make install && 
                      make clean && 
                      mv -t ${CMAKE_CURRENT_BINARY_DIR}/mct config.h config.status config.log Makefile.conf
)

message(STATUS "CMake variables required by PIO:")
message(STATUS "GENF90_PATH=$CACHE{GENF90_PATH}")
message(STATUS "CMAKE_MODULE_PATH=$CACHE{CMAKE_MODULE_PATH}")
message(STATUS "NetCDF_ROOT=$CACHE{NetCDF_ROOT}")
set(PIO_BLD_DIR ${CMAKE_CURRENT_BINARY_DIR}/pio1/bld)
ExternalProject_Add(pio1
    PREFIX            pio1
    SOURCE_DIR        ${CMAKE_CURRENT_SOURCE_DIR}/pio1
    INSTALL_DIR       ${SHARED_LIBS}
    CONFIGURE_COMMAND cmake
                      -S ${CMAKE_CURRENT_SOURCE_DIR}/pio1
                      -B ${PIO_BLD_DIR}
                      -D GENF90_PATH=$CACHE{GENF90_PATH}
                      -D USER_CMAKE_MODULE_PATH=$CACHE{CMAKE_MODULE_PATH}
                      -D CMAKE_C_COMPILER=${CMAKE_C_COMPILER}
                      -D CMAKE_Fortran_COMPILER=${CMAKE_Fortran_COMPILER}
                      -D NetCDF_PATH=$CACHE{NetCDF_ROOT}
                      -D PnetCDF_PATH=$CACHE{NetCDF_ROOT}
                      -D CMAKE_INSTALL_PREFIX=${SHARED_LIBS}
    BUILD_COMMAND     cmake --build ${PIO_BLD_DIR} 
    INSTALL_COMMAND   cmake --install ${PIO_BLD_DIR}
)
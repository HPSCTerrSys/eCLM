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
    BUILD_ALWAYS      YES      
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
    BUILD_ALWAYS      YES 
)
add_subdirectory(pio1)
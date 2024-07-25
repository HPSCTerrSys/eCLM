cmake_minimum_required (VERSION 3.16.3)
project(externals LANGUAGES C Fortran)
include(ExternalProject)

# ===========
#    GPTL
# ===========
set(GPTL_BLD_DIR ${CMAKE_CURRENT_BINARY_DIR}/gptl)
file(MAKE_DIRECTORY ${GPTL_BLD_DIR}/include ${GPTL_BLD_DIR}/lib)

set(GPTL_MACROS_FILE ${GPTL_BLD_DIR}/Macros.make)
file(WRITE  ${GPTL_MACROS_FILE} "  MPICC := ${CMAKE_C_COMPILER}\n")
file(APPEND ${GPTL_MACROS_FILE} "  MPIFC := ${CMAKE_Fortran_COMPILER}\n")
file(APPEND ${GPTL_MACROS_FILE} "  CLAGS := ${CMAKE_C_FLAGS}\n")
file(APPEND ${GPTL_MACROS_FILE} " FFLAGS := ${CMAKE_Fortran_FLAGS}\n")
file(APPEND ${GPTL_MACROS_FILE} "CPPDEFS := -DFORTRANUNDERSCORE\n")

ExternalProject_Add(gptl_external
    PREFIX            gptl
    SOURCE_DIR        ${CMAKE_CURRENT_SOURCE_DIR}/gptl
    BUILD_IN_SOURCE   FALSE
    CONFIGURE_COMMAND ""
    BUILD_COMMAND     make install -f ${CMAKE_CURRENT_SOURCE_DIR}/gptl/Makefile         
                      MACFILE=${GPTL_BLD_DIR}/Macros.make
                      GPTL_DIR=${CMAKE_CURRENT_SOURCE_DIR}/gptl
                      SHAREDPATH=${GPTL_BLD_DIR}
    INSTALL_COMMAND   ""
    BUILD_ALWAYS      YES
    BUILD_BYPRODUCTS  ${GPTL_BLD_DIR}/lib/libgptl.a
)

add_library(gptl INTERFACE IMPORTED GLOBAL)
target_include_directories(gptl INTERFACE ${GPTL_BLD_DIR}/include)
target_link_directories(gptl INTERFACE ${GPTL_BLD_DIR}/lib)
target_link_libraries(gptl INTERFACE libgptl.a)
add_dependencies(gptl gptl_external)
install (FILES ${GPTL_BLD_DIR}/lib/libgptl.a TYPE LIB)


# ===========
#     MCT
# ===========
option(BUILD_MCT "Use built-in MCT library." ON)
add_library(mct INTERFACE IMPORTED GLOBAL)
if (BUILD_MCT)
    set(MCT_BLD_DIR ${CMAKE_CURRENT_BINARY_DIR}/mct)
    file(MAKE_DIRECTORY ${MCT_BLD_DIR}/include ${MCT_BLD_DIR}/lib)
    ExternalProject_Add(mct_external
        PREFIX            mct
        SOURCE_DIR        ${CMAKE_CURRENT_SOURCE_DIR}/mct
        BUILD_IN_SOURCE   TRUE
        CONFIGURE_COMMAND ./configure
                        --prefix=${MCT_BLD_DIR}
                        --exec-prefix=${MCT_BLD_DIR}
                        CC=${CMAKE_C_COMPILER}
                        FC=${CMAKE_Fortran_COMPILER}
                        MPIFC=${CMAKE_Fortran_COMPILER}
                        CFLAGS=${CMAKE_C_FLAGS}
                        FCFLAGS=${CMAKE_Fortran_FLAGS}
        BUILD_ALWAYS      YES
        BUILD_BYPRODUCTS  ${GPTL_BLD_DIR}/lib/libmct.a ${GPTL_BLD_DIR}/lib/libmpeu.a
    )
    target_include_directories(mct INTERFACE ${MCT_BLD_DIR}/include)
    target_link_directories(mct INTERFACE ${MCT_BLD_DIR}/lib)
    target_link_libraries(mct INTERFACE libmct.a libmpeu.a)
    add_dependencies(mct mct_external) 
    install (FILES ${MCT_BLD_DIR}/lib/libmct.a ${MCT_BLD_DIR}/lib/libmpeu.a TYPE LIB)
else()
    find_package(MCT REQUIRED)
    if (${MCT_FOUND})
        target_include_directories(mct SYSTEM INTERFACE ${MCT_INCLUDE_DIR})
        target_link_libraries(mct INTERFACE ${MCT_LIBRARIES})
    endif()
endif()

# ===========
#     PIO
# ===========
add_subdirectory(pio1)

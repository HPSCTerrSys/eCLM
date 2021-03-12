# This module sets the required compile flags and definitions for all targets.

if(UNIX AND NOT APPLE)
    add_compile_definitions(LINUX)
endif()

# Set default build = RELEASE if none was specified. 
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE "RELEASE" CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "DEBUG" "RELEASE")
endif()

# Set default compiler = GNU if none was specified. 
if(NOT COMPILER)
    set(COMPILER "GNU" CACHE STRING "Choose compiler toolchain." FORCE)
    set_property(CACHE COMPILER PROPERTY STRINGS "GNU" "Intel")
endif()

if(COMPILER STREQUAL "GNU")
    add_compile_definitions(CPRGNU)
    set(CMAKE_C_FLAGS "-std=gnu99")
    set(CMAKE_C_FLAGS_DEBUG "-fcheck=bounds")
    set(CMAKE_C_FLAGS_RELEASE "-O")
    set(CMAKE_Fortran_FLAGS "-fconvert=big-endian -ffree-line-length-none -ffixed-line-length-none -ffree-form")
    set(CMAKE_Fortran_FLAGS_DEBUG "-g -Wall -Og -fbacktrace -ffpe-trap=zero,overflow -fcheck=bounds")
    set(CMAKE_Fortran_FLAGS_RELEASE "-O") 
elseif(COMPILER STREQUAL "Intel")
    add_compile_definitions(CPRINTEL)
    set(CMAKE_C_FLAGS -qno-opt-dynamic-align -std=gnu99 "SHELL:-fp-model precise -debug minimal")
    set(CMAKE_C_FLAGS_DEBUG "-O0 -g")
    set(CMAKE_C_FLAGS_RELEASE "-O2")
    set(CMAKE_Fortran_FLAGS -free -qno-opt-dynamic-align -ftz -traceback "SHELL:-convert big_endian -assume byterecl -assume realloc_lhs -fp-model source")
    set(CMAKE_Fortran_FLAGS_DEBUG "-O0 -g -check uninit -check bounds -check pointers -fpe0 -check noarg_temp_created")
    set(CMAKE_Fortran_FLAGS_RELEASE "-O2 -debug minimal") 
else()
    message(FATAL_ERROR "COMPILER='${COMPILER}' is not supported.")
endif()

message(STATUS " ******* ${CMAKE_PROJECT_NAME} build options ******* ")
message(STATUS " Build type = '${CMAKE_BUILD_TYPE}'")
message(STATUS " Compiler = '${COMPILER}'")
message(STATUS " *************************************** ")
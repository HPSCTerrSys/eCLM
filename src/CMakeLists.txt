cmake_minimum_required (VERSION 3.16.3)

project (clm5-tsmp LANGUAGES C Fortran)

# Set global compile features and definitions
if(UNIX AND NOT APPLE)
    add_compile_definitions(LINUX)
endif()

if(CMAKE_C_COMPILER_ID STREQUAL "GNU")
    set(cdefs CPRGNU)
    set(cflags -O -std=gnu99)
elseif(CMAKE_C_COMPILER_ID STREQUAL "Intel")
    set(cdefs CPRINTEL)
    set(cflags -qno-opt-dynamic-align -std=gnu99 -O2 "SHELL:-fp-model precise -debug minimal")
endif()

if(CMAKE_Fortran_COMPILER_ID STREQUAL "GNU")
    set(fdefs CPRGNU)
    set(fflags -ffree-form -ffree-line-length-none -fconvert=big-endian -O)
elseif(CMAKE_Fortran_COMPILER_ID STREQUAL "Intel")
    set(fdefs CPRINTEL)
    set(fflags -free -qno-opt-dynamic-align -ftz -traceback -O2 "SHELL:-convert big_endian -assume byterecl -assume realloc_lhs -fp-model source -debug minimal")
endif()

add_compile_options("$<$<COMPILE_LANGUAGE:Fortran>:${fflags}>")
add_compile_options("$<$<COMPILE_LANGUAGE:C>:${cflags}>")
add_compile_definitions("$<$<COMPILE_LANGUAGE:Fortran>:${fdefs}>")
add_compile_definitions($<$<COMPILE_LANGUAGE:C>:${cdefs}>)

add_subdirectory(externals)
add_subdirectory(csm_share)
add_subdirectory(clm5)
project (csm_share LANGUAGES C Fortran)

add_library(${PROJECT_NAME} STATIC)

# TODO: NUM_COMP_INST_<COMP> should be adjusted for ensemble runs. See the ff. for more info:
# https://esmci.github.io/cime/versions/cesm2.2/html/users_guide/multi-instance.html
# https://github.com/ESMCI/cime/blob/cime5.6.33/src/build_scripts/buildlib.csm_share#L63
# https://github.com/ESMCI/cime/blob/cime5.6.33/src/drivers/mct/cime_config/config_component.xml#L1989

target_compile_definitions(${PROJECT_NAME} 
    PUBLIC 
        NDEBUG
        FORTRANUNDERSCORE
        NUM_COMP_INST_ATM=1
        NUM_COMP_INST_LND=1
        NUM_COMP_INST_ICE=1
        NUM_COMP_INST_OCN=1
        NUM_COMP_INST_ROF=1
        NUM_COMP_INST_GLC=1
        NUM_COMP_INST_WAV=1
        NUM_COMP_INST_ESP=1
        HAVE_IEEE_ARITHMETIC
)

target_include_directories(${PROJECT_NAME} PRIVATE esmf_wrf_timemgr)
target_include_directories(${PROJECT_NAME} PUBLIC include)
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_BINARY_DIR})

set(F90IN_FILES util/shr_assert_mod.F90.in
                util/shr_frz_mod.F90.in
                util/shr_infnan_mod.F90.in)

set(PREPROCESSED_F90_FILES "")
foreach(f90in_file IN LISTS F90IN_FILES)
    get_filename_component(filename_noext ${f90in_file} NAME_WE)
    set(outfile "${CMAKE_CURRENT_BINARY_DIR}/${filename_noext}.F90")
    add_custom_command(
        OUTPUT ${outfile}
        COMMAND ${GENF90} ${CMAKE_CURRENT_SOURCE_DIR}/${f90in_file} > ${outfile}
        DEPENDS  ${CMAKE_CURRENT_SOURCE_DIR}/${f90in_file}
    )
    list(APPEND PREPROCESSED_F90_FILES ${outfile})
endforeach()

target_sources(${PROJECT_NAME} PRIVATE ${PREPROCESSED_F90_FILES})

target_sources(${PROJECT_NAME} PRIVATE 
    esmf_wrf_timemgr/ESMF_AlarmClockMod.F90
    esmf_wrf_timemgr/ESMF_AlarmMod.F90
    esmf_wrf_timemgr/ESMF_BaseMod.F90
    esmf_wrf_timemgr/ESMF_BaseTimeMod.F90
    esmf_wrf_timemgr/ESMF_CalendarMod.F90
    esmf_wrf_timemgr/ESMF_ClockMod.F90
    esmf_wrf_timemgr/ESMF.F90
    esmf_wrf_timemgr/ESMF_FractionMod.F90
    esmf_wrf_timemgr/ESMF_ShrTimeMod.F90
    esmf_wrf_timemgr/ESMF_Stubs.F90
    esmf_wrf_timemgr/ESMF_TimeIntervalMod.F90
    esmf_wrf_timemgr/ESMF_TimeMod.F90
    esmf_wrf_timemgr/MeatMod.F90
    esmf_wrf_timemgr/wrf_error_fatal.F90
    esmf_wrf_timemgr/wrf_message.F90
    mct/glc_elevclass_mod.F90
    mct/seq_cdata_mod.F90
    mct/seq_comm_mct.F90
    mct/seq_drydep_mod.F90
    mct/seq_flds_mod.F90
    mct/seq_infodata_mod.F90
    mct/seq_io_read_mod.F90
    mct/seq_timemgr_mod.F90
    mct/shr_carma_mod.F90
    mct/shr_expr_parser_mod.F90
    mct/shr_fire_emis_mod.F90
    mct/shr_megan_mod.F90
    mct/shr_ndep_mod.F90
    streams/shr_dmodel_mod.F90
    streams/shr_strdata_mod.F90
    streams/shr_stream_mod.F90
    streams/shr_tInterp_mod.F90
    util/mct_mod.F90
    util/shr_abort_mod.F90
    util/shr_cal_mod.F90
    util/shr_const_mod.F90
    util/shr_file_mod.F90
    util/shr_flds_mod.F90
    util/shr_flux_mod.F90
    util/shr_kind_mod.F90
    util/shr_log_mod.F90
    util/shr_map_mod.F90
    util/shr_mct_mod.F90
    util/shr_mem_mod.F90
    util/shr_mpi_mod.F90
    util/shr_msg_mod.F90
    util/shr_ncread_mod.F90
    util/shr_nl_mod.F90
    util/shr_orb_mod.F90
    util/shr_pcdf_mod.F90
    util/shr_pio_mod.F90
    util/shr_precip_mod.F90
    util/shr_reprosum_mod.F90
    util/shr_reprosumx86.c
    util/shr_scam_mod.F90
    util/shr_spfn_mod.F90
    util/shr_strconvert_mod.F90
    util/shr_string_mod.F90
    util/shr_sys_mod.F90
    util/shr_timer_mod.F90
    util/shr_vmath_mod.F90
    util/shr_wv_sat_mod.F90
    util/water_isotopes.F90
    util/water_types.F90
)

target_link_libraries(${PROJECT_NAME} PUBLIC pio mct gptl)
if (USE_OASIS)
    find_package(OASIS3MCT REQUIRED)
    if (OASIS3MCT_FOUND)
        target_link_libraries(${PROJECT_NAME} PUBLIC OASIS3MCT::OASIS3MCT)
        target_compile_definitions(${PROJECT_NAME} PUBLIC USE_OASIS)
        option(COUP_OAS_ICON "Couple eCLM with ICON" OFF)
        if(COUP_OAS_ICON)
             target_compile_definitions(${PROJECT_NAME} PUBLIC COUP_OAS_ICON)
        endif()
        option(COUP_OAS_PFL "Couple eCLM with ParFlow" OFF)
	    if(COUP_OAS_PFL)
             target_compile_definitions(${PROJECT_NAME} PUBLIC COUP_OAS_PFL)
        endif()
    endif()
endif()

if (USE_PDAF)
  target_compile_definitions(${PROJECT_NAME} PUBLIC USE_PDAF)
endif()

if (ENABLE_TESTS)
    add_subdirectory(util/test)
endif()

install (TARGETS ${PROJECT_NAME} ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})

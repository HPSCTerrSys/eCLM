project (eclm LANGUAGES Fortran)

add_executable(${PROJECT_NAME})
set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".exe")

target_sources(${PROJECT_NAME} 
  PRIVATE
    cime_comp_mod.F90
    cime_driver.F90
    component_mod.F90
    component_type_mod.F90
    cplcomp_exchange_mod.F90
    map_glc2lnd_mod.F90
    map_lnd2glc_mod.F90
    map_lnd2rof_irrig_mod.F90
    mrg_mod.F90
    prep_aoflux_mod.F90
    prep_atm_mod.F90
    prep_glc_mod.F90
    prep_ice_mod.F90
    prep_lnd_mod.F90
    prep_ocn_mod.F90
    prep_rof_mod.F90
    prep_wav_mod.F90
    seq_diag_mct.F90
    seq_domain_mct.F90
    seq_flux_mct.F90
    seq_frac_mct.F90
    seq_hist_mod.F90
    seq_io_mod.F90
    seq_map_mod.F90
    seq_map_type_mod.F90
    seq_rest_mod.F90
    t_driver_timers_mod.F90
)

target_link_libraries(${PROJECT_NAME} PRIVATE clm mosart ocn wav ice glc esp csm_share)
if(COUP_OAS_ICON)
    target_link_libraries(${PROJECT_NAME} PRIVATE icon_atm)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE datm)
endif()
install (TARGETS ${PROJECT_NAME} ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
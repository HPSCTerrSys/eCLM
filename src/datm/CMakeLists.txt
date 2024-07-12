project (datm LANGUAGES Fortran)

add_library(${PROJECT_NAME} STATIC)

target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
target_link_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_BINARY_DIR})

target_sources(${PROJECT_NAME} 
    PRIVATE 
        datm_shr_mod.F90
        datm_comp_mod.F90
        atm_comp_mct.F90
)
target_link_libraries(${PROJECT_NAME} PRIVATE csm_share)
install (TARGETS ${PROJECT_NAME} ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
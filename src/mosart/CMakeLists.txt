project (mosart LANGUAGES Fortran)

add_library(${PROJECT_NAME} STATIC)

target_sources(${PROJECT_NAME} PRIVATE 
    src/cpl/rof_cpl_indices.F90
    src/cpl/rof_comp_mct.F90
    src/riverroute/RtmIO.F90
    src/riverroute/MOSART_physics_mod.F90
    src/riverroute/RtmRestFile.F90
    src/riverroute/RtmMod.F90
    src/riverroute/RtmDateTime.F90
    src/riverroute/RtmFileUtils.F90
    src/riverroute/RtmVar.F90
    src/riverroute/RtmHistFile.F90
    src/riverroute/RtmSpmd.F90
    src/riverroute/RtmHistFlds.F90
    src/riverroute/RunoffMod.F90
    src/riverroute/RtmTimeManager.F90
)

target_link_libraries(${PROJECT_NAME} PRIVATE csm_share)
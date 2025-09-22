# shr_abort_test
add_pfunit_ctest (${PROJECT_NAME}_abort
    TEST_SOURCES
        shr_abort_test/test_shr_abort.pf
    LINK_LIBRARIES ${PROJECT_NAME}
)

# shr_assert_test
add_pfunit_ctest (${PROJECT_NAME}_assert
    TEST_SOURCES
        shr_assert_test/test_assert_array.pf
        shr_assert_test/test_assert.pf
        shr_assert_test/test_macro.pf
        shr_assert_test/test_ndebug.pf
    LINK_LIBRARIES ${PROJECT_NAME}
)

# shr_cal_test
add_pfunit_ctest (${PROJECT_NAME}_calendar
    TEST_SOURCES
        shr_cal_test/test_shr_cal.pf
    LINK_LIBRARIES ${PROJECT_NAME}
)

# shr_log_test
add_pfunit_ctest (${PROJECT_NAME}_log
    TEST_SOURCES
        shr_log_test/test_error_printers.pf
    LINK_LIBRARIES ${PROJECT_NAME}
)

# shr_precip_test
add_pfunit_ctest (${PROJECT_NAME}_precip
    TEST_SOURCES
        shr_precip_test/test_shr_precip.pf
    LINK_LIBRARIES ${PROJECT_NAME}
)

# shr_spfn_test
add_pfunit_ctest (${PROJECT_NAME}_spfn
    TEST_SOURCES
        shr_spfn_test/test_erf_r4.pf
        shr_spfn_test/test_erf_r8.pf
        shr_spfn_test/test_gamma_factorial.pf
        shr_spfn_test/test_igamma.pf
    LINK_LIBRARIES ${PROJECT_NAME}
)

# shr_strconvert_test
add_pfunit_ctest (${PROJECT_NAME}_strconvert
    TEST_SOURCES
        shr_strconvert_test/test_toString.pf
    LINK_LIBRARIES ${PROJECT_NAME}
)

# shr_string_test
add_pfunit_ctest (${PROJECT_NAME}_string
    TEST_SOURCES
        shr_string_test/test_shr_string.pf
    LINK_LIBRARIES ${PROJECT_NAME}
)

# shr_wv_sat_test
add_pfunit_ctest (${PROJECT_NAME}_wv_sat
    TEST_SOURCES
        shr_wv_sat_test/test_wv_sat_each_method.pf
        shr_wv_sat_test/test_wv_sat.pf
    LINK_LIBRARIES ${PROJECT_NAME}
)
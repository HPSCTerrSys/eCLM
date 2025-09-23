# shr_abort_test
add_pfunit_ctest (csm_share_abort
    TEST_SOURCES
        shr_abort_test/shr_abort_mod_abortthrows.F90
        shr_abort_test/test_shr_abort.pf
    LINK_LIBRARIES csm_share
)

# shr_assert_test
add_pfunit_ctest (csm_share_assert
    TEST_SOURCES
        shr_assert_test/test_assert_array.pf
        shr_assert_test/test_assert.pf
        shr_assert_test/test_macro.pf
        shr_assert_test/test_ndebug.pf
    LINK_LIBRARIES csm_share
)

# shr_cal_test
add_pfunit_ctest (csm_share_calendar
    TEST_SOURCES
        shr_cal_test/test_shr_cal.pf
    LINK_LIBRARIES csm_share
)

# shr_log_test
add_pfunit_ctest (csm_share_log
    TEST_SOURCES
        shr_log_test/test_error_printers.pf
    LINK_LIBRARIES csm_share
)

# shr_precip_test
add_pfunit_ctest (csm_share_precip
    TEST_SOURCES
        shr_precip_test/test_shr_precip.pf
    LINK_LIBRARIES csm_share
)

# shr_spfn_test
add_pfunit_ctest (csm_share_spfn
    TEST_SOURCES
        shr_spfn_test/test_erf_r4.pf
        shr_spfn_test/test_erf_r8.pf
        shr_spfn_test/test_gamma_factorial.pf
        shr_spfn_test/test_igamma.pf
    LINK_LIBRARIES csm_share
)

# shr_strconvert_test
add_pfunit_ctest (csm_share_strconvert
    TEST_SOURCES
        shr_strconvert_test/test_toString.pf
    LINK_LIBRARIES csm_share
)

# shr_string_test
add_pfunit_ctest (csm_share_string
    TEST_SOURCES
        shr_string_test/test_shr_string.pf
    LINK_LIBRARIES csm_share
)

# shr_wv_sat_test
add_pfunit_ctest (csm_share_wv_sat
    TEST_SOURCES
        shr_wv_sat_test/test_wv_sat_each_method.pf
        shr_wv_sat_test/test_wv_sat.pf
    LINK_LIBRARIES csm_share
)

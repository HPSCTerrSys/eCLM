module dynCovercropFileMod

#include "shr_assert.h"

  !---------------------------------------------------------------------------
  ! !DESCRIPTION:
  ! Read the cover-crop rotation file and switch patch ivt after harvest.
  !
  ! Rotation file format:
  !   dimensions: time, cft, lndgrid
  !   integer YEAR(time)                  -- calendar year per time slice
  !   real    PCT_CFT(time, cft, lndgrid) -- CFT fractions 0-100%
  !
  ! After harvest of any cash crop, covercrop_switch_ivt finds the dominant
  ! CFT in the next year slice for this gridcell and switches ivt(p).
  ! Works identically for point and regional/global domains.
  !
  ! Backward compatibility:
  !   use_covercropping = .false. -> never called, zero overhead
  !   use_covercropping = .true.  -> transient_landuse_file must be set
  ! tboas
  !
  ! !USES:
  use shr_kind_mod            , only : r8 => shr_kind_r8
  use shr_log_mod             , only : errMsg => shr_log_errMsg
  use decompMod               , only : bounds_type, BOUNDS_LEVEL_PROC
  use dynFileMod              , only : dyn_file_type
  use clm_varctl              , only : iulog, use_covercropping, transient_landuse_file
  use clm_varctl              , only : debug_covercrop  ! tboas-fix
  use pftconMod               , only : nwwheat, nirrig_wwheat, nwbarley, nirrig_wbarley, ncovercrop_1, ncovercrop_2  ! tboas
  use CNVegCarbonStateType    , only : cnveg_carbonstate_type  ! tboas
  use CNVegNitrogenStateType  , only : cnveg_nitrogenstate_type  ! tboas
  use clm_varcon              , only : grlnd
  use clm_varpar              , only : cft_size, cft_lb
  use abortutils              , only : endrun
  use histFileMod             , only : hist_addfld1d
  use spmdMod                 , only : masterproc
  use PatchType               , only : patch
  use pftconMod               , only : pftcon, ncovercrop_1, ncovercrop_2
  !
  implicit none
  private
  save

  public :: dyncovercrop_init
  public :: dyncovercrop_interp
  public :: covercrop_switch_ivt
  public :: covercrop_target_ivt  ! tboas

  !---------------------------------------------------------------------------
  type(dyn_file_type), target :: dyncovercrop_file
  real(r8), allocatable :: pct_cft_cur (:,:)  ! (begg:endg, cft_size)
  real(r8), allocatable :: pct_cft_next(:,:)  ! (begg:endg, cft_size)
  real(r8), allocatable :: pct_cft_winter(:,:)  ! (begg:endg, cft_size) tboas
  logical               :: has_winter_slot = .false.  ! tboas
  integer               :: last_year_index = -1       ! tboas: read cache
  real(r8), pointer :: active_ivt_patch(:) => null() ! (begp:endp) active itype for history  ! tboas

  character(len=*), parameter, private :: sourcefile = __FILE__

contains

  !-----------------------------------------------------------------------
  subroutine dyncovercrop_init(bounds)
    use dynTimeInfoMod        , only : YEAR_POSITION_START_OF_TIMESTEP
    use dynVarTimeUninterpMod , only : dyn_var_time_uninterp_type
    use ncdio_pio             , only : check_dim
    type(bounds_type), intent(in) :: bounds
    type(dyn_var_time_uninterp_type) :: wtcft_obj
    integer :: num_points, pct_cft_shape(2), pi
    character(len=*), parameter :: subname = "dyncovercrop_init"
    !-----------------------------------------------------------------------
    SHR_ASSERT_ALL(bounds%level == BOUNDS_LEVEL_PROC, &
         subname // ": argument must be PROC-level bounds")
    if (.not. use_covercropping) return
    if (trim(transient_landuse_file) == "" .or. &
        trim(transient_landuse_file) == " ") then
       call endrun(msg=" ERROR: use_covercropping=.true. but transient_landuse_file" // &
            " is not set in lnd_in." // errMsg(sourcefile, __LINE__))
    end if
    if (masterproc) write(iulog,*) &
         "dyncovercrop_init: opening ", trim(transient_landuse_file)
    dyncovercrop_file = dyn_file_type( &
         trim(transient_landuse_file), YEAR_POSITION_START_OF_TIMESTEP)
    call check_dim(dyncovercrop_file, "cft", cft_size)
    num_points    = bounds%endg - bounds%begg + 1
    pct_cft_shape = [num_points, cft_size]
    allocate(pct_cft_cur (bounds%begg:bounds%endg, cft_size))
    allocate(pct_cft_next(bounds%begg:bounds%endg, cft_size))
    allocate(pct_cft_winter(bounds%begg:bounds%endg, cft_size))
    pct_cft_cur    = 0._r8
    pct_cft_next   = 0._r8
    pct_cft_winter = 0._r8
    call dyncovercrop_interp(bounds)

    ! Register IVT as history field for rotation diagnostics --- tboas
    allocate(active_ivt_patch(bounds%begp:bounds%endp))
    do pi = bounds%begp, bounds%endp
       active_ivt_patch(pi) = real(patch%itype(pi), r8)
    end do
    call hist_addfld1d(fname='IVT', units='unitless', &
         avgflag='I', long_name='current patch vegetation type index', &
         ptr_patch=active_ivt_patch, default='active')
  end subroutine dyncovercrop_init

  !-----------------------------------------------------------------------
  subroutine dyncovercrop_interp(bounds)
    use dynVarTimeUninterpMod , only : dyn_var_time_uninterp_type
    use ncdio_pio             , only : ncd_io
    type(bounds_type), intent(in) :: bounds
    type(dyn_var_time_uninterp_type) :: wtcft_obj
    integer :: num_points, pct_cft_shape(2), pi
    integer :: idx_next, ntimes
    integer :: cur_year_index  ! tboas
    real(r8), pointer :: raw_next(:,:)  ! (lndgrid, cft) pointer for ncd_io_2d
    logical :: readvar
    !-----------------------------------------------------------------------
    if (.not. use_covercropping)       return
    if (.not. allocated(pct_cft_cur))  return
    call dyncovercrop_file%time_info%set_current_year()

    ! tboas: the file only changes when the year index changes. Without this
    ! guard the slices below are re-read on every timestep -- 17520 reads per
    ! simulated year at dtime=1800s, which dominates runtime on a regional grid.
    cur_year_index = dyncovercrop_file%time_info%get_time_index_lower()
    if (cur_year_index /= last_year_index) then
       num_points    = bounds%endg - bounds%begg + 1
       pct_cft_shape = [num_points, cft_size]

       ! Read current year PCT_CFT via standard mechanism
       wtcft_obj = dyn_var_time_uninterp_type( &
            dyn_file              = dyncovercrop_file, &
            varname               = "PCT_CFT", &
            dim1name              = grlnd, &
            conversion_factor     = 100._r8, &
            do_check_sums_equal_1 = .false., &
            data_shape            = pct_cft_shape)
       call wtcft_obj%get_current_data(pct_cft_cur(bounds%begg:bounds%endg, :))

       ! Read next year PCT_CFT directly via ncd_io_2d at time_index_lower + 1
       ! This is needed for post-harvest planting of winter crops/cover crops
       ! which are sown in fall of current year but belong to next year's rotation
       ntimes   = dyncovercrop_file%time_info%get_time_index_upper()
       idx_next = min(dyncovercrop_file%time_info%get_time_index_lower() + 1, ntimes)
       nullify(raw_next)
       allocate(raw_next(num_points, cft_size))
       call ncd_io(varname="PCT_CFT", data=raw_next, dim1name=grlnd, &
            flag="read", ncid=dyncovercrop_file, nt=idx_next, readvar=readvar)
       if (readvar) then
          pct_cft_next(bounds%begg:bounds%endg, :) = raw_next * 100._r8
       else
          ! Fallback: end of timeseries — use current year
          pct_cft_next(bounds%begg:bounds%endg, :) = pct_cft_cur(bounds%begg:bounds%endg, :)
          if (masterproc) write(iulog,*) "dyncovercrop_interp: end of timeseries, using current year for pct_cft_next"
       end if
       deallocate(raw_next)

       ! tboas: optional winter cover-crop slot, read at the CURRENT year index.
       ! PCT_CFT_WINTER(year N) is the cover crop sown in autumn of year N.
       allocate(raw_next(num_points, cft_size))
       call ncd_io(varname="PCT_CFT_WINTER", data=raw_next, dim1name=grlnd, &
            flag="read", ncid=dyncovercrop_file, &
            nt=dyncovercrop_file%time_info%get_time_index_lower(), readvar=readvar)
       if (readvar) then
          pct_cft_winter(bounds%begg:bounds%endg, :) = raw_next * 100._r8
          has_winter_slot = .true.
       else
          pct_cft_winter(bounds%begg:bounds%endg, :) = 0._r8
          has_winter_slot = .false.
       end if
       deallocate(raw_next)
       last_year_index = cur_year_index
    end if

    ! Update IVT history field with current patch itype --- tboas
    if (associated(active_ivt_patch)) then
       do pi = bounds%begp, bounds%endp
          active_ivt_patch(pi) = real(patch%itype(pi), r8)
          ! tboas: debug write disabled for regional runs
          !if (pi == 2) write(iulog,*) 'IVT_TRACK: pi=',pi,' itype=',patch%itype(pi)  ! tboas
       end do
    end if
  end subroutine dyncovercrop_interp

  !-----------------------------------------------------------------------
  subroutine covercrop_switch_ivt(p, crop_inst, cnveg_state_inst, cnveg_carbonstate_inst, use_next, use_winter)
    use CropType              , only : crop_type
    use CNVegStateType        , only : cnveg_state_type
    integer               , intent(in)    :: p
    logical               , intent(in)    :: use_next  ! .true. = use pct_cft_next
    logical               , intent(in), optional :: use_winter  ! tboas
    type(crop_type)       , intent(inout) :: crop_inst
    type(cnveg_state_type), intent(inout) :: cnveg_state_inst
    type(cnveg_carbonstate_type), intent(inout) :: cnveg_carbonstate_inst
    integer  :: new_ivt
    integer, parameter :: NOT_Planted = 999
    !-----------------------------------------------------------------------
    if (.not. use_covercropping)       return
    if (.not. allocated(pct_cft_cur)) return
    new_ivt = covercrop_target_ivt(p, use_next, use_winter)
    if (new_ivt <= 0) return
    if (debug_covercrop) then
       write(iulog,*) 'SWITCH_DEBUG: new_ivt=',new_ivt,' patch%itype=',patch%itype(p),' use_next=',use_next  ! tboas
    end if
    if (new_ivt == patch%itype(p)) return
    ! tboas: no crop-type restriction — any crop can be switched to post-harvest
    patch%itype(p)                       = new_ivt
    if (associated(active_ivt_patch)) active_ivt_patch(p) = real(new_ivt, r8)
    crop_inst%croplive_patch(p)          = .false.
    crop_inst%cropplant_patch(p)         = .false.
    cnveg_state_inst%idop_patch(p)       = NOT_Planted
    ! Reset phenology GDD state so new crop starts fresh --- tboas
    crop_inst%gddplant_patch(p)              = 0._r8
    ! tboas: huigrain/gddmaturity NOT zeroed — CropPhenology derives them at
    ! planting; zeroing them makes 'hui < huigrain' impossible and locks the
    ! crop out of phase 2 permanently.
    ! cnveg_state_inst%huigrain_patch(p)       = 0._r8
    ! cnveg_state_inst%gddmaturity_patch(p)    = 0._r8
    crop_inst%harvdate_patch(p)              = NOT_Planted
    crop_inst%cphase_patch(p)                = 0._r8
    ! tboas: peaklai MUST be reset — if it carries over as 1 from the previous
    ! crop, CNPhenologyMod line ~2731 clamps hui up to huigrain on the first
    ! live timestep, making 'hui < huigrain' permanently false and locking the
    ! new crop out of phase 2 (no leaf emergence, no onset, leafc_xfer never drains).
    cnveg_state_inst%peaklai_patch(p)        = 0
    ! onset/offset flags NOT reset — onset_counter must go negative for crop onset to fire --- tboas
    ! Clear the previous crop's excess-maintenance-respiration pool --- tboas
    ! tboas-fix: xsmrpool is part of totc_patch, so assigning 0 here destroyed
    ! (or, for a negative pool, created) carbon with no matching flux, which is
    ! what forced the CNBalanceCheckMod tolerance up to 100 gC/m2/timestep.
    ! Move it into xsmrpool_loss instead: that pool is also inside totc_patch, so
    ! the transfer conserves carbon, and CNCStateUpdate1Mod releases it to the
    ! atmosphere through xsmrpool_to_atm, which the C balance already counts as
    ! an output.
    cnveg_carbonstate_inst%xsmrpool_loss_patch(p) = &
         cnveg_carbonstate_inst%xsmrpool_loss_patch(p) + &
         cnveg_carbonstate_inst%xsmrpool_patch(p)
    cnveg_carbonstate_inst%xsmrpool_patch(p) = 0._r8
    ! tboas: remaining C/N pools are kept from the previous crop
    ! tboas: use_grainproduct is a namelist flag and is NOT rewritten here.
    ! Mutating it made the last patch switched determine the setting for the
    ! whole domain. Grain-product suppression for cover crops is now decided
    ! per patch at the point of use, via pftconMod::is_covercrop.
  end subroutine covercrop_switch_ivt

  !-----------------------------------------------------------------------
  integer function covercrop_target_ivt(p, use_next, use_winter)
    ! tboas: return the dominant CFT for patch p as a global PFT index.
    ! Returns -1 if covercropping is off or the arrays are not allocated.
    integer, intent(in) :: p
    logical, intent(in) :: use_next   ! .true. = pct_cft_next, .false. = pct_cft_cur
    logical, intent(in), optional :: use_winter  ! tboas: PCT_CFT_WINTER slot
    integer  :: g, cft, best_cft
    real(r8) :: best_pct
    logical  :: want_winter
    !-----------------------------------------------------------------------
    covercrop_target_ivt = -1
    want_winter = .false.
    if (present(use_winter)) want_winter = use_winter .and. has_winter_slot
    if (.not. use_covercropping)      return
    if (.not. allocated(pct_cft_cur)) return
    if (use_next .and. .not. allocated(pct_cft_next)) return
    g = patch%gridcell(p)
    best_cft = 1
    best_pct = -1._r8
    do cft = 1, cft_size
       if (want_winter) then
          if (pct_cft_winter(g, cft) > best_pct) then
             best_pct = pct_cft_winter(g, cft)
             best_cft = cft
          end if
       else if (use_next) then
          if (pct_cft_next(g, cft) > best_pct) then
             best_pct = pct_cft_next(g, cft)
             best_cft = cft
          end if
       else
          if (pct_cft_cur(g, cft) > best_pct) then
             best_pct = pct_cft_cur(g, cft)
             best_cft = cft
          end if
       end if
    end do
    ! tboas: an empty slot yields no target
    if (best_pct <= 0._r8) return
    ! cft_lb = first crop PFT index = natpft_ub + 1
    covercrop_target_ivt = cft_lb + best_cft - 1
  end function covercrop_target_ivt

end module dynCovercropFileMod

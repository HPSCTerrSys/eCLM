module oas_defineMod
  use mod_oasis
  implicit none
  save
  private

  public  :: oas_definitions_init
  integer :: ierror
contains

  subroutine oas_definitions_init(bounds)
    use spmdMod      , only : masterproc
    use clm_varpar   , only : nlevsoi, nlevgrnd
    use decompMod    , only : ldecomp, bounds_type
    use oas_vardefMod

    type(bounds_type) , intent(in)  :: bounds ! start and end gridcell indices for this MPI task

    ! oasis_def_partition
    integer, allocatable :: partition(:)      ! partition descriptor; input to oasis_def_partition
    integer              :: gcell_start       ! starting gridcell index
    integer              :: gcell_previous    ! gridcell index from previous loop iteration
    integer              :: k, g              ! array/loop indices
    integer              :: grid_id           ! id returned after call to oasis_def_partition
#ifdef COUP_OAS_ICON
    integer              :: jg                ! loop counter
#endif

    ! oasis_def_var
    integer              :: var_nodims(2)     ! var dimension parameters


    if (masterproc) then
      call define_grid()
    end if


    ! -----------------------------------------------------------------
    ! ... Define partition
    ! -----------------------------------------------------------------
    allocate(partition(200))
    partition(:) = 0; k = 0

    ! Use ORANGE partitioning scheme. This scheme defines an ensemble
    ! of gridcell segments. See OASIS3-MCT User's guide for more info.
    partition(1) = 3

    ! Mark 1st segment
    gcell_start = ldecomp%gdc2glo(bounds%begg)
    partition(2) = 1
    gcell_previous = gcell_start

    ! Capture segments by detecting segment boundaries. A boundary is 
    ! detected when the current and previous gridcells are not consecutive.
    do g = bounds%begg+1, bounds%endg
      if (ldecomp%gdc2glo(g) - gcell_previous /= 1) then
        ! Previous segment complete; its partition params could now be defined
        partition(3+k) = gcell_start - 1                  ! segment global offset (0-based)
        partition(4+k) = gcell_previous - gcell_start + 1 ! segment length
        k = k + 2
  
        gcell_start  = ldecomp%gdc2glo(g) ! current gridcell marks the start of a new segment 
        partition(2) = partition(2) + 1   ! increment number of segments
      end if
      gcell_previous = ldecomp%gdc2glo(g)
    enddo

    ! Define partition params for last segment
    partition(3+k) = gcell_start - 1
    partition(4+k) = gcell_previous - gcell_start + 1

    call oasis_def_partition(grid_id, partition, ierror)
    deallocate(partition)

    ! -----------------------------------------------------------------
    ! ... Define coupling fields
    ! -----------------------------------------------------------------

#ifdef COUP_OAS_PFL
    var_nodims(1) = 1         ! unused
    var_nodims(2) = nlevsoi   ! number of fields in a bundle

    call oasis_def_var(oas_et_loss_id, "ECLM_ET", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror)

    var_nodims(2) = nlevgrnd         ! number of fields in a bundle
    call oasis_def_var(oas_sat_id, "ECLM_SOILLIQ", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror)
    call oasis_def_var(oas_psi_id, "ECLM_PSI", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror)
    call oasis_def_var(oas_ice_impedance_id, "ECLM_ICE_IMPEDANCE", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror)
#endif

#ifdef COUP_OAS_ICON

    var_nodims(1) = 1         ! unused
    var_nodims(2) = 1         ! number of fields in a bundle

    ! send to ICON
    CALL oasis_def_var(oas_id_t,  "CLMTEMPE", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) ! 1 
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMTEMPE.')
    CALL oasis_def_var(oas_id_u,  "CLMUWIND", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) ! 2
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMUWIND.')
    CALL oasis_def_var(oas_id_v,  "CLMVWIND", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) ! 3
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMVWIND.')
    CALL oasis_def_var(oas_id_qv, "CLMSPWAT", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) ! 4
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMSPWAT.')
    CALL oasis_def_var(oas_id_ht, "CLMTHICK", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) ! 5
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMTHICK.')
    CALL oasis_def_var(oas_id_pr, "CLMPRESS", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) ! 6
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMPRESS.')
    CALL oasis_def_var(oas_id_rs, "CLMDIRSW", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) ! 7
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMDIRSW.')
    CALL oasis_def_var(oas_id_fs, "CLMDIFSW", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) ! 8
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMDIFSW.')
    CALL oasis_def_var(oas_id_lw, "CLMLONGW", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) ! 9
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMLONGW.')
    CALL oasis_def_var(oas_id_cr, "CLMCVPRE", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) !10
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMCVPRE.')
    CALL oasis_def_var(oas_id_gr, "CLMGSPRE", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror) !11
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMGSPRE.')

    ! receive from ICON
    CALL oasis_def_var(oas_id_it, "CLMINFRA", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror) !12
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMINFRA.')
    CALL oasis_def_var(oas_id_ad, "CLMALBED", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror) !13
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMALBED.')
    CALL oasis_def_var(oas_id_ai, "CLMALBEI", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror) !14
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMALBEI.')
    CALL oasis_def_var(oas_id_tx, "CLMTAUX" , grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror) !15
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMTAUX.')
    CALL oasis_def_var(oas_id_ty, "CLMTAUY" , grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror) !16
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMTAUY.')
    CALL oasis_def_var(oas_id_sh, "CLMSHFLX", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror) !17
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMSHFLX.')
    CALL oasis_def_var(oas_id_lh, "CLMLHFLX", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror) !18
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMLHFLX.')
    CALL oasis_def_var(oas_id_st, "CLMTGRND", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror) !19
    IF (ierror /= 0) CALL oasis_abort(oas_comp_id, oas_comp_name, 'Failure in oasis_def_var for CLMTGRND.')

#endif

    ! End definition phase
    call oasis_enddef(ierror)
  end subroutine oas_definitions_init

  subroutine define_grid()
    use shr_kind_mod , only : r8 => shr_kind_r8
    use domainMod    , only : ldomain
    character(len=4), parameter   :: grid_name='gclm'
    integer,          parameter   :: SOUTH = 1
    integer,          parameter   :: NORTH = 2
    integer,          parameter   :: WEST  = 1
    integer,          parameter   :: EAST  = 2   
    real(kind=r8),    allocatable :: corner_lon(:,:), corner_lat(:,:)
    real(kind=r8),    allocatable :: oas_lon(:,:), oas_lat(:,:)
    real(kind=r8),    allocatable :: oas_corner_lon(:,:,:), oas_corner_lat(:,:,:)
    integer,          allocatable :: oas_mask(:,:)
    real(kind=r8)                 :: center, offset, neighbor
    integer                       :: write_grid_files
    integer                       :: i, j
    integer                       :: n_lons, n_lats, n_gridcells

    call oasis_start_grids_writing(write_grid_files)

    if (write_grid_files == 1) then
      n_lons = ldomain%ni
      n_lats = ldomain%nj
      n_gridcells = ldomain%ns

      ! -----------------------------------------------------------------
      ! ... Define centers
      ! -----------------------------------------------------------------
      allocate(oas_lon(n_gridcells, 1))
      allocate(oas_lat(n_gridcells, 1))
      do j = 1, n_lats
        i = (j-1)*n_lons + 1
        oas_lon(i:n_lons, 1) = ldomain%lonc(:)
        oas_lat(i:n_lons, 1) = ldomain%latc(j)
      enddo
      call oasis_write_grid(grid_name, n_gridcells, 1, oas_lon, oas_lat)

      ! -----------------------------------------------------------------
      ! ... Define corners
      ! -----------------------------------------------------------------
      allocate(corner_lon(n_lons, WEST:EAST))
      allocate(corner_lat(n_lats, SOUTH:NORTH))
      allocate(oas_corner_lon(n_gridcells, 1, 4))
      allocate(oas_corner_lat(n_gridcells, 1, 4))

      do j = 1, n_lats
        if (j == 1) then
          neighbor = ldomain%latc(j+1)
        else
          neighbor = ldomain%latc(j-1)
        end if
        center = ldomain%latc(j)
        offset = abs(center - neighbor) / 2.0_r8
        corner_lat(j, SOUTH:NORTH) = [center-offset, center+offset]
      enddo
    
      do i = 1, n_lons
        if (i == 1) then
          neighbor = ldomain%lonc(i+1)
        else
          neighbor = ldomain%lonc(i-1)
        end if
        center = ldomain%lonc(i)
        offset = abs(center - neighbor) / 2.0_r8
        corner_lon(i, WEST:EAST) = [center-offset, center+offset]
      enddo

      !  oas_corner indexing scheme                       
      !       4 +-----+ 3  NORTH    
      !         |     |             
      !         |     |             
      !       1 +-----+ 2  SOUTH   
      !       WEST   EAST                                    
      do j = 1, n_lats
        i = (j-1)*n_lons + 1
        oas_corner_lon(i:n_lons,1,1:2) = corner_lon(:, WEST:EAST) ! bottom side
        oas_corner_lat(i:n_lons,1,2)   = corner_lat(j, SOUTH)     ! right side
        oas_corner_lat(i:n_lons,1,3)   = corner_lat(j, NORTH)     ! right side
      enddo
    
      ! Fill missing longitudes and latitudes
      oas_corner_lon(:,1,[4,3]) = oas_corner_lon(:,1,[1,2]) ! West-East for top side
      oas_corner_lat(:,1,[1,4]) = oas_corner_lat(:,1,[2,3]) ! South-North for left side
      call oasis_write_corner(grid_name, n_gridcells, 1, 4, oas_corner_lon, oas_corner_lat)

      ! -----------------------------------------------------------------
      ! ... Define mask
      ! -----------------------------------------------------------------
      ! CLM5 landmask convention: 0 = ocean, 1 = land
      allocate(oas_mask(n_gridcells, 1))
      do j = 1, n_lats
        i = (j-1)*n_lons + 1
        oas_mask(i:n_lons,1) = ldomain%mask(:)
      enddo

      ! Invert mask to conform to OASIS convention: 0 = not masked, 1 = masked
      where (oas_mask(:,1) == 0)
        oas_mask(:,1) = 1
      else where
        oas_mask(:,1) = 0
      end where
      call oasis_write_mask(grid_name, n_gridcells, 1, oas_mask)
      call oasis_terminate_grids_writing()
      deallocate(oas_lon, oas_lat, oas_corner_lon, oas_corner_lat, oas_mask, corner_lon, corner_lat)
    end if
  end subroutine define_grid
end module oas_defineMod

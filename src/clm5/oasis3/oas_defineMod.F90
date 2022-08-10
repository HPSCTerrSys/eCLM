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
    use decompMod    , only : bounds_type, ldecomp
    use shr_log_mod  , only : s_logunit => shr_log_Unit
    use oas_vardefMod

    type(bounds_type) , intent(in)  :: bounds ! start and end gridcell indices for this MPI task

    ! oasis_def_partition
    integer, allocatable :: partition(:)      ! partition descriptor; input to oasis_def_partition
    integer              :: gcell_start       ! starting gridcell index
    integer              :: gcell_previous    ! gridcell index from previous loop iteration
    integer              :: k, g              ! array/loop indices
    integer              :: grid_id           ! id returned after call to oasis_def_partition
#if defined(COUP_OAS_ICON)
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

#if defined(COUP_OAS_PFL)
    var_nodims(1) = 1         ! unused
    var_nodims(2) = nlevsoi   ! number of fields in a bundle

    call oasis_def_var(oas_et_loss_id, "ECLM_ET", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror)
    
    var_nodims(2) = nlevgrnd  ! number of fields in a bundle
    call oasis_def_var(oas_sat_id, "ECLM_SAT", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror)
    call oasis_def_var(oas_psi_id, "ECLM_PSI", grid_id, var_nodims, OASIS_In, OASIS_Real, ierror)
#endif 

#if defined(COUP_OAS_ICON)

    var_nodims(1) = 1         ! unused
    var_nodims(2) = 1         ! number of fields in a bundle

    oas_rcv_meta(1)%clpname = "CLMTEMPE"
    oas_rcv_meta(2)%clpname = "CLMUWIND"
    oas_rcv_meta(3)%clpname = "CLMVWIND"
    oas_rcv_meta(4)%clpname = "CLMSPWAT"
    oas_rcv_meta(5)%clpname = "CLMTHICK"
    oas_rcv_meta(6)%clpname = "CLMPRESS"
    oas_rcv_meta(7)%clpname = "CLMDIRSW"
    oas_rcv_meta(8)%clpname = "CLMDIFSW"
    oas_rcv_meta(9)%clpname = "CLMLONGW"
    oas_rcv_meta(10)%clpname = "CLMCVPRE"
    oas_rcv_meta(11)%clpname = "CLMGSPRE"

    oas_snd_meta(1)%clpname = "CLMINFRA"
    oas_snd_meta(2)%clpname = "CLMALBED"
    oas_snd_meta(3)%clpname = "CLMALBEI"
    oas_snd_meta(4)%clpname = "CLMTAUX"
    oas_snd_meta(5)%clpname = "CLMTAUY"
    oas_snd_meta(6)%clpname = "CLMSHFLX"
    oas_snd_meta(7)%clpname = "CLMLHFLX"
    oas_snd_meta(8)%clpname = "CLMTGRND"

!    call oasis_def_var(oas_temp_id, "ECLM_TEMP", grid_id, var_nodims, OASIS_Out, OASIS_Real, ierror)

    DO jg = 1, SIZE(oas_rcv_meta)
      CALL oasis_def_var(oas_rcv_meta(jg)%vid, oas_rcv_meta(jg)%clpname, grid_id, &
          var_nodims, OASIS_In, OASIS_Real, ierror)
      IF (ierror /= 0) THEN
        write(s_logunit,*) 'Failure in oasis_def_var for ', oas_rcv_meta(jg)%clpname,' Errornum: ',ierror
        CALL oasis_abort(oas_comp_id, oas_comp_name, '')
      END IF
    END DO

    DO jg = 1, SIZE(oas_snd_meta)
      CALL oasis_def_var(oas_snd_meta(jg)%vid, oas_snd_meta(jg)%clpname, grid_id, &
          var_nodims, OASIS_Out, OASIS_Real, ierror)
      IF (ierror /= 0) THEN
        write(s_logunit,*) 'Failure in oasis_def_var for ', oas_snd_meta(jg)%clpname,' Errornum: ',ierror
        CALL oasis_abort(oas_comp_id, oas_comp_name, '')
      END IF
    END DO

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

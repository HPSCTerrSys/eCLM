module oas_defineMod
  use domainMod , only : ldomain
  use mod_oasis
  implicit none
  save
  private

  public  :: oas_definitions_init

  integer :: grid_id     ! id returned by oasis_def_partition
  integer :: ierror
  integer :: n_gridcells ! lats x lons
contains

  subroutine oas_definitions_init()
    use spmdMod      , only : masterproc, mpicom

    call mpi_barrier(mpicom, ierror)
    if (masterproc) then
      n_gridcells = ldomain%ns
      call define_grid()
      call define_partition()
      call define_cpl_flds()
      call oasis_enddef(ierror)
    end if
  end subroutine oas_definitions_init

  subroutine define_grid()
    use shr_kind_mod , only : r8 => shr_kind_r8

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
    integer                       :: n_lons, n_lats

    call oasis_start_grids_writing(write_grid_files)

    if (write_grid_files == 1) then
      n_lons = ldomain%ni
      n_lats = ldomain%nj

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
        if (j == 1) then
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

  subroutine define_partition()
    integer :: partition_def(4)  ! shape of arrays passed to PSMILe

    ! Compute global offsets and local extents
    partition_def(1) = 3           ! ORANGE style partition
    partition_def(2) = 1           ! partitions number
    partition_def(3) = 0           ! Global offset
    partition_def(4) = n_gridcells ! Local extent
    call oasis_def_partition(grid_id, partition_def, ierror)
  end subroutine define_partition

  subroutine define_cpl_flds()
    use oas_vardefMod
   
    integer          :: var_nodims(2) 
    integer          :: fld_shape(2)
    character(len=2) :: soil_layer         
    integer          :: i, i_100, i_110
    
    ! Disable coupling fields by default
    ssnd(1:MAX_OAS_CPL_FIELDS)%laction = .false.
    srcv(1:MAX_OAS_CPL_FIELDS)%laction = .false.

    ! ----------------------------
    ! CLM-Parflow fields (101-120)
    ! ----------------------------
    do i = 1, MAX_SOIL_LAYERS
      i_100 = 100+i
      i_110 = 110+i
      write (soil_layer, '(I2.2)') i ! soil layer index (01-10)

      ! Evapotranspiration fluxes sent to Parflow
      ssnd(i_100)%clname  = 'CLMFLX'//soil_layer
      ssnd(i_100)%laction = .true.

      ! Water saturation received from Parflow
      srcv(i_100)%ref     = 'SAT'
      srcv(i_100)%clname  = 'CLMSAT'//soil_layer
      srcv(i_100)%level   = i
      srcv(i_100)%laction = .true.

      ! Pressure head received from Parflow
      srcv(i_110)%ref     = 'PSI'      
      srcv(i_110)%clname  = 'CLMPSI'//soil_layer
      srcv(i_110)%level   = i
      srcv(i_110)%laction = .true.
    end do

    var_nodims(1) = 1               ! var_nodims(1) is not used anymore in OASIS
    var_nodims(2) = 1               ! number of fields in a bundle
    fld_shape(:)  = [1,n_gridcells] ! min & max index for each dim of the coupling field array

    ! Announce send and receive variables
    do i = 1, MAX_OAS_CPL_FIELDS
      if (ssnd(i)%laction) then 
        call oasis_def_var(ssnd(i)%nid, ssnd(i)%clname, grid_id, var_nodims, OASIS_Out, fld_shape, OASIS_Real, ierror)
      end if
      if (srcv(i)%laction) then 
        call oasis_def_var(srcv(i)%nid, srcv(i)%clname, grid_id, var_nodims, OASIS_In,  fld_shape, OASIS_Real, ierror)
      end if
    end do
  end subroutine define_cpl_flds
end module oas_defineMod
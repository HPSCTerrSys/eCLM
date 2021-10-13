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
    use clm_varpar   , only : nlevsoi
    use decompMod    , only : bounds_type
    use oas_vardefMod

    type(bounds_type) , intent(in)  :: bounds
    integer          :: partition(3)
    integer          :: grid_id       ! id returned by oasis_def_partition
    integer          :: var_nodims(2)
    integer          :: var_shape(1)  ! not used by oasis_def_var
    character(len=2) :: soil_layer         
    integer          :: i, n_grid_points

    if (masterproc) then
      call define_grid()
    end if

    ! -----------------------------------------------------------------
    ! ... Define partition
    ! -----------------------------------------------------------------
    n_grid_points = (bounds%endg - bounds%begg) + 1
    partition(1) = 1                ! Apple style partition
    partition(2) = bounds%begg - 1  ! Global offset
    partition(3) = n_grid_points    ! # of grid cells allocated to this MPI task
    call oasis_def_partition(grid_id, partition, ierror)

    ! -----------------------------------------------------------------
    ! ... Define coupling fields
    ! -----------------------------------------------------------------
    var_nodims(1) = 1               ! var_nodims(1) is not used anymore in OASIS
    var_nodims(2) = 1               ! number of fields in a bundle

    allocate(et_loss(nlevsoi))
    allocate(watsat(nlevsoi))
    allocate(psi(nlevsoi))

    do i = 1, nlevsoi
      write (soil_layer, '(I2.2)') i ! soil layer index (01-10)

      et_loss(i)%name = 'CLMFLX'//soil_layer ! Evapotranspiration fluxes sent to Parflow
      watsat(i)%name  = 'CLMSAT'//soil_layer ! Water saturation received from Parflow
      psi(i)%name     = 'CLMPSI'//soil_layer ! Pressure head received from Parflow

      call oasis_def_var(et_loss(i)%id, et_loss(i)%name, grid_id, var_nodims, OASIS_Out, var_shape, OASIS_Real, ierror) 
      call oasis_def_var(watsat(i)%id, watsat(i)%name, grid_id, var_nodims, OASIS_In, var_shape, OASIS_Real, ierror)
      call oasis_def_var(psi(i)%id, psi(i)%name, grid_id, var_nodims, OASIS_In, var_shape, OASIS_Real, ierror)
    end do

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
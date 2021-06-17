module oas_clm_define
! Based from https://github.com/HPSCTerrSys/TSMP/blob/master/bldsva/intf_oas3/clm3_5/oas3/oas_clm_define.F90
! [Work-in-progress]
    use mod_oasis
    implicit none

contains

    subroutine oas_define_grid()
        use shr_kind_mod , only : r8 => shr_kind_r8
        use pio          , only : file_desc_t
        use ncdio_pio

        character(len=4)         :: grid_name='eclm'
        integer                  :: n_lon, n_lat            ! dimensions in the 2 directions of space
        integer                  :: n_cells                 ! n_lon * n_lat
        real(r8)                 :: lon(:,:), lat(:,:)      ! longitudes and latitudes
        real(r8)                 :: mask(:,:)                ! latitudes
        type(file_desc_t)        :: ncid                    ! netcdf id
        character(len=256)       :: filepath, domain_file  ! local file name

        ! -----------------------------------------------------------------
        ! ... Define the elements, i.e. specify the corner points for each
        !     volume element. 
        !     We only need to give the 4 horizontal corners
        !     for a volume element plus the vertical position of the upper
        !     and lower face. Nevertheless the volume element has 8 corners.
        ! -----------------------------------------------------------------

        ! -----------------------------------------------------------------
        ! ... Define centers and corners 
        ! -----------------------------------------------------------------
        !  1: lower left corner. 2,: lower right corner.
        !  3: upper right corner. 4,: upper left corner.
        !  using latlon%edges :  global edges (N,E,S,W)
        call oasis_start_grids_writing(1)

        filepath = '../../domain.lnd.NRW_300x300.190619.nc'
        call getfil(filepath, domain_file, 0)
        call ncd_pio_openfile (ncid, trim(domain_file), 0)

        ! Determine dimensions
        call ncd_inqfdims(ncid, isgrid2d, n_lon, n_lat, n_cells)
        ! SUBROUTINE oasis_write_grid(cgrid, nx, ny, lon, lat)
        !    ''' Writes longitudes and latitudes for a model grid '''
        !    character(len=*),         intent (in) :: cgrid      !< grid name
        !    integer(kind=ip_intwp_p), intent (in) :: nx         !< global nx size
        !    integer(kind=ip_intwp_p), intent (in) :: ny         !< global ny size
        !    real(kind=ip_double_p),   intent (in) :: lon(:,:)   !< longitudes
        !    real(kind=ip_double_p),   intent (in) :: lat(:,:)   !< latitudes
        !    integer(kind=ip_intwp_p), intent (in),optional :: partid  !< partition id if nonglobal data
        call oasis_write_grid(grid_name, n_lon, n_lat, lon(:,1), lat(:,2))

        ! SUBROUTINE oasis_write_corner(cgrid, nx, ny, nc, clon, clat)
        !    ''' writes the longitudes and latitudes of the grid cell corners. '''
        !    character(len=*),         intent (in) :: cgrid  !< grid name
        !    integer(kind=ip_intwp_p), intent (in) :: nx     !< global nx size
        !    integer(kind=ip_intwp_p), intent (in) :: ny     !< global ny size
        !    integer(kind=ip_intwp_p), intent (in) :: nc     !< number of corners per cell
        !    real(kind=ip_double_p),   intent (in) :: clon(:,:,:) !< corner longitudes
        !    real(kind=ip_double_p),   intent (in) :: clat(:,:,:) !< corner latitudes
        !    integer(kind=ip_intwp_p), intent (in),optional :: partid  !< partition id if nonglobal data
        call oasis_write_corner(grid_name, n_lon, n_lat, 4, lon(:,1:4), lat(:,5:8))

        ! SUBROUTINE oasis_write_mask(cgrid, nx, ny, mask)
        !    ''' create a new masks file or add a land sea mask to an existing masks file '''
        !    character(len=*),         intent (in) :: cgrid       !< grid name
        !    integer(kind=ip_intwp_p), intent (in) :: nx          !< global nx size
        !    integer(kind=ip_intwp_p), intent (in) :: ny          !< global ny size
        !    integer(kind=ip_intwp_p), intent (in) :: mask(:,:)   !< mask array
        !    integer(kind=ip_intwp_p), intent (in),optional :: partid  !< partition id if nonglobal data
        call oasis_write_mask(grid_name, n_lon, n_lat, mask)

        call oasis_terminate_grids_writing()
    end subroutine

    subroutine oas_define_partition()
        ! SUBROUTINE oasis_def_partition (id_part, kparal, kinfo, ig_size)
        !    ''' define a decomposition '''
        !    INTEGER(kind=ip_intwp_p)              ,intent(out) :: id_part  !< field decomposition id
        !    INTEGER(kind=ip_intwp_p), DIMENSION(:),intent(in)  :: kparal   !< type of parallel decomposition
        !    INTEGER(kind=ip_intwp_p), optional    ,intent(out) :: kinfo    !< return code
        !    INTEGER(kind=ip_intwp_p), optional    ,intent(in)  :: ig_size  !< total size of partition
        !    character(len=*)        , optional    ,intent(in)  :: name     !< name of partition
        call oasis_def_partition(igrid, igparal, nerror)
    end subroutine oas_define_partition

    subroutine oas_define_coupling_fields()
        ! --------------------
        !      Sent fields
        ! --------------------
        ssnd(1)%clname  = 'CLM_TAUX'      !  zonal wind stress
        ssnd(2)%clname  = 'CLM_TAUY'      !  meridional wind stress
        ssnd(3)%clname  = 'CLMLATEN'      !  total latent heat flux (W/m**2)
        ssnd(4)%clname  = 'CLMSENSI'      !  total sensible heat flux (W/m**2)
        ssnd(5)%clname  = 'CLMINFRA'      ! emitted infrared (longwave) radiation (W/m**2)
        ssnd(6)%clname  = 'CLMALBED'      ! direct albedo
        ssnd(7)%clname  = 'CLMALBEI'      ! diffuse albedo
        ssnd(8)%clname  = 'CLMCO2FL'      ! net CO2 flux (now only photosynthesis rate) (umol CO2 m-2s-1)
        ssnd(9)%clname  = 'CLM_RAM1'      ! Aerodynamic resistance (s/m)   !CPS
        ssnd(10)%clname = 'CLM_RAH1'      ! Aerodynamic resistance (s/m)   !CPS
        ssnd(11)%clname = 'CLM_RAW1'      ! Aerodynamic resistance (s/m)   !CPS
        ssnd(12)%clname = 'CLM_TSF1'      ! Surface Temperature (K)   !CPS
        ssnd(13)%clname = 'CLM_QSF1'      ! Surface Humidity (kg/kg)   !CPS
        ssnd(14)%clname = 'CLMPHOTO'      ! photosynthesis rate (umol CO2 m-2s-1)
        ssnd(15)%clname = 'CLMPLRES'      ! plant respiration (umol CO2 m-2s-1)
  
        ! CLM -> PFL
        ssnd(101)%clname = 'CLMFLX01'    !  evapotranspiration fluxes sent to PFL for each soil layer  
        ssnd(102)%clname = 'CLMFLX02'
        ssnd(103)%clname = 'CLMFLX03'
        ssnd(104)%clname = 'CLMFLX04'
        ssnd(105)%clname = 'CLMFLX05'
        ssnd(106)%clname = 'CLMFLX06'
        ssnd(107)%clname = 'CLMFLX07'
        ssnd(108)%clname = 'CLMFLX08'
        ssnd(109)%clname = 'CLMFLX09'
        ssnd(110)%clname = 'CLMFLX10'
        
        ! --------------------
        !   Received fields
        ! --------------------
        srcv(1)%clname  = 'CLMTEMPE'
        srcv(2)%clname  = 'CLMUWIND'
        srcv(3)%clname  = 'CLMVWIND'
        srcv(4)%clname  = 'CLMSPWAT'   ! specific water vapor content
        srcv(5)%clname  = 'CLMTHICK'   ! thickness of lowest level (m)
        srcv(6)%clname  = 'CLMPRESS'   ! surface pressure (Pa)
        srcv(7)%clname  = 'CLMDIRSW'   ! direct shortwave downward radiation (W/m2)
        srcv(8)%clname  = 'CLMDIFSW'   ! diffuse shortwave downward radiation (W/m2)
        srcv(9)%clname  = 'CLMLONGW'   ! longwave downward radiation (W/m2)
        srcv(10)%clname = 'CLMCVRAI'  ! convective rain precipitation      (kg/m2*s)
        srcv(11)%clname = 'CLMCVSNW'  ! convective snow precipitation      (kg/m2*s)
        srcv(12)%clname = 'CLMGSRAI'  ! gridscale rain precipitation
        srcv(13)%clname = 'CLMGSSNW'  ! gridscale snow precipitation
        srcv(14)%clname = 'CLMGRAUP'  ! gridscale graupel precipitation
        srcv(15)%clname = 'CLMCVPRE'  ! total convective precipitation
        srcv(16)%clname = 'CLMGSPRE'  ! total gridscale precipitation
        srcv(17)%clname = 'CLMCO2PP'  ! CO2 partial pressure (Pa)  !CMU
      
        ! PFL -> CLM
        srcv(101)%clname = 'CLMSAT01' ! water saturation received from PFL for each soil layer
        srcv(102)%clname = 'CLMSAT02'
        srcv(103)%clname = 'CLMSAT03'
        srcv(104)%clname = 'CLMSAT04'   
        srcv(105)%clname = 'CLMSAT05'  
        srcv(106)%clname = 'CLMSAT06'
        srcv(107)%clname = 'CLMSAT07' 
        srcv(108)%clname = 'CLMSAT08'  
        srcv(109)%clname = 'CLMSAT09'   
        srcv(110)%clname = 'CLMSAT10'  
      
        srcv(101)%level= 1 ! # of soil layer
        srcv(102)%level= 2
        srcv(103)%level= 3
        srcv(104)%level= 4   
        srcv(105)%level= 5  
        srcv(106)%level= 6
        srcv(107)%level= 7 
        srcv(108)%level= 8  
        srcv(109)%level= 9   
        srcv(110)%level= 10  
      
        srcv(101:110)%ref='SAT'  
      
        srcv(111)%clname = 'CLMPSI01' ! pressure head received from PFL for each soil layer
        srcv(112)%clname = 'CLMPSI02'
        srcv(113)%clname = 'CLMPSI03'
        srcv(114)%clname = 'CLMPSI04'   
        srcv(115)%clname = 'CLMPSI05'  
        srcv(116)%clname = 'CLMPSI06'
        srcv(117)%clname = 'CLMPSI07' 
        srcv(118)%clname = 'CLMPSI08'  
        srcv(119)%clname = 'CLMPSI09'   
        srcv(120)%clname = 'CLMPSI10'  
        
        srcv(111)%level= 1 ! # of soil layer
        srcv(112)%level= 2
        srcv(113)%level= 3
        srcv(114)%level= 4   
        srcv(115)%level= 5  
        srcv(116)%level= 6
        srcv(117)%level= 7 
        srcv(118)%level= 8  
        srcv(119)%level= 9   
        srcv(120)%level= 10  
      
        srcv(111:120)%ref='PSI'


        !SUBROUTINE oasis_def_var(id_nports, cdport, id_part, id_var_nodims, kinout, id_var_shape, ktype, kinfo)
        !    INTEGER(kind=ip_i4_p),intent(out) :: id_nports    !< coupling field ID
        !    CHARACTER(len=*)     ,intent(in)  :: cdport       !< field name as in namcouple
        !    INTEGER(kind=ip_i4_p),intent(in)  :: id_part      !< partition ID
        !    INTEGER(kind=ip_i4_p),intent(in)  :: id_var_nodims(2)  !< rank and number of bundles
        !    INTEGER(kind=ip_i4_p),intent(in)  :: kinout       !< input or output flag
        !    INTEGER(kind=ip_i4_p),intent(in)  :: id_var_shape(2*id_var_nodims(1)) !< size of field
        !    INTEGER(kind=ip_i4_p),intent(in)  :: ktype        !< type of coupling field
        !    INTEGER(kind=ip_i4_p),intent(out),optional :: kinfo    !< return code
        ! Announce send variables
        call oasis_def_var(ssnd(ji)%nid, ssnd(ji)%clname, igrid, var_nodims, OASIS_Out, ipshape, OASIS_Real, nerror)
        ! Announce received variables
        call oasis_def_var(srcv(ji)%nid, srcv(ji)%clname, igrid, var_nodims, OASIS_In, ipshape, OASIS_Real, nerror)

    end subroutine oas_define_coupling_fields

end module oas_clm_define


program test_oas_clm_define
    use mod_oasis
    use oas_clm_define
    
    integer :: oas_comp_id, ierr

    call oasis_init_comp(oas_comp_id, 'eclm', ierr)

    call oas_define_grid()
    call oas_define_coupling_fields()
    call oas_define_partition()

    call oasis_terminate(ierr)

end program test_oas_clm_define
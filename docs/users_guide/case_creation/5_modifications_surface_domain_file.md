# Modification of the surface and domain file

The created surface and domain file have negative longitudes that eCLM/CLM5 does not accept and inherently has no landmask. To modify the longitudes (into a 360 degree system) and to add a landmask, you can use the `mod_domain.sh` script in the main folder `eCLM_static_file_workflow`.

Before executing the script adapt the paths to your surface file (created in step 4), domain file (created in step 3) and landmask file (the land mask is already on the files if you used the mkscripgrid.ncl script to create the SCRIP grid file, if you started from a netCDF file you will have to provide a file that contains your landmask (value 1 for land and 0 for ocean)).
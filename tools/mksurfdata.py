#!/usr/bin/env python3

CSMDATA = "/glade/p/cesm/cseg/inputdata"

opts = {}
opts["hgrid"] = "all"
opts["vic"] = 0
opts["glc"] = 0
opts["ssp_rcp"] = "hist" 
opts["debug"] = 0
opts["exedir"] = "undef"
opts["allownofile"] = "undef"
opts["crop"] = 1
opts["fast_maps"] = 0
opts["hirespft"] = "undef"
opts["years"] = "1850,2000"
opts["glc_nec"] = 10
opts["merge_gis"] = "undef"
opts["inlandwet"] = "undef"
opts["help"] = 0
opts["no_surfdata"] = 0
opts["pft_override"] = "undef"
opts["pft_frc"] = "undef"
opts["pft_idx"] = "undef"
opts["soil_override"] = "undef"
opts["soil_cly"] = "undef"
opts["soil_snd"] = "undef"
opts["soil_col"] = "undef"
opts["soil_fmx"] = "undef"
opts["outnc_double"] = "undef"
opts["outnc_dims"] = "2"     
opts["usrname"] = ""
opts["rundir"] = "$cwd"
opts["usr_mapdir"] = "../mkmapdata"
opts["dynpft"] = "undef"
opts["csmdata"] = CSMDATA
opts["urban_skip_abort_on_invalid_data_check"] = "undef"

numpft = 78;

def usage():
   print("""
SYNOPSIS 

     For supported resolutions:
     $ProgName -res <res>  [OPTIONS]
        -res [or -r] "resolution" is the supported resolution(s) to use for files (by default $opts{'hgrid'} ).

      
     For unsupported, user-specified resolutions:	
     $ProgName -res usrspec -usr_gname <user_gname> -usr_gdate <user_gdate>  [OPTIONS]
        -usr_gname "user_gname"    User resolution name to find grid file with 
                                   (only used if -res is set to 'usrspec')
        -usr_gdate "user_gdate"    User map date to find mapping files with
                                   (only used if -res is set to 'usrspec')
                                   NOTE: all mapping files are assumed to be in mkmapdata
                                    - and the user needs to have invoked mkmapdata in 
                                      that directory first
        -usr_mapdir "mapdirectory" Directory where the user-supplied mapping files are
                                   Default: $opts{'usr_mapdir'}

OPTIONS
     NOTE: The three critical options are (-years, -glc_nec, and -ssp_rcp) they are marked as such.

     -allownofile                  Allow the script to run even if one of the input files
                                   does NOT exist.
     -dinlc [or -l]                Enter the directory location for inputdata 
                                   (default $opts{'csmdata'})
     -debug [or -d]                Do not actually run -- just print out what 
                                   would happen if ran.
     -dynpft "filename"            Dynamic PFT/harvesting file to use if you have a manual list you want to use
                                   (rather than create it on the fly, must be consistent with first year)
                                   (Normally NOT used)
     -fast_maps                    Toggle fast mode which doesn't use the large mapping files
     -glc_nec "number"             Number of glacier elevation classes to use (by default $opts{'glc_nec'})
                                   (CRITICAL OPTION)
     -merge_gis                    If you want to use the glacier dataset that merges in
                                   the Greenland Ice Sheet data that CISM uses (typically
                                   used only if consistency with CISM is important)
     -hirespft                     If you want to use the high-resolution pft dataset rather 
                                   than the default lower resolution dataset
                                   (low resolution is at half-degree, high resolution at 3minute)
                                   (hires only available for present-day [2000])
     -exedir "directory"           Directory where mksurfdata_map program is
                                   (by default assume it is in the current directory)
     -inlandwet                    If you want to allow inland wetlands
     -no-crop                      Create datasets without the extensive list of prognostic crop types
     -no_surfdata                  Do not output a surface dataset
                                   This is useful if you only want a landuse_timeseries file
     -years [or -y] "years"        Simulation year(s) to run over (by default $opts{'years'}) 
                                   (can also be a simulation year range: i.e. 1850-2000 or 1850-2100 for ssp_rcp future scenarios)
                                   (CRITICAL OPTION)
     -help  [or -h]                Display this help.

     -rundir "directory"           Directory to run in
                                   (by default current directory $opts{'rundir'})

     -ssp_rcp "scenario-name"      Shared Socioeconomic Pathway and Representative Concentration Pathway Scenario name(s).
                                   "hist" for historical, otherwise in form of SSPn-m.m where n is the SSP number
                                   and m.m is the radiative forcing in W/m^2 at the peak or 2100.
                                   (normally use thiw with -years 1850-2100)
                                   (CRITICAL OPTION)
     
     -usrname "clm_usrdat_name"    CLM user data name to find grid file with.

     -vic                          Add the fields required for the VIC model
     -glc                          Add the optional 3D glacier fields for verification of the glacier model

      NOTE: years, res, and ssp_rcp can be comma delimited lists.


OPTIONS to override the mapping of the input gridded data with hardcoded input

     -pft_frc "list of fractions"  Comma delimited list of percentages for veg types
     -pft_idx "list of veg index"  Comma delimited veg index for each fraction
     -soil_cly "% of clay"         % of soil that is clay
     -soil_col "soil color"        Soil color (1 [light] to 20 [dark])
     -soil_fmx "soil fmax"         Soil maximum saturated fraction (0-1)
     -soil_snd "% of sand"         % of soil that is sand

OPTIONS to work around bugs?
     -urban_skip_abort_on_invalid_data_check
                                   do not abort on an invalid data check in urban.
                                   Added 2015-01 to avoid recompiling as noted in
                                   /glade/p/cesm/cseg/inputdata/lnd/clm2/surfdata_map/README_c141219
   """)

def check_soil():
    """
    check that the soil options are set correctly
    """
    # TODO
    pass

def check_soil_col_fmx():
    """
    check that the soil color or soil fmax option is set correctly
    """
    # TODO
    pass

def check_pft():
    """
    check that the pft options are set correctly
    """
    # TODO
    pass

def write_transient_timeseries_file():
    """
    """
    # TODO
    pass

def write_namelist_file():
    """
    """
    # TODO
    pass

if __name__ == "__main__":
    # TODO
   print("Work in progress...")

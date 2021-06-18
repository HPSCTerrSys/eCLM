#!/usr/bin/env python3

import os, subprocess
from datetime import datetime

CSMDATA = "$CESMDATAROOT/inputdata"
scrdir = ""
debug = 0

opts = {}
opts["hgrid"] = "usrspec"
opts["vic"] = 0
opts["glc"] = 0
opts["ssp_rcp"] = "hist" 
opts["debug"] = 0
opts["exedir"] = None
opts["allownofile"] = None
opts["crop"] = 1
opts["fast_maps"] = 0
opts["hirespft"] = None
opts["years"] = "2000"
opts["glc_nec"] = 10
opts["merge_gis"] = None
opts["inlandwet"] = None
opts["help"] = 0
opts["no_surfdata"] = 0
opts["pft_override"] = None
opts["pft_frc"] = None
opts["pft_idx"] = None
opts["soil_override"] = None
opts["soil_cly"] = None
opts["soil_snd"] = None
opts["soil_col"] = None
opts["soil_fmx"] = None
opts["outnc_double"] = None
opts["outnc_dims"] = "2"     
opts["usrname"] = ""
opts["rundir"] = os.getcwd()
opts["usr_gname"] = "Nigeria"
opts["usr_gdate"] = "200503"
opts["usr_mapdir"] = CSMDATA + "/lnd/clm2/mappingdata/maps/Nigeria"
opts["dynpft"] = None
opts["csmdata"] = CSMDATA
opts["urban_skip_abort_on_invalid_data_check"] = None

numpft = 78

def usage():
   print("""
SYNOPSIS 

     For supported resolutions:
     ProgName -res <res>  [OPTIONS]
        -res [or -r] "resolution" is the supported resolution(s) to use for files (by default opts["hgrid"] ).

      
     For unsupported, user-specified resolutions:	
     ProgName -res usrspec -usr_gname <user_gname> -usr_gdate <user_gdate>  [OPTIONS]
        -usr_gname "user_gname"    User resolution name to find grid file with 
                                   (only used if -res is set to 'usrspec')
        -usr_gdate "user_gdate"    User map date to find mapping files with
                                   (only used if -res is set to 'usrspec')
                                   NOTE: all mapping files are assumed to be in mkmapdata
                                    - and the user needs to have invoked mkmapdata in 
                                      that directory first
        -usr_mapdir "mapdirectory" Directory where the user-supplied mapping files are
                                   Default: opts["usr_mapdir"]

OPTIONS
     NOTE: The three critical options are (-years, -glc_nec, and -ssp_rcp) they are marked as such.

     -allownofile                  Allow the script to run even if one of the input files
                                   does NOT exist.
     -dinlc [or -l]                Enter the directory location for inputdata 
                                   (default opts["csmdata"])
     -debug [or -d]                Do not actually run -- just print out what 
                                   would happen if ran.
     -dynpft "filename"            Dynamic PFT/harvesting file to use if you have a manual list you want to use
                                   (rather than create it on the fly, must be consistent with first year)
                                   (Normally NOT used)
     -fast_maps                    Toggle fast mode which doesn't use the large mapping files
     -glc_nec "number"             Number of glacier elevation classes to use (by default opts["glc_nec"])
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
     -years [or -y] "years"        Simulation year(s) to run over (by default opts["years"]) 
                                   (can also be a simulation year range: i.e. 1850-2000 or 1850-2100 for ssp_rcp future scenarios)
                                   (CRITICAL OPTION)
     -help  [or -h]                Display this help.

     -rundir "directory"           Directory to run in
                                   (by default current directory opts["rundir"])

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

class NamelistDefinition(object):
   """
   Stub class. Actual implementation should be ported from clm5.0/cime/utils/perl5lib/Build/NamelistDefinition.pm
   """
   def __init__(self, nl_file):
        pass

   def is_valid_value(self, var_name, value):
      return True

   def get_valid_values(self, var_name):
      return None

def check_soil():
    """
    check that the soil options are set correctly
    """
    for my_type in ["soil_cly", "soil_snd"]:
      if not my_type in opts:
         raise KeyError("ERROR: Soil variables were set, but $type was NOT set")

    texsum = opts["soil_cly"] + opts["soil_snd"]
    loam   = 100.0 - texsum
    if ( texsum < 0.0 or texsum > 100.0 ):
      raise ValueError(f'ERROR: Soil textures are out of range: clay = {opts["soil_cly"]} sand = {opts["soil_snd"]} loam = {loam}')

def check_soil_col_fmx():
    """
    check that the soil color or soil fmax option is set correctly
    """
    if "soil_col" in opts:
      if opts["soil_col"] < 0 or opts["soil_col"] > 20:
         raise ValueError(f'ERROR: Soil color is out of range = {opts["soil_col"]}')

    if "soil_fmx" in opts:
      if opts["soil_fmx"] < 0 or opts["soil_fmx"] > 1.0:
         raise ValueError(f'ERROR: Soil fmax is out of range = = {opts["soil_fmx"]}')

def check_pft():
    """
    check that the pft options are set correctly
    """
    # TODO
    # Eliminate starting and ending square brackets
    # $opts{'pft_idx'} =~ s/^\[//;
    # $opts{'pft_idx'} =~ s/\]$//;
    # $opts{'pft_frc'} =~ s/^\[//;
    # $opts{'pft_frc'} =~ s/\]$//;

    for mytype in ["pft_idx", "pft_frc"]:
       if not mytype in opts:
          raise ValueError(f"ERROR: PFT variables were set, but {mytype} was NOT set")

    pft_idx = [int(idx) for idx in opts["pft_idx"].split(",")]
    pft_frc = [int(frc) for frc in opts["pft_frc"].split(",")]

    if len(pft_idx) != len(pft_frc):
       raise IndexError("ERROR: PFT arrays are different sizes: pft_idx and pft_frc")

    sumfrc = 0.0

    for i in range(0, len(pft_idx)):
       if int(pft_idx[i]) < 0 or pft_idx[i] > numpft:
          # check index in range
          raise IndexError(f'ERROR: pft_idx out of range = {opts["pft_idx"]}')

       # make sure there are no duplicates
       for j in range(0, i):
          if pft_idx[i] == pft_idx[j]:
             raise IndexError(f'ERROR: pft_idx has duplicates = {opts["pft_idx"]}')

       # check fraction in range
       if pft_frc[i] < 0.0 or pft_frc[i] > 100.0:
          raise OverflowError(f'ERROR: pft_frc out of range (>0.0 and <=100.0) = {opts["pft_frc"]}')

       sumfrc = sumfrc + pft_frc[i]

    # check that fraction sums up to 100%
    if abs(sumfrc - 100.0) > 1e-6:
       # TODO
       #raise ArithmeticError(f'ERROR: pft_frc does NOT add up to 100% = {opts["pft_frc"]}')
       pass

def write_transient_timeseries_file(transient, desc, sim_yr0, sim_yrn, queryfilopts, resol, 
                                    resolhrv, ssp_rcp, mkcrop, sim_yr_surfdat):
    """
    """
    strlen = 195
    dynpft_format = "{0:<{1}} {2:04d}"
    landuse_timeseries_text_file = ""
    if transient:
       if (opts["dynpft"] is None and not opts["pft_override"]):
         landuse_timeseries_text_file = f"landuse_timeseries_{desc}.txt"
         queryDefaultNamelist = "/home/p.rigor/Codes/00_CLM/GH_CLM5.0/bld/queryDefaultNamelist.pl"
         with open(landuse_timeseries_text_file, "w") as fh_landuse_timeseries:
            print(f"Writing out landuse_timeseries text file: {landuse_timeseries_text_file}")
            for yr in range(sim_yr0, sim_yrn + 1):
               vegtypyr = subprocess.run([queryDefaultNamelist, queryfilopts, resol, "-options", f"sim_year={yr},ssp_rcp={ssp_rcp}{mkcrop}", "-var", "mksrf_fvegtyp", "-namelist", "clmexp"], capture_output=True, text=True).stdout
               vegtypyr.rstrip('\n')
               fh_landuse_timeseries.write(dynpft_format.format(vegtypyr, strlen, yr))
               hrvtypyr = subprocess.run([queryDefaultNamelist, queryfilopts, resolhrv, "-options", f"sim_year={yr},ssp_rcp={ssp_rcp}{mkcrop}", "-var", "mksrf_fvegtyp", "-namelist", "clmexp"], capture_output=True, text=True).stdout
               hrvtypyr.rstrip('\n')
               fh_landuse_timeseries.write(dynpft_format.format(hrvtypyr, strlen, yr))
               if (yr % 100 == 0):
                  print("year:", yr)
         print("Done writing file")
       elif opts["pft_override"] and "dynpft" in opts:
         landuse_timeseries_text_file = opts["dynpft"]
       else:
         landuse_timeseries_text_file = f"landuse_timeseries_override_{desc}.txt"
         with open(landuse_timeseries_text_file, "w") as fh_landuse_timeseries:
            frstpft = (f'<pft_f>{opts["pft_frc"]}</pft_f>' +
                        f'<pft_i>{opts["pft_frc"]}</pft_i>' +
                        '<harv>0,0,0,0,0</harv><graz>0</graz>')
            print(f"Writing out landuse_timeseries text file: {landuse_timeseries_text_file}")
            l = len(frstpft)
            if (l > strlen):
               raise ValueError(f"ERROR PFT line is too long ({l}): {frstpft}")
            fh_landuse_timeseries.write(dynpft_format.format(frstpft, strlen, sim_yr_surfdat))
            print("Done writing file")
    return landuse_timeseries_text_file

def write_namelist_file(namelist_fname, logfile_fname, fsurdat_fname, fdyndat_fname,
                        glc_nec, griddata, map, datfil, double,
                        all_urb, no_inlandwet, vegtyp, hrvtyp, 
                        landuse_timeseries_text_file, setnumpft):
    """
    """
   # TODO: Read `git describe` output from scrdir=clm5.0/tools/mksurfdata_map
   #  orig_cwd = os.getcwd()
   #  os.chdir(scrdir)
   #  gitdescribe = subprocess.run(["git", "describe"], capture_output=True, text=True).stdout
   #  os.chdir(orig_cwd)
    gitdescribe = "release-clm5.0.34-24-gdc5ea974 ../CESMDATAROOT/inputdata/lnd/clm2/surfdata_map"

    with open(namelist_fname, "w") as fh:
       fh.write(f"""&clmexp
 nglcec           = $glc_nec
 mksrf_fgrid      = {griddata}
 map_fpft         = {map['veg']}
 map_fglacier     = {map['glc']}
 map_fglacierregion = {map['glcregion']}
 map_fsoicol      = {map['col']}
 map_furban       = {map['urb']}
 map_fmax         = {map['fmx']}
 map_forganic     = {map['org']}
 map_flai         = {map['lai']}
 map_fharvest     = {map['hrv']}
 map_flakwat      = {map['lak']}
 map_fwetlnd      = {map['wet']}
 map_fvocef       = {map['voc']}
 map_fsoitex      = {map['tex']}
 map_furbtopo     = {map['utp']}
 map_fgdp         = {map['gdp']}
 map_fpeat        = {map['peat']}
 map_fsoildepth   = {map['soildepth']}
 map_fabm         = {map['abm']}
 mksrf_fsoitex    = {datfil['tex']}
 mksrf_forganic   = {datfil['org']}
 mksrf_flakwat    = {datfil['lak']}
 mksrf_fwetlnd    = {datfil['wet']}
 mksrf_fmax       = {datfil['fmx']}
 mksrf_fglacier   = {datfil['glc']}
 mksrf_fglacierregion = {datfil['glcregion']}
 mksrf_fvocef     = {datfil['voc']}
 mksrf_furbtopo   = {datfil['utp']}
 mksrf_fgdp       = {datfil['gdp']}
 mksrf_fpeat      = {datfil['peat']}
 mksrf_fsoildepth = {datfil['soildepth']}
 mksrf_fabm       = {datfil['abm']}
 outnc_double   = {double}
 all_urban      = {all_urb}
 no_inlandwet   = {no_inlandwet}
 mksrf_furban   = {datfil['urb']}
 gitdescribe    = {gitdescribe}""")

       if opts["vic"]:
          fh.write(f' map_fvic         = {map["vic"]}')
          fh.write(f' mksrf_fvic       = {datfil["vic"]}')
          fh.write(f' outnc_vic = .true.')

       if opts["glc"]:
          fh.write(" outnc_3dglc = .true.")

       if opts["fast_maps"]:
          fh.write(f' map_ftopostats   = {map["topostats"]}')
          fh.write(f' mksrf_ftopostats   = {datfil["topostats"]}')
       else:
          fh.write(" std_elev         = 371.0d00")

       if opts["soil_override"]:
          fh.write(f' soil_clay     = {opts["soil_clay"]}')
          fh.write(f' soil_sand     = {opts["soil_snd"]}')

       if opts["pft_override"]:
          fh.write(f' all_veg      = .true.')
          fh.write(f' pft_frc      = {opts["pft_frc"]}')
          fh.write(f' pft_idx      = {opts["pft_idx"]}')

       fh.write(f"""
 mksrf_fvegtyp  = {vegtyp}
 mksrf_fhrvtyp  = {hrvtyp}
 mksrf_fsoicol  = {datfil['col']}
 mksrf_flai     = {datfil['lai']}
 fsurdat        = {fsurdat_fname}
 fsurlog        = {logfile_fname}
 mksrf_fdynuse  = {landuse_timeseries_text_file}
 fdyndat        = {fdyndat_fname}""")

       if setnumpft:
          fh.write(setnumpft)

       if opts["urban_skip_abort_on_invalid_data_check"]:
          fh.write(f' urban_skip_abort_on_invalid_data_check = .true.')

    with open(namelist_fname, "r") as fh:
       print(fh.readlines())

def main():
   clm5 = "" # set full path to CLM5
   nldef_file = f"{clm5}/bld/namelist_files/namelist_definition_clm4_5.xml"
   definition = NamelistDefinition(nldef_file)

   try:
      os.chdir( opts["rundir"] ) 
   except:
      raise SystemError(f'** cant change to directory: {opts["rundir"]}')
   # If csmdata was changed from the default
   #if (CSMDATA != opts["csmdata"]):
   CSMDATA = opts["csmdata"]
   glc_nec = opts["glc_nec"]
   if (glc_nec <= 0):
      print("** glc_nec must be at least 1")
      usage()
   no_inlandwet = True
   if "inlandwet" in opts:
      no_inlandwet = False
   #
   # Set disk location to send files to, and list resolutions to operate over, 
   # set filenames, and short-date-name
   #
   hresols = []
   mapdate = ""
   if (opts["hgrid"] == "all"):
      all_hresols = definition.get_valid_values( "res" )
      hresols = all_hresols
   elif (opts["hgrid"] == "usrspec"):
      hresols = opts["usr_gname"] 
      mapdate = opts["usr_gdate"] 
   else:
      hresols = opts["hgrid"].split(",")
      # Check that resolutions are valid
      for res in hresols:
         if (not definition.is_valid_value( "res", res )):
            if (opts["usrname"] == ""  or res != opts["usrname"]):
               print(f"** Invalid resolution: {res}")
               usage()
   #
   # Set years to run over
   #
   years = opts["years"].split(",")
   # Check that resolutions are valid
   for sim_year in years:
     if "-" in sim_year:
       # range of years for transient run
       if (not definition.is_valid_value( "sim_year_range", sim_year )):
         print(f"** Invalid simulation simulation year range: {sim_year}")
         usage()
       else:
       # single year.
         if (not definition.is_valid_value( "sim_year", sim_year )):
            print("** Invalid simulation year: sim_year")
            usage()
   #
   # Set ssp_rcp to use
   #
   rcpaths = opts["ssp_rcp"].split(",")
   # Check that ssp_rcp is valid
   for ssp_rcp in rcpaths:
      if (not definition.is_valid_value( "ssp_rcp", ssp_rcp )):
          print("** Invalid ssp_rcp: ssp_rcp")
          usage()

   # CMIP series input data is corresponding to
   cmip_series = "CMIP6"
   # Check if soil set
   if (opts["soil_cly"] is not None and opts["soil_snd"] is not None):
       check_soil()
       opts["soil_override"] = 1

   # Check if pft set
   if (not opts["crop"]): numpft = 16   # First set numpft if crop is off
   if (opts["pft_frc"] is not None and opts["pft_idx"] is not None):
       check_pft( )
       opts["pft_override"] = 1

   # Check if dynpft set and is valid filename
   if opts["dynpft"] is not None:
       if not os.path.isfile(opts["dynpft"]):
          print(f'** Dynamic PFT file does NOT exist: {opts["dynpft"]}')
          usage()

   sdate = "c{}".format(datetime.now().strftime("%Y%m%d"))
   sdate.rstrip('\n')

   cfile = "clm.input_data_list"
   if os.path.isfile(cfile):
      subprocess.run(["mv", "-f", cfile, cfile + ".previous"])

   subprocess.run(["rm", "-f", cfile])
   subprocess.run(["touch", cfile])
   with open(cfile, "w") as cfh:
      cfh.write(f"""#!/bin/csh -f
      set CSMDATA = {CSMDATA}
      """)
   subprocess.run(["chmod", "+x", cfile])

   surfdir = "lnd/clm2/surfdata"

   # string to add to options for crop off or on
   mkcrop_off = ",crop=on"
   mkcrop_on  = ",crop=on"

   #
   # Loop over all resolutions and sim-years listed
   #
   numpft = 78
   for res in hresols:
      #
      # Query the XML default file database to get the appropriate files
      #
      if (opts["hgrid"] == "usrspec"):
	      queryopts = f"-csmdata {CSMDATA} -silent -justvalue"
      else:
	      queryopts = f"-res {res} -csmdata {CSMDATA} -silent -justvalue"
      queryfilopts = f"{queryopts} -onlyfiles -phys clm4_5 "
      mkcrop = mkcrop_off
      setnumpft = ""
      mkcrop    = mkcrop_on
      setnumpft = f"numpft = {numpft}"
      usrnam    = ""
      if (opts["usrname"] != "" and res == opts["usrname"]):
         usrnam    = "-usrname " + opts["usrname"]
      #
      # Mapping files
      #
      map, hgrd, lmsk, datfil, filnm = {}, {}, {}, {}, {}
      hirespft = "off"
      if opts["hirespft"]:
         hirespft = "on"
      merge_gis = "off"
      if opts["merge_gis"]:
         merge_gis = "on"

      mopts  = f"{queryopts} -namelist default_settings {usrnam}"
      mkopts = f"-csmdata {CSMDATA} -silent -justvalue -namelist clmexp {usrnam}"
      typlist = ["lak", "veg", "voc", "tex", "col", "hrv",
                 "fmx", "lai", "urb", "org", "glc", "glcregion", "utp", "wet",
		           "gdp", "peat","soildepth","abm"]
      if (opts["vic"]):
         typlist.append("vic")
      if (not opts["fast_maps"]):
         typlist.append("topostats")

      queryDefaultNamelist = f"{clm5}/bld/queryDefaultNamelist.pl"
      args = [queryDefaultNamelist] + mopts.split()
      for typ in typlist:
         lmask_query = subprocess.run(args + ["-options", f"type={typ},mergeGIS={merge_gis},hirespft={hirespft}", "-var", "lmask"], capture_output=True, text=True).stdout.strip()
         hgrid_query = subprocess.run(args + ["-options", f"type={typ},hirespft={hirespft}", "-var", "hgrid"], capture_output=True, text=True).stdout.strip()
         if debug:
           print("query to determine hgrid:\n    hgrid_cmd \n\n")

         filnm_query = subprocess.run(args + ["-options", f"type={typ}", "-var", "mksrf_filename"], capture_output=True, text=True).stdout.strip()
         filnm[typ] = filnm_query
         hgrd[typ] = hgrid_query
         lmsk[typ]  = lmask_query

         if (opts["hgrid"] == "usrspec"):
            map[typ] = opts["usr_mapdir"] + f"/map_{hgrid_query}_{lmask_query}_to_{res}_nomask_aave_da_c{mapdate}\.nc"
         else:
            map[typ] = subprocess.run([queryDefaultNamelist] + queryfilopts.split() + ["-namelist", "clmexp", "-options", f"frm_hgrid={hgrid},frm_lmask={lmask},to_hgrid={res},to_lmask=nomask", "-var", "map"], capture_output=True, text=True).stdout.strip()
	     
         if (map[typ] == ""):
            raise FileNotFoundError("ERROR: could NOT find a mapping file for this resolution: res and type: typ at hgrid and lmask.")
         
         if (not "allownofile" in opts) and not os.path.isfile(map[typ]):
            raise FileNotFoundError(f'ERROR: mapping file for this resolution does NOT exist ({map[typ]}).')
      #
      # Grid file from the pft map file or grid if not found
      #
      griddata    = map["veg"].strip()
      if (griddata == ""):
         griddata = subprocess.run([queryDefaultNamelist] + queryfilopts.split() + [usrnam, "-var", "fatmgrid"], capture_output=True, text=True).stdout
         if (griddata == ""):
            raise FileNotFoundError(f"ERROR: could NOT find a grid data file for this resolution: {res}.")

      desc = ""
      desc_surfdat = ""
      #
      # Check if all urban single point dataset
      #
      urb_datasets = ["1x1_camdenNJ","1x1_vancouverCAN", "1x1_mexicocityMEX", "1x1_urbanc_alpha"]
      all_urb = False
      urb_pt  = 0
      for urb_res in urb_datasets:
         if res == urb_res:
            all_urb = True
            if (res != "1x1_camdenNJ"): urb_pt  = 1 
      #
      # Always run at double precision for output
      #
      double = True
      #
      # Loop over each SSP-RCP scenario
      #
      for ssp_rcp in rcpaths:
      #
      # Loop over each sim_year
      #
         for sim_year in years:
            #
            # Skip if urban unless sim_year=2000
            #
            if (urb_pt and sim_year != '2000'):
               print("For urban -- skip this simulation year = sim_year")
               continue

            #
            # If year is 1850-2000 actually run 1850-2015
            #
            if (sim_year == "1850-2000"):
               actual = "1850-2015"
               print(f"For {sim_year} actually run {actual}")
               sim_year = actual

            urbdesc = "urb3den"
            resol    = "-res " + hgrd["veg"]
            resolhrv = "-res " + hgrd["hrv"]
            sim_yr0 = sim_year
            sim_yrn = sim_year
            transient = 0
            sim_year_arr = sim_year.split("-")
            if len(sim_year_arr) >= 2:
               sim_yr0 = sim_year_arr[0]
               sim_yrn = sim_year_arr[1]
               transient = 1

            #
            # Find the file for each of the types
            #
            for typ in typlist:
               typ_cmd = [queryDefaultNamelist] + mkopts.split() + ["-options", f"hgrid={hgrd[typ]},lmask={lmsk[typ]},mergeGIS={merge_gis}{mkcrop},sim_year={sim_yr0}", "-var", filnm[typ]]
               datfil[typ] = subprocess.run(typ_cmd, capture_output=True, text=True).stdout.strip()
               if (datfil[typ] == ""):
                  raise FileNotFoundError(f"ERROR: could NOT find a {filnm[typ]} data file for this resolution: {hgrd[typ]} and type: {typ} and {lmsk[typ]}.\n{typ_cmd}\n")
   
               if (not "allownofile" in opts) and not os.path.isfile(datfil[typ]):
                  raise FileNotFoundError(f"ERROR: data file for this resolution does NOT exist ({datfil[typ]}).")


            # determine simulation year to use for the surface dataset:
            sim_yr_surfdat = sim_yr0
         
            cmd    = [queryDefaultNamelist] + queryfilopts.split() + resol.split() + \
            ["-options", f"sim_year={sim_yr_surfdat}{mkcrop},ssp_rcp={ssp_rcp}{mkcrop}", "-var", "mksrf_fvegtyp", "-namelist", "clmexp"]
            vegtyp = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
            if (vegtyp == ""):
               raise RuntimeError(f"** trouble getting vegtyp file with: {cmd}")

            cmd    = [queryDefaultNamelist] + queryfilopts.split() + resolhrv.split() + \
            ["-options", f"sim_year={sim_yr_surfdat}{mkcrop},ssp_rcp={ssp_rcp}{mkcrop}", "-var", "mksrf_fvegtyp", "-namelist", "clmexp"]
            hrvtyp = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
            if (hrvtyp == ""):
               raise RuntimeError(f"** trouble getting hrvtyp file with: {cmd}")

            options = ""
            crpdes  = "{:02d}pfts".format(numpft)
            if (numpft == 16):
               crpdes = crpdes + "_Irrig"

            if (mkcrop != ""):
               options = "-options " + mkcrop

            desc = "{}_{}_{}_simyr{}-{:04d}".format(ssp_rcp, crpdes, cmip_series, sim_yr0, int(sim_yrn))
            desc_surfdat = "{}_{}_{}_simyr{}".format(ssp_rcp, crpdes, cmip_series, sim_yr_surfdat)

            fsurdat_fname_base = ""
            fsurdat_fname = ""
            if (not opts["no_surfdata"]):
               fsurdat_fname_base = f"surfdata_{res}_{desc_surfdat}_{sdate}"
               fsurdat_fname = fsurdat_fname_base + ".nc"

            fdyndat_fname_base = ""
            fdyndat_fname = ""
            if transient:
               fdyndat_fname_base = f"landuse.timeseries_{res}_{desc}_{sdate}"
               fdyndat_fname = fdyndat_fname_base + ".nc"

            if (not fsurdat_fname and not fdyndat_fname):
               raise RuntimeError("ERROR: Tried to run mksurfdata_map without creating either a surface dataset or a landuse.timeseries file")

            logfile_fname = ""
            namelist_fname = ""
            if fsurdat_fname_base:
               logfile_fname = fsurdat_fname_base + ".log"
               namelist_fname = fsurdat_fname_base + ".namelist"
            else:
               logfile_fname = fdyndat_fname_base + ".log"
               namelist_fname = fdyndat_fname_base + ".namelist"

            landuse_timeseries_text_file = write_transient_timeseries_file(
               transient, desc, sim_yr0, sim_yrn,
               queryfilopts, resol, resolhrv, ssp_rcp, mkcrop,
               sim_yr_surfdat)

            print(f"CSMDATA is {CSMDATA} ")
            print(f"resolution: {res} ssp_rcp={ssp_rcp} sim_year = {sim_year}")
            print(f"namelist: {namelist_fname}")
         
            write_namelist_file(
               namelist_fname, logfile_fname, fsurdat_fname, fdyndat_fname,
               glc_nec, griddata, map, datfil, double,
               all_urb, no_inlandwet, vegtyp, hrvtyp, 
               landuse_timeseries_text_file, setnumpft)

            #
            # Delete previous versions of files that will be created
            #
            subprocess.run(["rm", "-f", fsurdat_fname, logfile_fname])
            #
            # Run mksurfdata_map with the namelist file
            #
            exedir = f"{clm5}/tools/mksurfdata_map" # TODO: read value from scrdir
            if opts["exedir"] is not None:
               exedir = opts["exedir"]

            print(f"{exedir}/mksurfdata_map < {namelist_fname}")
            if (not opts["debug"]):
               errcode = subprocess.run([f"{exedir}/mksurfdata_map", "<", namelist_fname]).returncode
               if errcode != 0: raise RuntimeError(f"ERROR in mksurfdata_map: {errcode}\n")

            print("\n===========================================\n")

            #
            # If urban point, overwrite urban variables from previous surface dataset to this one
            #
            if (urb_pt and not opts["no_surfdata"]):
               prvsurfdata = subprocess.run([queryDefaultNamelist] + queryopts.split() + ["-var", "fsurdat"])
               if (errcode != 0):
                  raise FileNotFoundError("ERROR:: previous surface dataset file NOT found")
   
               prvsurfdata.rstrip('\n')
               varlist = "CANYON_HWR,EM_IMPROAD,EM_PERROAD,EM_ROOF,EM_WALL,HT_ROOF,THICK_ROOF,THICK_WALL,T_BUILDING_MIN,WIND_HGT_CANYON,WTLUNIT_ROOF,WTROAD_PERV,ALB_IMPROAD_DIR,ALB_IMPROAD_DIF,ALB_PERROAD_DIR,ALB_PERROAD_DIF,ALB_ROOF_DIR,ALB_ROOF_DIF,ALB_WALL_DIR,ALB_WALL_DIF,TK_ROOF,TK_WALL,TK_IMPROAD,CV_ROOF,CV_WALL,CV_IMPROAD,NLEV_IMPROAD,PCT_URBAN,URBAN_REGION_ID"
               print("Overwrite urban parameters with previous surface dataset values")
               cmd = ["ncks", "-A", "-v", varlist, prvsurfdata, fsurdat_fname]
               print(cmd)
               if (not opts["debug"]): subprocess.run(cmd)

   print("Successfully created fsurdat files")

if __name__ == "__main__":
   main()
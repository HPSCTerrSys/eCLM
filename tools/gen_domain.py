#!/usr/bin/env python3

import os
import numpy as np
from math import pi
from datetime import datetime
from netCDF4 import Dataset
#-------------------------------------------------------------------------------
# PURPOSE:
# o given a SCRIP map matrix data file, create datm/dlnd/docn/dice domain data files
#
# NOTES:
# o all output data is base on the "_a" grid, the "_b" grid is ignored
# o to compile on an NCAR's SGI, tempest (Dec 2004):
#   unix> f90 -64 -mips4 -r8 -i4 -lfpe -I/usr/local/include Make_domain.F90 \
#         -L/usr/local/lib64/r4i4 -lnetcdf
#-------------------------------------------------------------------------------

def gen_domain(fmap, fn1_out_ocn, fn2_out_lnd, fn2_out_ocn, set_fv_pole_yc, usercomment):
    """
    fmap        - file name ( input nc file)
    fn1_out_ocn - file name (output nc file) for grid _a
    fn2_out_lnd - file name (output nc file) for grid _b (lnd frac)
    fn2_out_ocn - file name (output nc file) for grid _b (ocn frac)
    usercomment - file name (output nc file) for grid _b (ocn frac)
    """
    c0 = 0.0
    c1 = 1.0
    c90 = 90.0
    eps = 1.0e-12
    fminval = 0.001
    fmaxval = c1
    print("fmap   = ",fmap)
    print("fn1_out_ocn= ", fn1_out_ocn)
    print("fn2_out_lnd= ", fn2_out_lnd)
    print("fn2_out_ocn= ", fn2_out_ocn)
    print("usercomment= ", usercomment)
    print("eps    = ", eps)
    print("fminval= ",fminval)
    print("fmaxval= ",fmaxval)
    print("set_fv_pole_yc = ",set_fv_pole_yc)

    #----------------------------------------------------------------------------
    print(" ")
    print("input SCRIP data...")
    #----------------------------------------------------------------------------

    for nf in [1,2]:

        if (nf == 1):
            suffix = '_a'
            fn_out = fn1_out_ocn
            complf = False
        elif (nf == 2):
            suffix = '_b'
            fn_out_lnd = fn2_out_lnd
            fn_out_ocn = fn2_out_ocn
            complf = True
            pole_fix = False
        else:
            print(" ERROR: nf loop error ")
            raise IndexError("ERROR: nf loop error ")
        
        pole_fix = False
        if (nf == set_fv_pole_yc): pole_fix = True
        print(" pole_fix = ", pole_fix)

        print(" ")
        print("input file  = ", fmap)
        fid = Dataset(fmap, "r", format="NETCDF4")
        print("open ", fmap)

        str_da = 'unknown'
        str_db = 'unknown'
        str_grido = 'unknown'
        str_grida = 'unknown'

        str_da = fid.getncattr("domain_a")
        str_db = fid.getncattr('domain_b')

        try:
            str_grido = fid.getncattr('grid_file_ocn')
        except:
            str_grido = fid.getncattr('grid_file_src')

        try:
            str_grida = fid.getncattr('grid_file_atm')
        except:
            str_grida = fid.getncattr('grid_file_dst')

        print("domain_a     = ", str_da)
        print("domain_b     = ", str_db)
        print("grid_file_ocn= ", str_grido)
        print("grid_file_atm= ", str_grida)

        #----------------------------------------------
        # get domain info
        #----------------------------------------------
        if (suffix == '_b'):
            dst_grid_dims = fid.variables['dst_grid_dims'][:]

        n = fid.dimensions["n" + suffix].size
        nv = fid.dimensions["nv" + suffix].size
        try:
            ni = fid.dimensions["ni" + suffix].size
        except:
            ni = n
        try:
            nj = fid.dimensions["nj" + suffix].size
        except:
            nj = 1

        if (ni == 1 and nj == 0):
            ni = n
            nj = 1

        ns = fid.dimensions["n_s"].size
        na = fid.dimensions["n_a"].size
        dst_grid_rank = fid.dimensions["dst_grid_rank"].size
        src_grid_rank = fid.dimensions["src_grid_rank"].size

        src_grid_dims = fid.variables['src_grid_dims'][:]
        dst_grid_dims = fid.variables['dst_grid_dims'][:]

        try:
            str_grida = fid.getncattr('grid_file_atm')
        except:
            str_grida = fid.getncattr('grid_file_dst')

        print("n,nv,ni,nj,na,ns=",n,nv,ni,nj,na,ns)

        units_xc = fid.variables['xc' + suffix].getncattr("units")
        units_yc = fid.variables['yc' + suffix].getncattr("units")
        xc = fid.variables['xc' + suffix][:]     # x-coordinates of center for either _a or _b grid
        yc = fid.variables['yc' + suffix][:]     # y-coordinates of center for either _a or _b grid
        xv = fid.variables['xv' + suffix][:]     # x-coordinates of verticies for either _a or _b grid
        yv = fid.variables['yv' + suffix][:]     # y-coordinates of verticies for either _a or _b grid
        area = fid.variables['area' + suffix][:] # grid cell area

        #--- set default ocean frac ---

        if (not complf):
            # Determine ocn mask on ocn grid
            omask = fid.variables['mask' + suffix][:]
            ofrac = np.zeros(n)
            omask[omask != 0] = c1
        else:
            #----------------------------------------------------------------------------
            print("compute frac")
            #----------------------------------------------------------------------------

            lmask = []
            lfrac = []
            col = fid.variables['col'][:]
            row = fid.variables['row'][:]
            S = fid.variables['S'][:]
            mask_a = fid.variables['mask_a'][:]
            frac_a = np.zeros(n)
            # where (mask_a /= 0) frac_a = [c1]

            #--- compute ocean fraction on atm grid ---
            ofrac = np.zeros(n)
            for k in range(ns):
                ofrac[row[k]] = ofrac[row[k]] + frac_a[col[k]]*S[k]

                #--- convert to land fraction, 1.0-frac and ---
                #--- trap errors and modify computed frac ---
            lmask = np.zeros(n)
            omask = np.ones(n)
            lfrac_min = fmaxval
            lfrac_max = fminval
            for k in range(n):
                lfrac[k] = c1 - ofrac[k]
                lfrac_min = min(lfrac_min,lfrac[k])
                lfrac_max = max(lfrac_max,lfrac[k])
                if (lfrac[k] > fmaxval): lfrac[k] = c1
                if (lfrac[k] < fminval): lfrac[k] = c0   # extra requirement for landfrac
                ofrac[k] = c1 - lfrac[k]
                if (lfrac[k] != c0):
                    lmask[k] = 1
                if (ofrac[k] == c0):
                    omask[k] = 0

            print("----------------------------------------------------------------------")
            print("IMPORTANT: note original min/max frac and decide if that''s acceptable")
            print("original lfrac clipped above by       : ",fmaxval)
            print("original reset to zero when less than : ",fminval)
            print("original min, max lfrac : ",lfrac_min,lfrac_max)
            print("final min, max llfrac   : ',minval(lfrac),maxval(lfrac)")
            print("----------------------------------------------------------------------")

        fid.close()
        #-----------------------------------------------------------------
        # adjust j = 1 and j = nj lats to -+ 90 degrees
        #-----------------------------------------------------------------

        if (pole_fix):
            print("ni,nj= ",ni,nj)
            if (ni > 1 and nj == 1):
                if (dst_grid_rank != 2):
                    raise NotImplementedError("pole_fix not appropriate for unstructured grid")
            for i in range(dst_grid_dims[0]):
                yc[i] = -c90
                yc[n-dst_grid_dims[0]+i] = c90


        #-----------------------------------------------------------------
        # create a new nc files
        #-----------------------------------------------------------------

        print(" ")
        print("output domain data...")

        assert (n == ni*nj)

        print("nf = ", nf)
        if (nf == 1):
            if (src_grid_rank == 2):
                ni = src_grid_dims[0]
                nj = src_grid_dims[1]
            print("create ", fn_out)
            fid = Dataset(fn_out, "w", format="NETCDF4")
            print("write ", fn_out)
            write_file(fid, fmap, units_xc, units_yc, n, ni, nj, nv, \
                xc, yc, xv, yv, area, omask, ofrac, suffix, eps, pole_fix, \
                fmaxval, fminval, str_da, str_db, str_grido, str_grida)
            fid.close()
            print("successfully created domain file ", fn_out)
        elif (nf == 2):
            if (dst_grid_rank == 2):
                ni = dst_grid_dims[0]
                nj = dst_grid_dims[1]

            fid = Dataset(fn_out_lnd, "w", format="NETCDF4")
            print("write ", fn_out_lnd)
            write_file(fid, fmap, units_xc, units_yc, n, ni, nj, nv, \
                xc, yc, xv, yv, area, lmask, lfrac, suffix, eps, pole_fix, \
                fmaxval, fminval, str_da, str_db, str_grido, str_grida)
            fid.close()
            print("successfully created domain file ", fn_out_lnd)

            fid = Dataset(fn_out_ocn, "w", format="NETCDF4")
            print("write ", fn_out_ocn)
            write_file(fid, fmap, units_xc, units_yc, n, ni, nj, nv, \
                xc, yc, xv, yv, area, omask, ofrac, suffix, eps, pole_fix, \
                fmaxval, fminval, str_da, str_db, str_grido, str_grida)
            fid.close()
            print("successfully created domain file ", fn_out_ocn)

def usage_exit (arg):
    """
    """
    print(arg)
    print(" Purpose:")
    print("    Given a SCRIP map matrix data file from the ocean grid ")
    print("    (where the mask is defined) to the land grid, gen_domain ")
    print("    creates land and ocean domain files")
    print("    These files are currently used by ")
    print("       datm, dlnd, dice, docn, clm, cice(prescribed mode)")
    print(" ")
    print(" Usage: ")
    print("    gen_domain  -m <filemap>")
    print("                -o <gridocn>")
    print("                -l <gridlnd>")
    print("                [-p set_fv_pole_yc]")
    print("                [-c <usercomment>]")
    print(" ")
    print(" Where: ")
    print("    filemap = input conservative mapping file name (from ocn->atm)")
    print("    gridocn = output ocean grid name")
    print("    gridlnd = output land  grid name")
    print("    set_fv_pole_yc = [0,1,2] ~ optional, default = 0")
    print("    usercomment = optional, netcdf global attribute (character string)")
    print(" ")
    print(" The following output domain files are created:")
    print("    domain.lnd.gridlnd_gridocn.nc")
    print("      land domain file on the land grid with a ")
    print("      land fraction corresponding to ")
    print("      (1-gridocn) mask mapped to the land grid")
    print("    domain.ocn.gridlnd_gridocn.nc")
    print("      ocean domain on the land grid with an ")
    print("      ocean fraction corresponding to the")
    print("      gridocn mask mapped to the land grid")
    print("      this is used when both atm,lnd,ice,ocn are all on the")
    print("      same grid (F compset)")
    print("    domain.ocn.gridocn.nc")
    print("      ocean domain on the ocean grid ")
    print(" ")

def write_file(fid: Dataset, fmap, units_xc, units_yc, n, ni, nj, nv, \
       xc, yc, xv, yv, area, mask, frac, suffix, eps, pole_fix, \
       fmaxval, fminval, str_da, str_db, str_grido, str_grida):
    version = 'SVN $Id: gen_domain.F90 65202 2014-11-06 21:07:45Z mlevy@ucar.edu $'

    # Set netCDF global attributes
    fid.title = "CESM domain data: "
    fid.Conventions = "CF-1.0"
    fid.source_code = version
    fid.SVN_url = " $URL: https://svn-ccsm-models.cgd.ucar.edu/tools/mapping/gen_domain/trunk/src/gen_domain.F90 $"
    fid.Compiler_Optimized = "FALSE"
    fid.hostname = os.uname().nodename
    fid.history = "created by {}, {}".format("user", datetime.now())
    fid.source = fmap
    fid.map_domain_a = str_da
    fid.map_domain_b = str_db
    fid.map_grid_file_ocn = str_grido
    fid.map_grid_file_atm = str_grida
    fid.user_comment = ""

    # dimension data
    fid.createDimension("n", n)   # of points total
    fid.createDimension("ni", ni) # of points wrt i
    fid.createDimension("nj", nj) # of points wrt j
    fid.createDimension("nv", nv) # of verticies per cell

    # define data -- coordinates, input grid
    fid.createVariable("xc","f4",("nj","ni"))
    fid.variables["xc"].long_name = "longitude of grid cell center"
    fid.variables["xc"].units = "degrees_east"
    fid.variables["xc"].bounds = "xv"

    fid.createVariable("yc","f4",("nj","ni"))
    fid.variables["yc"].long_name = "latitude of grid cell center"
    fid.variables["yc"].units = "degrees_north"
    fid.variables["yc"].bounds = "yv"
    if pole_fix:
        fid.variables["yc"].filter1 = "set_fv_pole_yc ON, yc = -+90 at j=1,j=nj"
    
    fid.createVariable("xv","f4",("nj", "ni", "nv"))
    fid.variables["xv"].long_name = "longitude of grid cell verticies"
    fid.variables["xv"].units = "degrees_east"

    fid.createVariable("yv","f4",("nj", "ni", "nv"))
    fid.variables["yv"].long_name = "latitude of grid cell verticies"
    fid.variables["yv"].units = "degrees_north"

    fid.createVariable("mask","i4",("nj","ni"))
    fid.variables["mask"].long_name = "domain mask"
    fid.variables["mask"].note = "unitless"
    fid.variables["mask"].coordinates = "xc yc"
    fid.variables["mask"].comment = "0 value indicates cell is not active"

    fid.createVariable("area","f4",("nj","ni"))
    fid.variables["area"].long_name = "area of grid cell in radians squared"
    fid.variables["area"].coordinates = "xc yc"
    fid.variables["area"].units = "radian2"

    fid.createVariable("frac","f4",("nj","ni"))
    fid.variables["frac"].long_name = "fraction of grid cell that is active"
    fid.variables["frac"].coordinates = "xc yc"
    fid.variables["frac"].note = "unitless"
    fid.variables["frac"].filter1 = f"error if frac> 1.0+eps or frac < 0.0-eps; eps = {eps}"
    fid.variables["frac"].filter2 = f"limit frac to [fminval,fmaxval]; fminval={fminval}, fmaxval={fmaxval}"

    if units_xc == "radians":
        xc = xc * 100 / pi
        xv = xv * 100 / pi
        units_xc = "degrees"

    if units_yc == "radians":
        yc = yc * 100 / pi
        yv = yv * 100 / pi
        units_yc = "degrees"
    
    fid.variables["xc"][:,:] = xc
    fid.variables["yc"][:,:] = yc
    fid.variables["xv"][:,:,:] = xv
    fid.variables["yv"][:,:,:] = yv
    fid.variables["mask"][:,:] = mask
    fid.variables["area"][:,:] = area
    fid.variables["frac"][:,:] = frac

def main():
    # TODO: read these params from command line
    set_fv_pole_yc = 0
    fmap = "$CESMDATAROOT/inputdata/lnd/clm2/mappingdata/maps/Nigeria/map_0.9x1.25_GRDC_to_Nigeria_nomask_aave_da_c200503.nc"
    fn1_out = 'Nigeria'
    fn2_out = 'Nigeria'
    usercomment = 'null'

    if (fmap == 'null' or fn1_out == 'null' or fn2_out== 'null'):
        usage_exit ('Must specify all the following arguments')
    cdate = "c{}".format(datetime.now().strftime("%Y%m%d"))
    fn1_out_ocn = f"domain.ocn.{fn1_out}.{cdate}.nc"
    fn2_out_lnd = f"domain.lnd.{fn2_out}_{fn1_out}.{cdate}.nc"
    fn2_out_ocn = f"domain.ocn.{fn2_out}_{fn1_out}.{cdate}.nc"
    gen_domain (fmap, fn1_out_ocn, fn2_out_lnd, fn2_out_ocn, set_fv_pole_yc, usercomment)

if __name__ == "__main__":
   main()
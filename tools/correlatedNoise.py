#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 14:17:32 2023

@author: Yorck Ewerdwalbesloh
"""
# %% Description
# This script generates spatially and temporally correlated noise and correlation of the variables
# Four variables are disturbed:
# - Surface precipitation, log-normal multiplicative
# - temperature at lowest atmospheric level, additive
# - solar radiation, log-normal multilicative
# - long wave radiation, additive


# %% Modules
import numpy as np
import scipy.io
import netCDF4 as nc
from scipy.interpolate import griddata
import os
import datetime
from scipy.spatial import distance
import calendar
import json
import pdb


def copy_attr_dim(src, dst, usr=None):
    # copy attributes
    for name in src.ncattrs():
        dst.setncattr("original_attribute_" + name, src.getncattr(name))
    # copy dimensions
    for name, dimension in src.dimensions.items():
        dst.createDimension(name, len(dimension))
    # Additional attribute
    if usr is None:
        usr = os.getlogin()
    dst.setncattr("perturbed_by", usr)
    dst.setncattr("perturbed_on_date", datetime.datetime.today().strftime("%d.%m.%y"))


def compute_distances(e, f):
    # Create a 2D array of (x, y) coordinates
    points = np.column_stack((e, f))
    dist = distance.cdist(points, points, "euclidean")

    return dist


def rnd_state_serialize():
    tmp_state = np.random.get_state()
    save_state = ()
    for i in tmp_state:
        if type(i) is np.ndarray:
            save_state = save_state + (i.tolist(),)
        else:
            save_state = save_state + (i,)
    json.dump(save_state, open("rnd_state.json", "w"))


def rnd_state_deserialize():
    tmp_state = json.load(open("rnd_state.json", "r"))
    load_state = ()
    for i in tmp_state:
        if type(i) is list:
            load_state = load_state + (np.array(i),)
        else:
            load_state = load_state + (i,)
    np.random.set_state(load_state)


# Log normal to normal and vice versa
# for standard deviation and mean (formula from wikipedia)
def ln_to_n(sd_ln, mean_ln):
    term = 1.0 + sd_ln * sd_ln / mean_ln / mean_ln
    return (np.sqrt(np.log(term)), np.log(mean_ln / np.sqrt(term)))


def n_to_ln(sd_n, mean_n):
    return (
        (np.exp(sd_n * sd_n) - 1.0) * np.exp(2.0 * mean_n + sd_n * sd_n),
        np.exp(mean_n + sd_n * sd_n / 2.0),
    )


# %% Parameters
outputpath = "/path/to/noise/"
if outputpath == "/path/to/noise/":
    raise ValueError("ERROR: Please set 'outputpath' to your own output directory path!")

dt = 3  # time interval --> 3 hours for ERA5 data --> if different, this has to be adjusted

n_ens = 64  # number of ensemble members

# Correlation Length
L_P = 80  # km for precipitation
L_T = 250  # km for temperature, solar radiation and long wave radiation

# Persistance parameter
rho = (
    7 / 8
)  # decorrelation time 24h. time step of forcings 3h --> decorrelation after one days which means 3h are 1/8 --> 7/8 decorrelation time step

# Covariance matrix for fields
C_var = np.array(
    [[1, 0, -0.8, 0.5], [0, 1, 0.4, 0.4], [-0.8, 0.4, 1, -0.5], [0.5, 0.4, -0.5, 1]]
)

# standard deviations and mean, for precipitation and short wave radiations, log normal distributions are there.

std = np.array([ln_to_n(0.3, 1.0)[0], 2, ln_to_n(0.3, 1.0)[0], 30])
mean = np.array([ln_to_n(0.3, 1.0)[1], 0, ln_to_n(0.3, 1.0)[1], 0])


# min and max for disturbance
trunc_PREC = np.array([0.3, 1.7])
trunc_TBOT = np.array([-5, 5])
trunc_FSDS = np.array([0.3, 1.7])
trunc_FLDS = np.array([-70, 70])

# Distance between grid points
ds = 12.5

# number of points for generating noise
nn = 100

# Specify the range of years (e.g., 2003 to 2020)
start_year = 2002
end_year = 2022

# Create the year and month arrays
years = [year for year in range(start_year, end_year + 1) for month in range(1, 13)]
months = [month for year in range(start_year, end_year + 1) for month in range(1, 13)]


rnd_state_file = "/path/to/random/state/rnd_state.json"
if rnd_state_file == "/path/to/random/state/rnd_state.json":
    raise ValueError("ERROR: Please set 'rnd_state_file' to your own random state file path!")

force_seed = True
# Either seed random number generator or continue with existing state
if not os.path.isfile(rnd_state_file) or force_seed:
    np.random.seed(42)
else:
    rnd_state_deserialize()

print("Starting")


# %% Cholesky decomposition of covariance matrix for variable correlation
R_var = np.linalg.cholesky(C_var).T

# %% Grid of atmospheric data
fname = "/path/to/forcings/era5/2011-01.nc"
if fname == "/path/to/forcings/era5/2011-01.nc":
    raise ValueError("ERROR: Please set 'fname' to your own forcing data path!")

with nc.Dataset(fname) as src:
    dim_time = src.dimensions["time"].size
    dim_lat = src.dimensions["lat"].size
    dim_lon = src.dimensions["lon"].size


# %% grid of input data (not real longitude and latitude but only grid on which the noise is simulated)
X = np.arange(0, dim_lon * ds, ds)
Y = np.arange(0, dim_lat * ds, ds)

c1, d1 = np.meshgrid(X, Y)
c = np.transpose(c1).ravel()
d = np.transpose(d1).ravel()


# %% grid for generating noise
X = np.linspace(np.min(c), np.max(c), nn)  # grid points
Y = np.linspace(np.min(d), np.max(d), nn)

e1, f1 = np.meshgrid(X, Y)  # raster
e = np.transpose(e1).ravel()
f = np.transpose(f1).ravel()

# %% generate Matrix for spatial correlation, distances between all grid points have to be computed

dist = compute_distances(e, f)

# precipitation --> shorter scales (weather)

C_P = np.exp(-(dist / L_P))
R_P = np.linalg.cholesky(C_P).T

# temperature
C_T = np.exp(-(dist / L_T))
R_T = np.linalg.cholesky(C_T).T

# %% Generate random noise for each variable
e_PREC = np.random.randn(len(e))
e_TBOT = np.random.randn(len(e))
e_FSDS = np.random.randn(len(e))
e_FLDS = np.random.randn(len(e))

# %% Correlations between variables
temp = np.array((e_PREC, e_TBOT, e_FSDS, e_FLDS)).T.dot(R_var)
e_PREC = temp[:, 0]
e_TBOT = temp[:, 1]
e_FSDS = temp[:, 2]
e_FLDS = temp[:, 3]
del temp

# %% Correlate random noise
e_corrSpat_PREC = R_P.T.dot(e_PREC)
e_corrSpat_TBOT = R_T.T.dot(e_TBOT)
e_corrSpat_FSDS = R_T.T.dot(e_FSDS)
e_corrSpat_FLDS = R_T.T.dot(e_FLDS)


# %% Extend to large grid
e_corrSpat_PREC = griddata((e, f), e_corrSpat_PREC, (c, d), "linear")
e_add_PREC = 0.2 * np.random.randn(dim_lon * dim_lat, 1)
e_corrSpat_PREC = e_corrSpat_PREC.ravel() + e_add_PREC.ravel()

e_corrSpat_TBOT = griddata((e, f), e_corrSpat_TBOT, (c, d), "linear")
e_add_TBOT = 0.2 * np.random.randn(dim_lon * dim_lat, 1)
e_corrSpat_TBOT = e_corrSpat_TBOT.ravel() + e_add_TBOT.ravel()

e_corrSpat_FSDS = griddata((e, f), e_corrSpat_FSDS, (c, d), "linear")
e_add_FSDS = 0.2 * np.random.randn(dim_lon * dim_lat, 1)
e_corrSpat_FSDS = e_corrSpat_FSDS.ravel() + e_add_FSDS.ravel()

e_corrSpat_FLDS = griddata((e, f), e_corrSpat_FLDS, (c, d), "linear")
e_add_FLDS = 0.2 * np.random.randn(dim_lon * dim_lat, 1)
e_corrSpat_FLDS = e_corrSpat_FLDS.ravel() + e_add_FLDS.ravel()

if not force_seed:
    rnd_state_serialize()

e_prev_PREC = e_corrSpat_PREC
e_prev_TBOT = e_corrSpat_TBOT
e_prev_FSDS = e_corrSpat_FSDS
e_prev_FLDS = e_corrSpat_FLDS

del e_corrSpat_PREC, e_corrSpat_TBOT, e_corrSpat_FSDS, e_corrSpat_FLDS
del e_add_PREC, e_add_TBOT, e_add_FSDS, e_add_FLDS

PREC_old = 0
TBOT_old = 0
FSDS_old = 0
FLDS_old = 0
print("Looping over years")

i = 0
for year, month in zip(years, months * len(years)):
    print(str(year) + "-" + str(month).zfill(2))
    filename = outputpath + str(year) + "-" + str(month).zfill(2) + ".nc"

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fname = (
        "/path/to/forcings/era5/"
        + str(year)
        + "-"
        + str(month).zfill(2)
        + ".nc"
    )
    if fname.startswith("/path/to/forcings/era5/"):
        raise ValueError("ERROR: Please update the forcing data path in the loop to your own directory!")

    # number of extra entries due to ensemble run
    timeExtra = (n_ens - 1) * (24 / dt)

    # number of time steps for files
    timeNum = calendar.monthrange(year, month)[1] * (24 / dt) + timeExtra
    # pdb.set_trace()
    with nc.Dataset(filename, "w") as ncid:
        dimid_lon = ncid.createDimension("lon", dim_lon)
        dimid_lat = ncid.createDimension("lat", dim_lat)
        dimid_time = ncid.createDimension("time", timeNum)
        with nc.Dataset(fname) as src:
            for name, var in src.variables.items():
                if name == "latitude" or name == "longitude":
                    nvar = ncid.createVariable(name, var.datatype, ("lat", "lon"))
                    ncid[name].setncatts(src[name].__dict__)
                    ncid[name][:] = src[name][:]
                if name == "time":
                    nvar = ncid.createVariable(name, var.datatype, ("time"))
                    ncid[name].setncatts(src[name].__dict__)
                    ncid[name][: len(src[name][:])] = src[name][:]
                    start = 90000000
                    length = len(ncid[name][len(src[name][:]) :])
                    ncid[name][len(src[name][:]) :] = [start + i for i in range(length)]

        PRECTmms_ID = ncid.createVariable("PRECTmms", "f8", ("time", "lat", "lon"))
        TBOT_ID = ncid.createVariable("TBOT", "f8", ("time", "lat", "lon"))
        FSDS_ID = ncid.createVariable("FSDS", "f8", ("time", "lat", "lon"))
        FLDS_ID = ncid.createVariable("FLDS", "f8", ("time", "lat", "lon"))

        # %% Loops over time
        PREC = np.zeros((dim_lon, dim_lat, int(timeNum)))
        TBOT = PREC.copy()
        FSDS = PREC.copy()
        FLDS = PREC.copy()
        t_start = 0

        if i > 0:
            PREC[:, :, : int(timeExtra)] = PREC_old[:, :, -int(timeExtra) :]
            TBOT[:, :, : int(timeExtra)] = TBOT_old[:, :, -int(timeExtra) :]
            FSDS[:, :, : int(timeExtra)] = FSDS_old[:, :, -int(timeExtra) :]
            FLDS[:, :, : int(timeExtra)] = FLDS_old[:, :, -int(timeExtra) :]
            t_start += timeExtra

        for t in range(int(t_start), int(timeNum)):

            print("Time Step ", t + 1, "/", timeNum)
            # %% Random numbers
            e_PREC = np.random.randn(len(e))
            e_TBOT = np.random.randn(len(e))
            e_FSDS = np.random.randn(len(e))
            e_FLDS = np.random.randn(len(e))

            # %% Correlation between variables on small grid
            lok = np.array((e_PREC, e_TBOT, e_FSDS, e_FLDS)).T
            temp = lok.dot(R_var)
            del lok
            coeff_corr = np.corrcoef(temp.T)
            e_PREC = temp[:, 0]
            e_TBOT = temp[:, 1]
            e_FSDS = temp[:, 2]
            e_FLDS = temp[:, 3]

            # %% Correlate random noise on small grid
            e_corrSpat_PREC = R_P.T.dot(e_PREC)
            e_corrSpat_TBOT = R_T.T.dot(e_TBOT)
            e_corrSpat_FSDS = R_T.T.dot(e_FSDS)
            e_corrSpat_FLDS = R_T.T.dot(e_FLDS)

            del e_PREC, e_TBOT, e_FSDS, e_FLDS

            # %% Extend to large grid
            e_corrSpat_PREC = griddata((e, f), e_corrSpat_PREC, (c, d), "linear")
            e_add_PREC = 0.2 * np.random.randn(dim_lon * dim_lat, 1)
            e_corrSpat_PREC = e_corrSpat_PREC.ravel() + e_add_PREC.ravel()

            e_corrSpat_TBOT = griddata((e, f), e_corrSpat_TBOT, (c, d), "linear")
            e_add_TBOT = 0.2 * np.random.randn(dim_lon * dim_lat, 1)
            e_corrSpat_TBOT = e_corrSpat_TBOT.ravel() + e_add_TBOT.ravel()

            e_corrSpat_FSDS = griddata((e, f), e_corrSpat_FSDS, (c, d), "linear")
            e_add_FSDS = 0.2 * np.random.randn(dim_lon * dim_lat, 1)
            e_corrSpat_FSDS = e_corrSpat_FSDS.ravel() + e_add_FSDS.ravel()

            e_corrSpat_FLDS = griddata((e, f), e_corrSpat_FLDS, (c, d), "linear")
            e_add_FLDS = 0.2 * np.random.randn(dim_lon * dim_lat, 1)
            e_corrSpat_FLDS = e_corrSpat_FLDS.ravel() + e_add_FLDS.ravel()

            del e_add_PREC, e_add_TBOT, e_add_FSDS, e_add_FLDS

            if not force_seed:
                rnd_state_serialize()

            # %% Correlate temporally
            e_corrSpatTemp_PREC = (
                rho * e_prev_PREC + np.sqrt(1 - rho**2) * e_corrSpat_PREC
            )
            e_corrSpatTemp_TBOT = (
                rho * e_prev_TBOT + np.sqrt(1 - rho**2) * e_corrSpat_TBOT
            )
            e_corrSpatTemp_FSDS = (
                rho * e_prev_FSDS + np.sqrt(1 - rho**2) * e_corrSpat_FSDS
            )
            e_corrSpatTemp_FLDS = (
                rho * e_prev_FLDS + np.sqrt(1 - rho**2) * e_corrSpat_FLDS
            )
            del e_corrSpat_PREC, e_corrSpat_TBOT, e_corrSpat_FSDS, e_corrSpat_FLDS
            del e_prev_PREC, e_prev_TBOT, e_prev_FSDS, e_prev_FLDS

            # %% new previous fields
            e_prev_PREC = e_corrSpatTemp_PREC
            e_prev_TBOT = e_corrSpatTemp_TBOT
            e_prev_FSDS = e_corrSpatTemp_FSDS
            e_prev_FLDS = e_corrSpatTemp_FLDS

            # %% Truncate noise
            e_corrSpatTemp_PREC = np.exp(mean[0] + std[0] * e_corrSpatTemp_PREC)
            e_corrSpatTemp_PREC[e_corrSpatTemp_PREC < trunc_PREC[0]] = trunc_PREC[0]
            e_corrSpatTemp_PREC[e_corrSpatTemp_PREC > trunc_PREC[1]] = trunc_PREC[1]

            e_corrSpatTemp_TBOT = std[1] * e_corrSpatTemp_TBOT
            e_corrSpatTemp_TBOT[e_corrSpatTemp_TBOT < trunc_TBOT[0]] = trunc_TBOT[0]
            e_corrSpatTemp_TBOT[e_corrSpatTemp_TBOT > trunc_TBOT[1]] = trunc_TBOT[1]

            e_corrSpatTemp_FSDS = np.exp(mean[2] + std[2] * e_corrSpatTemp_FSDS)
            e_corrSpatTemp_FSDS[e_corrSpatTemp_FSDS < trunc_FSDS[0]] = trunc_FSDS[0]
            e_corrSpatTemp_FSDS[e_corrSpatTemp_FSDS > trunc_FSDS[1]] = trunc_FSDS[1]

            e_corrSpatTemp_FLDS = std[3] * e_corrSpatTemp_FLDS
            e_corrSpatTemp_FLDS[e_corrSpatTemp_FLDS < trunc_FLDS[0]] = trunc_FLDS[0]
            e_corrSpatTemp_FLDS[e_corrSpatTemp_FLDS > trunc_FLDS[1]] = trunc_FLDS[1]

            # %% Apply to data
            PREC[:, :, t] = np.reshape(e_corrSpatTemp_PREC, (dim_lon, dim_lat))
            TBOT[:, :, t] = np.reshape(e_corrSpatTemp_TBOT, (dim_lon, dim_lat))
            FSDS[:, :, t] = np.reshape(e_corrSpatTemp_FSDS, (dim_lon, dim_lat))
            FLDS[:, :, t] = np.reshape(e_corrSpatTemp_FLDS, (dim_lon, dim_lat))

            del (
                e_corrSpatTemp_PREC,
                e_corrSpatTemp_TBOT,
                e_corrSpatTemp_FSDS,
                e_corrSpatTemp_FLDS,
            )

        # %% Save disturbed variables
        # Write PREC variable

        PRECTmms_ID[:] = np.transpose(PREC, (2, 1, 0))

        # Write TBOT variable
        TBOT_ID[:] = np.transpose(TBOT, (2, 1, 0))

        # Write FSDS variable
        FSDS_ID[:] = np.transpose(FSDS, (2, 1, 0))

        # Write FLDS variable
        FLDS_ID[:] = np.transpose(FLDS, (2, 1, 0))

    # pdb.set_trace()
    PREC_old = PREC
    TBOT_old = TBOT
    FSDS_old = FSDS
    FLDS_old = FLDS

    del PREC, TBOT, FSDS, FLDS

    i = i + 1

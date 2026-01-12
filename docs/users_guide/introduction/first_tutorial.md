# First Tutorial

```{warning}
TODO!!!
```

Welcome! This guide will teach you on how to set up and run eCLM for the first time. Normally, eCLM is run
on an HPC cluster, and thus eCLM user guides typically rely on steps that only work on a particular HPC
environment. Not in this tutorial though: the aim is toward general users with only a personal laptop/computer.
The most important thing to learn is the basic workflow of running eCLM simulation for the first time:

1. Install eCLM dependencies
2. Build eCLM
3. Set up a simulation experiment
4. Run eCLM

Steps 1 and 2 are the most time-consuming part. But once set up, you only need to do steps 3 and 4.

## Prerequisites

**This guide has been written to work on an Ubuntu system**. For Windows/Mac users, please set up a virtual
[Ubuntu 24.04 LTS] OS first through a container app (*e.g.* [Podman] or [Docker]). All steps in this guide
assume an Ubuntu system.

**Users are also expected to be familiar with using command-line interfaces (CLI).** For GUI users, unfortunately CLI is
usually the only option of working in an HPC environment. Consider this as a preparation to use HPC! You don't have to be
a CLI wizard; for starters you just need to know how to run your local terminal/console app and what the basic commands
such as `cd`, `ls`, `pwd`, and `cat`, do. If you want a refresher, check out the [beginner-friendly shell tutorial by MIT].
It will arm you with more than enough info to go through this tutorial.

## 1. Load eCLM dependencies

eCLM requires CMake, a Fortran compiler, an MPI library, and NetCDF libraries. On an HPC cluster these packages
are typically installed already. For our case, we need to install them:

```sh
# Install basic utilities
sudo apt-get install libxml2-utils cmake

# Install Fortran and MPI compilers
sudo apt-get install gfortran openmpi-bin libopenmpi-dev

# Install NetCDF libraries
sudo apt-get install netcdf-bin libnetcdf-dev libnetcdff-dev libpnetcdf-dev
```

## 2. Build eCLM

```{hint}
**Building** in this context means the transformation of source codes (e.g. eCLM Fortran source codes)
into an application binary (e.g. `eclm.exe`) which the users can run.
```

```sh
# You can modify the eCLM install directory, or simply use the provided default.
eCLM_INSTALL_DIR=${HOME}/eCLM  
mkdir -p ${eCLM_INSTALL_DIR}

# eCLM can be easily built via the TSMP2 build system. The following step will download TSMP2.
git clone https://github.com/HPSCTerrSys/TSMP2.git
cd TSMP2

# Start the eCLM build process (will take <10minutes).
export SYSTEMNAME="UBUNTU"
./build_tsmp2.sh eCLM --install-dir=${eCLM_INSTALL_DIR}
```

## 3. Set up a simulation experiment

```sh
git clone https://icg4geo.icg.kfa-juelich.de/ExternalReposPublic/tsmp2-static-files/extpar_eclm_wuestebach_sp.git
cd extpar_eclm_wuestebach_sp/static.resources
generate_wtb_namelists.sh 1x1_wuestebach
```

## 4. Run eCLM

```sh
cd 1x1_wuestebach
mpirun -np 1 ${eCLM_INSTALL_DIR}/bin/eclm.exe
```

## Next Steps

[Podman]: https://docs.podman.io/en/latest/Tutorials.html
[Docker]: https://docs.docker.com/get-started
[VirtualBox]: https://www.virtualbox.org
[UTM]: https://mac.getutm.app
[Ubuntu 24.04 LTS]: https://hub.docker.com/_/ubuntu
[beginner-friendly shell tutorial by MIT]: https://missing.csail.mit.edu/2020/course-shell

# First Tutorial

Welcome! This guide walks you through the basic steps in setting up eCLM. eCLM is typically used on an HPC cluster.
Still, you can run small eCLM test cases (e.g. single-point domains) on your laptop. This tutorial aims to teach you
just that: setting up and running a small eCLM test case on your laptop. This workflow remains more or less the same
once you move to an HPC cluster to do some serious eCLM runs.

An HPC environment and a personal computing environment (*e.g.* your laptop) use different sets of tools to accomplish
the same task. However, the goal is not overwhelm you with tool usage (which could be an interesting exercise in itself),
but rather focus on a common workflow that gets you up to speed with eCLM:

[1. Load eCLM dependencies](./first_tutorial.md#load-eclm-dependencies)
[2. Build eCLM](#build-eclm)
[3. Generate namelists](#generate-namelists)
[4. Run eCLM](#run-eclm)

## Prerequisites

**This guide has been written to work on an Ubuntu system**. For Windows/Mac users, I suggest to set up a virtual
[Ubuntu 24.04 LTS] OS first through a container app (*e.g.* [Podman] or [Docker]).

**Users are also expected to be familiar with using command-line interfaces (CLI).** For GUI users, unfortunately CLI is
the most of the time the only option of using an HPC cluster. Consider this as a preparation to use HPC!. You don't have to be
a CLI wizard; for starters you just need to know how to run your local terminal/console app and what the basic commands
such as `cd`, `ls`, `pwd`, and `cat`, do. If you want a refresher, check out the [beginner-friendly shell tutorial by MIT].
It will arm you with more than enough info to go through this tutorial.

## 1. Load eCLM dependencies

eCLM requires CMake, a Fortran compiler, an MPI library, and NetCDF. On an HPC cluster these libraries are typically
installed already. For our case, we need to install them:

```sh
# Install basic utilities
sudo apt-get install libxml2-utils cmake

# Install Fortran and MPI compilers
sudo apt-get install gfortran openmpi-bin libopenmpi-dev

# Install NetCDF libraries
sudo apt-get install netcdf-bin libnetcdf-dev libnetcdff-dev libpnetcdf-dev
```

## 2. Build eCLM

First, specify a folder where you want eCLM to be installed.

```sh
eCLM_INSTALL_DIR=${HOME}/eCLM  # you can change this to any directory
mkdir -p ${eCLM_INSTALL_DIR}   # create eCLM install folder
```

Get the [TSMP2 build system](https://github.com/HPSCTerrSys/TSMP2).

```sh
git clone https://github.com/HPSCTerrSys/TSMP2.git
cd TSMP2
```

```sh
./build_tsmp2.sh eCLM --install-dir=${eCLM_INSTALL_DIR}
```

## 3. Generate namelists


```sh
git clone https://icg4geo.icg.kfa-juelich.de/ExternalReposPublic/tsmp2-static-files/extpar_eclm_wuestebach_sp.git
cd extpar_eclm_wuestebach_sp/static.resources
generate_wtb_namelists.sh 1x1_wuestebach
```

The last command should generate ...

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

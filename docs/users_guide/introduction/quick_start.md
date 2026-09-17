# Quick Start

This guide lets you install eCLM on the target machine.

## Setting up eCLM on your local machine

Download [Podman].

1. Fetch the eCLM container image. On your terminal, run the ff.:

```sh
WORKDIR=$HOME/eclm_container
mkdir $WORKDIR
podman run --name eclm-dev -it -v ${WORKDIR}:/root/$(basename ${WORKDIR}) hpscterrsys/eclm:latest-dev
```

2. Build eCLM.

```sh
cd /root/eclm_container

# Download eCLM
git clone https://github.com/HPSCTerrSys/eCLM.git

# Build eCLM
cmake -S src -B bld -DCMAKE_INSTALL_PREFIX=$HOME/.local -DCMAKE_BUILD_TYPE="DEBUG"
cmake --build bld --parallel 4
cmake --install bld
```

3. Set up a simulation experiment.

```sh
cd /root/eclm_container

# Generate namelists files.
git clone https://icg4geo.icg.kfa-juelich.de/ExternalReposPublic/tsmp2-static-files/extpar_eclm_wuestebach_sp.git wtb_data
cd wtb_data/static.resources/generate_wtb_namelists.sh /root/1x1_wuestebach
```

4. Run eCLM.

```sh
cd /root/1x1_wuestebach
mpirun -np 1 eclm.exe
```

## Setting up eCLM on HPC systems

The steps are similar to above. The only difference is the build step and running step.

1. Download TSMP2 build system.

```sh
# eCLM can be easily built via the TSMP2 build system. The following step will download TSMP2.
git clone https://github.com/HPSCTerrSys/TSMP2.git
```

2. Build eCLM

```sh
# Build eCLM
cd TSMP2
./build_tsmp2.sh eCLM
```

3. Set up a simulation experiment.

```sh
cd ..
git clone https://icg4geo.icg.kfa-juelich.de/ExternalReposPublic/tsmp2-static-files/extpar_eclm_wuestebach_sp.git
cd extpar_eclm_wuestebach_sp/static.resources
./generate_wtb_namelists.sh 1x1_wuestebach
```

4a. (ONLY on JSC systems) Set up the run directory with symlinks and a
job script.

```sh
cd 1x1_wuestebach

# Symlink the eCLM executable and the JSC environment file
ln -s ../../../TSMP2/bin/JUWELS_eCLM/bin/eclm.exe eclm.exe
ln -s ../../../TSMP2/bin/JUWELS_eCLM/jsc.2025.intel.psmpi loadenvs

cat > jobscript.slurm << 'EOF'
#!/usr/bin/env bash
#SBATCH --job-name=1x1_wuestebach
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48
#SBATCH --account=jibg36
#SBATCH --partition=batch
#SBATCH --time=0:30:00
#SBATCH --output=logs/%j.eclm.1x1_wuestebach.out
#SBATCH --error=logs/%j.eclm.1x1_wuestebach.err

# Load environment
source loadenvs

# Run model
srun -n $SLURM_NTASKS eclm.exe
EOF
```

Run eCLM:
```sh
# On JSC systems (submit via Slurm):
sbatch jobscript.slurm
```

4b. (GENERIC HPC) Run eCLM.

```sh
cd 1x1_wuestebach
mpirun -np 1 eclm.exe
```

[Podman]: https://docs.podman.io/en/latest/Tutorials.html
[Docker]: https://docs.docker.com/get-started
[VirtualBox]: https://www.virtualbox.org
[UTM]: https://mac.getutm.app
[Ubuntu 24.04 LTS]: https://hub.docker.com/_/ubuntu

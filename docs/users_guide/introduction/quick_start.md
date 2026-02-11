# Quick Start

This guide lets you install eCLM on the target machine.

## Setting up eCLM on your local machine

Download [Podman].

1. Fetch the eCLM container image. On your terminal, run the ff.:

```sh
mkdir $HOME/eclm_share
podman run --name eclm -it --mount type=bind,src=$HOME/eclm_share,target=/share hpscterrsys/eclm:latest
```

Change permissions.

```sh
sudo chown -R user /share
sudo chgrp -R hpscterrsys /share
```

2. Build eCLM.

```sh
cd /share
build_eclm.sh
```

3. Set up a simulation experiment.

```sh
cd /share
git clone https://icg4geo.icg.kfa-juelich.de/ExternalReposPublic/tsmp2-static-files/extpar_eclm_wuestebach_sp.git
cd extpar_eclm_wuestebach_sp/static.resources
generate_wtb_namelists.sh 1x1_wuestebach
```

4. Run eCLM.

```sh
cd 1x1_wuestebach
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
cd /share
git clone https://icg4geo.icg.kfa-juelich.de/ExternalReposPublic/tsmp2-static-files/extpar_eclm_wuestebach_sp.git
cd extpar_eclm_wuestebach_sp/static.resources
generate_wtb_namelists.sh 1x1_wuestebach
```

4. Run eCLM.

```sh
cd 1x1_wuestebach
mpirun -np 1 eclm.exe
```

[Podman]: https://docs.podman.io/en/latest/Tutorials.html
[Docker]: https://docs.docker.com/get-started
[VirtualBox]: https://www.virtualbox.org
[UTM]: https://mac.getutm.app
[Ubuntu 24.04 LTS]: https://hub.docker.com/_/ubuntu

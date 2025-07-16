# Installing eCLM

The easiest way to install eCLM is through [TSMP2 build system](https://github.com/HPSCTerrSys/TSMP2). Currently only these OS/machines are supported:

- Ubuntu
- [Julich supercomputers](https://www.fz-juelich.de/en/ias/jsc/systems/supercomputers)
- [Marvin HPC cluster @ University of Bonn](https://www.hpc.uni-bonn.de/en/systems/marvin)

```sh
# Download TSMP2
git clone https://github.com/HPSCTerrSys/TSMP2.git
cd TSMP2

# Build eCLM
./build_tsmp2.sh --eCLM
```


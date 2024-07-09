# eCLM

[![CI](https://github.com/HPSCTerrSys/eCLM/actions/workflows/CI.yml/badge.svg)](https://github.com/HPSCTerrSys/eCLM/actions/workflows/CI.yml)
[![status: alpha](https://img.shields.io/badge/status-alpha-yellow)](https://github.com/HPSCTerrSys/eCLM)

eCLM is based from [Community Land Model 5.0 (CLM5.0)]. It has the same modelling capabilities as CLM5 but with a more simplified infrastructure for build and namelist generation. The build system is handled entirely by CMake and namelists are generated through a small set of Python scripts. Only Fortran source codes necessary for a functional land model simulation were imported from CLM5. 

Unlike CLM5, there are no built-in batch scripts in eCLM. It is up to system maintainers or users to craft their own workflows by combining the basic tools in this repo plus the native tools in their respective platforms.

> [!WARNING]
> eCLM is still experimental and has been undergoing extensive testing. Use it at your own risk!

## Usage

Please check the documentation at https://hpscterrsys.github.io/eCLM

[Community Land Model 5.0 (CLM5.0)]: https://github.com/ESCOMP/CTSM/tree/release-clm5.0

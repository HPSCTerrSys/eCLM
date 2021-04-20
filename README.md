# eCLM
[![status: alpha](https://img.shields.io/badge/status-alpha-yellow)](https://github.com/HPSCTerrSys/eCLM)

eCLM is based from [Community Land Model 5.0 (CLM5.0)]. It has the same modelling capabilities as CLM5 but with a more simplified infrastructure for build and namelist generation. The build system is handled entirely by CMake and namelists are generated through a small set of Python scripts. Only Fortran source codes necessary for a functional land model simulation were imported from CLM5. 

Unlike CLM5, there are no built-in batch scripts in eCLM. It is up to system maintainers or users to craft their own workflows by combining the basic tools in this repo plus the native tools in their respective platforms. If you are a user in [IBG-3], you may want to check out the [eCLM-JSC] repo.

### Status

eCLM has only been lightly tested; so far it could run a single-point and a regional case in Germany. Still, more work has to be done to ensure the correctness of the build process and the generated namelists. A user-friendly and lightweight approach to model configuration also has to be developed. *eCLM is still in alpha version and would not be ready for production runs anytime soon*.

[Community Land Model 5.0 (CLM5.0)]: https://github.com/ESCOMP/CTSM/tree/release-clm5.0
[IBG-3]: https://www.fz-juelich.de/ibg/ibg-3/EN/Home/home_node.html
[eCLM-JSC]: https://icg4geo.icg.kfa-juelich.de/ModelSystems/clm/eclm-jsc
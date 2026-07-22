# eCLM

[![helmholtz rsd](https://img.shields.io/badge/helmholtz.software-eclm-00a3e3)](https://helmholtz.software/software/eclm)
[![latest tag](https://badgen.net/github/tag/HPSCTerrSys/eCLM)](https://github.com/HPSCTerrSys/eCLM/tags)

eCLM is based from [Community Land Model 5.0 (CLM5.0)]. It has the same modelling capabilities as CLM5 but with a more simplified infrastructure for build and namelist generation. The build system is handled entirely by CMake and namelists are generated through a small set of Python scripts. Only Fortran source codes necessary for a functional land model simulation were imported from CLM5. 

Unlike CLM5, there are no built-in batch scripts in eCLM. It is up to system maintainers or users to craft their own workflows by combining the basic tools in this repo plus the native tools in their respective platforms.

## More info

- **Documentation**: https://hpscterrsys.github.io/eCLM
- **Contributions**: Mainly via [issues] and [pull requests]. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.
- **Contact**: You can send your general inquiries on our [eCLM Matrix channel].

[Community Land Model 5.0 (CLM5.0)]: https://github.com/ESCOMP/CTSM/tree/release-clm5.0
[issues]: https://github.com/HPSCTerrSys/eCLM/issues
[pull requests]: https://github.com/HPSCTerrSys/eCLM/pulls
[CONTRIBUTING.md]: CONTRIBUTING.md
[eCLM Matrix channel]: https://matrix.to/#/!UooUiDWmcOwQXoktJt:fz-juelich.de?via=fz-juelich.de&via=matrix.org

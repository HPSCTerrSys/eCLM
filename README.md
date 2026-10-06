# eCLM

[![helmholtz rsd](https://img.shields.io/badge/helmholtz.software-eclm-00a3e3)](https://helmholtz.software/software/eclm)
[![latest tag](https://badgen.net/github/tag/HPSCTerrSys/eCLM)](https://github.com/HPSCTerrSys/eCLM/tags)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17967419.svg)](https://doi.org/10.5281/zenodo.17967419)

eCLM is based from [Community Land Model 5.0 (CLM5.0)]. It has the same modelling capabilities as CLM5 but with a more simplified infrastructure for build and namelist generation. The build system is handled entirely by CMake and namelists are generated through a small set of Python scripts. Only Fortran source codes necessary for a functional land model simulation were imported from CLM5. 

Unlike CLM5, there are no built-in batch scripts in eCLM. It is up to system maintainers or users to craft their own workflows by combining the basic tools in this repo plus the native tools in their respective platforms.

## Documentation

Check our online docs at https://hpscterrsys.github.io/eCLM

## Contributing

Feel free to post your questions and problems via the [issue tracker]. We also welcome [pull requests]. Before opening an issue or a pull request, please review our **[contribution guidelines]**.

For general inquiries, leave us a message on our [eCLM Matrix channel].

## Citing

If you use this software, please cite:

```bibtex
@software{eclm,
 author = {Rigor, Paul and Poll, Stefan and González-Nicolás, Ana and Keller, Johannes and van Hulten, Marco and Caviedes-Voullieme, Daniel and Hendricks-Franssen, Harrie-Jan and Goergen, Klaus and Kollet, Stefan},
  title = {enCore Community Land Model (eCLM)},
   year = {2025},
    url = {https://github.com/HPSCTerrSys/eCLM},
    doi = {10.5281/ZENODO.17967419}
}
```

[Community Land Model 5.0 (CLM5.0)]: https://github.com/ESCOMP/CTSM/tree/release-clm5.0
[issue tracker]: https://github.com/HPSCTerrSys/eCLM/issues
[pull requests]: https://github.com/HPSCTerrSys/eCLM/pulls
[contribution guidelines]: CONTRIBUTING.md
[eCLM Matrix channel]: https://matrix.to/#/!UooUiDWmcOwQXoktJt:fz-juelich.de?via=fz-juelich.de&via=matrix.org

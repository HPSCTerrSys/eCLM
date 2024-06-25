# eCLM

eCLM is based on version 5.0 of the Community Land Model (CLM5) with simplified infrastructure for build and namelist generation. The build system is handled entirely by Cmake and namelists are generated through a small set of Python scripts. Similar to CLM5, eCLM is forced with meteorological data and uses numerous input streams on soil properties, land cover and land use, as well as complex parameter sets on crop phenology, and plant hydraulics for simulations.

# The Community Land Model

The Community Land Model is the land model for the Community Earth System Model (CESM). It focuses on modeling the land as the critical interface through which humanity affects, adapts to, and mitigates global environmental change. It includes a comprehensive representation of land biogeophysics, hydrology, plant physiology, biogeochemistry, anthropogenic land use, and ecosystem dynamics across a variety of spatial and temporal scales. The central theme is that terrestrial ecosystems, through their cycling of energy, water, chemical elements, and trace gases, are important determinants of climate.
The model represents several aspects of the land surface including surface heterogeneity and consists of components or submodels related to land biogeophysics, the hydrologic cycle, biogeochemistry, human dimensions, and ecosystem dynamics. Specific processes that are represented include:

-	Vegetation composition, structure, and phenology
-	Absorption, reflection, and transmittance of solar radiation
-	Absorption and emission of longwave radiation
-	Momentum, sensible heat (ground and canopy), and latent heat (ground evaporation, canopy evaporation, transpiration) fluxes
-	Heat transfer in soil and snow including phase change
-	Canopy hydrology (interception, throughfall, and drip)
-	Snow hydrology (snow accumulation and melt, compaction, water transfer between snow layers)
-	Soil hydrology (surface runoff, infiltration, redistribution of water within the column, sub-surface drainage, groundwater)
-	Plant hydrodynamics
-	Stomatal physiology and photosynthesis
-	Lake temperatures and fluxes
-	Dust deposition and fluxes
-	Routing of runoff from rivers to ocean
-	Volatile organic compounds emissions
-	Urban energy balance and climate
-	Carbon-nitrogen cycling
-	Dynamic landcover change
-	Land management including crops and crop management and wood harvest
-	Ecosystem Demography (FATES, optional)

```{figure} ../images/CLM5_processes.png
:height: 400px
:name: fig1

Figure 1: Overview of land biogeophysical, biogeochemical and landscape processes simulated by CLM. Adapted from [Lawrence et al. (2011)](https://doi.org/10.1029/2011MS00045).
```
<p>

Each time step the model solves the surface energy balance, water balance, and carbon exchange. Submodels of CLM include biophysics and biogeochemistry. It represents land surface heterogeneity through a subgrid tiling structure and different plant functional types that have unique parameters in terms of optical properties, morphology, photosynthesis. It can be run with prescribed vegetation states (satellite phenology mode) or prognostic vegetation states and biogeochemistry (BGC mode).

```{figure} ../images/CLM5_subgrid_structure.png
:height: 400px
:name: fig2

Figure 2: Configuration of the CLM subgrid hierarchy. Adapted from: http://www.cesm.ucar.edu/.
```
<p>

More background information on CLM (and it’s latest release CLM5) including documentation and publications can be found [here](https://www.cesm.ucar.edu/models/clm).
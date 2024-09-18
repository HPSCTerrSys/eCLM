# Modification of the surface and domain file


## Handling negative longitudes and the landmask

eCLM does not accept negative longitudes for the surface and domain file. In case you used a grid file to create your SCRIP grid file which used negative longitudes (instead of creating it through the `mkscripgrid.py` script), these need to be converted into the 0 to 360 degree system used by eCLM. You can use the `mod_domain.sh` script in the main directory `eCLM_static_file_workflow` to do this.

Before executing the script adapt the paths to your [surface file](https://hpscterrsys.github.io/eCLM/users_guide/case_creation/4_create_surface_file.html#create-surface-file) and [domain file](https://hpscterrsys.github.io/eCLM/users_guide/case_creation/3_create_domain_file.html#create-domain-file).

`mod_domain.sh` also replaces the `mask` and `frac` variables of your domain file with the information from a `landmask_file` (this `landmask.nc` file should contain the 2D variables `mask` and `frac` that contain your landmask (value 1 for land and 0 for ocean)). This step should not be necessary as you already swapped the `domain.lnd.*.nc` and `domain.ocn.*.nc` file when creating them. However, for some domains (e.g. the ICON grid) the mask from the rawdata may not correctly represent your landmask. Additionally, if you want to replace the surface parameters with higher resolution data (see below), you may need to update the landmask as well to match your surface parameters (e.g. coast lines may have changed).

## Modifying surface parameters

You may want to modify the default soil, landuse or other land surface data on the surface file if you have measurements or a different data source of higher resolution or similar available. 
You can do this by accessing the relevant variables on the surface file. 

Variables you want to modify may include (non-exhaustive list):

Soil:
- `PCT_SAND`: percentage sand at soil levels (10 levels are considered)
- `PCT_CLAY`: percentage clay at soil levels (10 levels are considered)
- `ORGANIC`: organic matter density at soil levels (10 levels are considered)

Landuse at the landunit level ([Fig. 2](https://hpscterrsys.github.io/eCLM/users_guide/introduction_to_eCLM/introduction.html#fig2)): 
- `PCT_NATVEG`: total percentage of natural vegetation landunit
- `PCT_CROP`: total percentage of crop landunit
- `PCT_URBAN`: total percentage of urban landunit
- `PCT_LAKE`: total percentage of lake landunit
- `PCT_GLACIER`: total percentage of glacier landunit
- `PCT_WETLAND`: total percentage of wetland landunit

Types of crop and natural vegetation at the patch level ([Fig. 2](https://hpscterrsys.github.io/eCLM/users_guide/introduction_to_eCLM/introduction.html#fig2)):

- `PCT_NAT_PFT`: percent plant functional type (PFT) on the natural veg landunit (% of landunit) (15 PFTs are considered see <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/tech_note/Ecosystem/CLM50_Tech_Note_Ecosystem.html#vegetation-composition" target="_blank">here</a> for a list of PFTs)
- `PCT_CFT`: percent crop functional type (CFT) on the crop landunit (% of landunit) (2 CFTs are considered in SP mode, 64 CFTs are considered in BGC mode, see <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/tech_note/Crop_Irrigation/CLM50_Tech_Note_Crop_Irrigation.html#crop-plant-functional-types" target="_blank">here</a> for a list of CFTs)

Land fraction:
- `LANDFRAC_PFT`: land fraction from PFT dataset
- `PFTDATA_MASK`: land mask from pft dataset, indicative of real/fake points
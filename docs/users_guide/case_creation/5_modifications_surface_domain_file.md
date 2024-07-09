# Modification of the surface and domain file

```{warning}
There is ongoing clarification for this section.
```

The created surface and domain file have negative longitudes that eCLM/CLM5 does not accept and inherently has no landmask. To modify the longitudes (into a 360 degree system) and to add a landmask, you can use the `mod_domain.sh` script in the main directory `eCLM_static_file_workflow`.

Before executing the script adapt the paths to your [surface file](https://hpscterrsys.github.io/eCLM/users_guide/case_creation/4_create_surface_file.md), [domain file](https://hpscterrsys.github.io/eCLM/users_guide/case_creation/4_create_domain_file.md) and landmask file (this file should contain a 2D variable called `mask` that contains your landmask (value 1 for land and 0 for ocean)).

## Modifying surface parameters

You may want to modify the default soil, landuse or other land surface data on the surface file if you have measurements or a different data source of higher resolution or similar available. 
You can do this by accessing the relevant variables on the surface file. 

These may include:

Soil:
- PCT_SAND: percentage sand at soil levels (10 levels are considered)
- PCT_CLAY: percentage clay at soil levels (10 levels are considered)
- ORGANIC: organic matter density at soil levels (10 levels are considered)

Landuse at the landunit level ([Fig. 2](https://hpscterrsys.github.io/eCLM/users_guide/introduction_to_eCLM/introduction.html#fig2)): 
- PCT_NATVEG: total percentage of natural vegetation landunit
- PCT_CROP: total percentage of crop landunit
- PCT_URBAN: total percentage of urban landunit
- PCT_LAKE: total percentage of lake landunit
- PCT_GLACIER: total percentage of glacier landunit
- PCT_WETLAND: total percentage of wetland landunit

Types of crop and natural vegetation at the patch level ([Fig. 2](https://hpscterrsys.github.io/eCLM/users_guide/introduction_to_eCLM/introduction.html#fig2)):

- PCT_NAT_PFT: percent plant functional type (PFT) on the natural veg landunit (% of landunit) (15 PFTs are considered see <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/tech_note/Ecosystem/CLM50_Tech_Note_Ecosystem.html#vegetation-composition" target="_blank">here</a> for a list of PFTs)
- PCT_CFT: percent crop functional type (CFT) on the crop landunit (% of landunit) (2 CFTs are considered in SP mode, 64 CFTs are considered in BGC mode, see <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/tech_note/Crop_Irrigation/CLM50_Tech_Note_Crop_Irrigation.html#crop-plant-functional-types" target="_blank">here</a> for a list of CFTs)
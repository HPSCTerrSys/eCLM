"""
Work in progress. Plenty of other user options hasn't been covered yet. 
Default datm_in values are based from these files:

[namelist_definition_drv_flds.xml]: https://github.com/ESMCI/cime/blob/cime5.6.33/src/drivers/mct/cime_config/namelist_definition_drv_flds.xml
[config_component.xml]: https://github.com/ESMCI/cime/blob/cime5.6.33/src/drivers/mct/cime_config/config_component.xml
"""
from pathlib import Path
from ..structures import drv_flds_in

__all__ = ['build_drv_flds_in']

def build_drv_flds_in(opts: dict = None, nl: dict = None, nl_file: str = None):
    
    _nl = drv_flds_in()

    with _nl.megan_emis_nl as n:
        n.megan_factors_file = nl["megan_factors_file"]
        n.megan_specifier = ["ISOP = isoprene",
                             "C10H16 = pinene_a + carene_3 + thujene_a",
                             "CH3OH = methanol",
                             "C2H5OH = ethanol",
                             "CH2O = formaldehyde",
                             "CH3CHO = acetaldehyde",
                             "CH3COOH = acetic_acid",
                             "CH3COCH3 = acetone"]

    # Write to file
    if nl_file: 
        _nl.write(nl_file)
        print(f"Generated {Path(nl_file).name}")

if __name__ == "__main__":
    """
    For testing purposes. To run gen_datm_in.py, 
    directly, execute it via Python script mode:
    
    $ cd <parent folder of clm5nl>
    $ python3 -m clm5nl.generators.gen_drv_flds_in   
    """
    opts, nl = {}, {}
    nl["megan_factors_file"] = "/p/scratch/cjicg41/jicg4177/cesm/inputdata/atm/cam/chem/trop_mozart/emis/megan21_emis_factors_78pft_c20161108.nc" # L78

    build_drv_flds_in(opts, nl, "drv_flds_in_test")
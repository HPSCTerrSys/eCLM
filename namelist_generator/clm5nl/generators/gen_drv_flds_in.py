"""
Work in progress. Plenty of other user options hasn't been covered yet. 
Default datm_in values are based from these files:

[namelist_definition_drv_flds.xml]: https://github.com/ESMCI/cime/blob/cime5.6.33/src/drivers/mct/cime_config/namelist_definition_drv_flds.xml
[config_component.xml]: https://github.com/ESMCI/cime/blob/cime5.6.33/src/drivers/mct/cime_config/config_component.xml
"""
from pathlib import Path
from ..structures import drv_flds_in

__all__ = ['build_drv_flds_in']
_opts = {}
_nl = drv_flds_in()

def build_drv_flds_in(opts: dict = None, nl_file: str = "drv_flds_in"):
    
    global _opts, _nl
    _opts = opts
    _user_nl = opts.get("user_nl", {})
    _nl = drv_flds_in()

    _opts["drydep"] = opts.get("drydep", False)
    _opts["fire_emis"] = opts.get("fire_emis", False)

    setup_logic_dry_deposition()
    setup_logic_fire_emis()
    setup_logic_megan()

    # Write to file
    if nl_file and Path(nl_file).name.strip() != "":
        _nl.write(nl_file)
        print(f"--> Generated {Path(nl_file).name}")

def setup_logic_dry_deposition():
    with _nl.drydep_inparm as n:
        if _opts["drydep"]:
            n.drydep_list = ["O3", "NO2", "HNO3", "NO", "HO2NO2", "CH3OOH", "CH2O", "CO", "H2O2", "CH3COOOH", 
                                                    "PAN", "MPAN", "C2H5OOH", "ONIT", "POOH", "C3H7OOH", "ROOH", "CH3COCHO", 
                                                    "CH3COCH3", "Pb", "ONITR", "MACROOH", "XOOH", "ISOPOOH", "CH3OH", "C2H5OH", 
                                                    "CH3CHO", "GLYALD", "HYAC", "HYDRALD", "ALKOOH", "MEKOOH", "TOLOOH", "TERPOOH", 
                                                    "CH3COOH", "CB1", "CB2", "OC1", "OC2", "SOA", "SO2", "SO4", "NH3", "NH4NO3"]
            n.drydep_method = "xactive_lnd"
        else:
            if (not n.drydep_list is None or not n.drydep_method is None):
                error("drydep_list or drydep_method defined, but drydep option NOT set")
    
def setup_logic_fire_emis():
    with _nl.fire_emis_nl as n:
        if _opts["fire_emis"]:
            n.fire_emis_factors_file = "lnd/clm2/firedata/fire_emis_factors_c140116.nc"
            n.fire_emis_specifier = ["bc_a1 = BC", "pom_a1 = 1.4*OC", "SO2 = SO2"]
        else:
            if (not n.fire_emis_elevated is None or
                not n.fire_emis_factors_file is None or
                not n.fire_emis_specifier is None):
                error("fire_emission setting defined: fire_emis_elevated, fire_emis_factors_file, or fire_emis_specifier, but fire_emis option NOT set")

def setup_logic_megan():
    # TODO: use_megan should depend on 'clm_accelerated_spinup' and
    # 'use_fates' parameters from lnd_in.
    #
    # if _opts["megan"] == "default":
    #     use_megan = not _opts["clm_accelerated_spinup"]
    # else:
    #     use_megan = bool(_opts["megan"])
    use_megan = True
    with _nl.megan_emis_nl as n:
        if use_megan:
            # if _nl.clm_inparm.use_fates:
            #     error("MEGAN can NOT be on when ED is also on. Use the '-no-megan' option when '-bgc fates' is activated")
            n.megan_specifier = ["ISOP = isoprene",
                        "C10H16 = pinene_a + carene_3 + thujene_a",
                        "CH3OH = methanol",
                        "C2H5OH = ethanol",
                        "CH2O = formaldehyde",
                        "CH3CHO = acetaldehyde",
                        "CH3COOH = acetic_acid",
                        "CH3COCH3 = acetone"]
            if _opts["megan_factors_file"] is not None:
                n.megan_factors_file = _opts["megan_factors_file"]
            else:
                n.megan_factors_file = "atm/cam/chem/trop_mozart/emis/megan21_emis_factors_78pft_c20161108.nc"
        else:
            if (not n.megan_factors_file is None or n.megan_specifier is None):
                error("megan_specifier or megan_factors_file defined, but megan option NOT set")


if __name__ == "__main__":
    """
    For testing purposes. To run gen_datm_in.py, 
    directly, execute it via Python script mode:
    
    $ cd <parent folder of clm5nl>
    $ python3 -m clm5nl.generators.gen_drv_flds_in   
    """
    opts, user_nl = {}, {}
    opts["drydep"] = False
    opts["fire_emis"] = False
    opts["megan"] = True
    opts["megan_factors_file"] = "/p/scratch/nrw_test_case/megan21_emis_factors_78pft_c20161108.nc"

    build_drv_flds_in(opts, user_nl, "drv_flds_in_test")
"""drv_flds_in namelist
"""
from typing import List
from .namelist import Namelist, namelist_group , namelist_item

class drv_flds_in(Namelist):

    @namelist_group
    class drydep_inparm():

        @namelist_item
        def drydep_list(self) -> List[str]:
            """
            List of species that undergo dry deposition.
            """
            pass

        @namelist_item
        def drydep_method(self) -> str:
            """
            Where dry deposition is calculated (from land, atmosphere, or from a table)
            This specifies the method used to calculate dry
            deposition velocities of gas-phase chemical species.  The available methods
            are:
            'table'       - prescribed method in CAM
            'xactive_atm' - interactive method in CAM
            'xactive_lnd' - interactive method in CLM
            """
            pass

    @namelist_group
    class fire_emis_nl():

        @namelist_item
        def fire_emis_elevated(self) -> bool:
            """
            If ture fire emissions are input into atmosphere as elevated forcings.
            Otherwise they are treated as surface emissions.
            Default: TRUE
            """
            pass
        
        @namelist_item
        def fire_emis_factors_file(self) -> str:
            """
            File containing fire emissions factors.
            Default: none
            """
            pass

        @namelist_item
        def fire_emis_specifier(self) -> List[str]:
            """
            Fire emissions specifier.
            Default: none
            """
            pass

    @namelist_group
    class megan_emis_nl():

        @namelist_item
        def megan_factors_file(self) -> str:
            """
            File containing MEGAN emissions factors. Includes the list of MEGAN compounds that can be
            used in the Comp_Name variable on the file.
            """
            pass

        @namelist_item
        def megan_specifier(self) -> List[str]:
            """
            MEGAN specifier. This is in the form of: Chem-compound = megan_compound(s)
            where megan_compound(s) can be the sum of megan compounds with a "+" between them.
            In each equation, the item to the left of the equal sign is a CAM chemistry compound, the
            items to the right are compounds known to the MEGAN model (single or combinations).
            For example: megan_specifier = 'ISOP = isoprene', 'C10H16 = pinene_a + carene_3 + thujene_a'
            """
            pass
        
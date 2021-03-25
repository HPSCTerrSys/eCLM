"""
PIO namelist
"""
from typing import List
from .namelist import Namelist, namelist_group , namelist_item

class modelio_in(Namelist):

    @namelist_group
    class modelio():

        @namelist_item
        def diri(self) -> str:
            """
            input directory (no longer needed)
            """
            pass

        @namelist_item
        def diro(self) -> str:
            """
            directory for output log files
            """
            pass

        @namelist_item
        def logfile(self) -> str:
            """
            name of component output log file
            """
            pass

    @namelist_group
    class pio_inparm():

        @namelist_item
        def pio_netcdf_format(self) -> str:
            """
            format of netcdf files created by pio, ignored if
            PIO_TYPENAME is netcdf4p or netcdf4c.  64bit_data only
            supported in netcdf 4.4.0 or newer

            valid values: classic,64bit_offset,64bit_data
            """
            pass

        @namelist_item
        def pio_numiotasks(self) -> int:
            """
            number of io tasks in pio used generically, component based value takes precedent.
            """
            pass

        @namelist_item
        def pio_rearranger(self) -> int:
            """
            Rearranger method for pio 1=box, 2=subset.
            """
            pass

        @namelist_item
        def pio_root(self) -> int:
            """
            io task root in pio used generically, component based value takes precedent.
            """
            pass

        @namelist_item
        def pio_stride(self) -> int:
            """
            stride of tasks in pio used generically, component based value takes precedent.
            """
            pass

        @namelist_item
        def pio_typename(self) -> str:
            """
            io type in pio used generically, component based value takes precedent.
            valid values: netcdf, pnetcdf, netcdf4p, netcdf4c, default
            """
            pass
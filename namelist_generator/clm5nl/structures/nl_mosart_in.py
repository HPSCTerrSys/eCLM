"""
MOSART namelist
"""
from typing import List
from .namelist import Namelist, namelist_group , namelist_item

class mosart_in(Namelist):

    @namelist_group
    class mosart_inparm():

        @namelist_item
        def bypass_routing_option(self) -> str:
            """
            Method for bypassing routing model.
            """
            pass

        @namelist_item
        def coupling_period(self) -> int:
            """
            MOSART coupling period to driver (sec).
            Can ONLY be set by modifying the value of the xml variable ROF_NCPL in env_run.xml.
            """
            pass

        @namelist_item
        def decomp_option(self) -> str:
            """
            Decomposition Option for mosart
            """
            pass

        @namelist_item
        def delt_mosart(self) -> int:
            """
            MOSART time step (sec). Default: 3600 Internal mosart timestep,
            will be adjusted down to be integer multiple of coupling_period if
            necessary
            """
            pass

        @namelist_item
        def do_rtm(self) -> bool:
            """
            If .true., turn on mosart river routing
            If the value of the xml variable ROF GRID in env_build.xml is set to 'null', then
            the MOSART build-namelist will set do_mosart to .false.
            If do_mosart is set to .false., then MOSART will send a flag of rof_prognostic = .false.
            back to the coupler on initialization.
            """
            pass

        @namelist_item
        def do_rtmflood(self) -> bool:
            """
            If .true., turn on mosart flooding back to clm
            Note that mosart flood is not supported in CESM1.1
            """
            pass

        @namelist_item
        def finidat_rtm(self) -> str:
            """
            Full pathname of initial rtm file 
            """
            pass

        @namelist_item
        def frivinp_rtm(self) -> str:
            """
            Full pathname of input datafile for RTM.
            """
            pass

        @namelist_item
        def ice_runoff(self) -> bool:
            """
            Default: .true.
            If .true., river runoff will be split up into liquid and ice streams,
            otherwise ice runoff will be zero and all runoff directed to liquid
            stream.
            """
            pass

        @namelist_item
        def qgwl_runoff_option(self) -> str:
            """
            Method for handling of qgwl runoff inputs.
            """
            pass

        @namelist_item
        def rtmhist_fexcl1(self) -> str:
            """
            Fields to exclude from history tape series 1.
            """
            pass

        @namelist_item
        def rtmhist_fexcl2(self) -> str:
            """
            Fields to exclude from history tape series 2.
            """
            pass

        @namelist_item
        def rtmhist_fexcl3(self) -> str:
            """
            Fields to exclude from history tape series 3.
            """
            pass

        @namelist_item
        def rtmhist_fincl1(self) -> str:
            """
            Fields to add to history tape series  1.
            """
            pass

        @namelist_item
        def rtmhist_fincl2(self) -> str:
            """
            Fields to add to history tape series  2.
            """
            pass

        @namelist_item
        def rtmhist_fincl3(self) -> str:
            """
            Fields to add to history tape series  3.
            """
            pass

        @namelist_item
        def rtmhist_mfilt(self) -> int:
            """
            Per tape series  maximum number of time samples.
            """
            pass

        @namelist_item
        def rtmhist_ndens(self) -> int:
            """
            Per tape series  history file density (i.e. output precision) 
            1=double precision, 2=single precision (NOT working)
            """
            pass

        @namelist_item
        def rtmhist_nhtfrq(self) -> int:
            """
            Per tape series history write frequency. 
            positive means in time steps,  0=monthly, negative means hours
            (i.e. 24 means every 24 time-steps and -24 means every day
            """
            pass

        @namelist_item
        def smat_option(self) -> str:
            """
            sparse matrix mct setting.  Xonly is bfb on different pe counts,
            opt and Yonly might involve partial sums
            """
            pass
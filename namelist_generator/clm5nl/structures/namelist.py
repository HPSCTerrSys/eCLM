from collections import OrderedDict
from .utils import nml2str, nmlGroup2str

class Namelist(object):
    def __init__(self, nl_obj: dict = None):
        self._name = type(self).__name__
        if nl_obj is None:
            self._nl = OrderedDict()
        else:
            self._nl = nl_obj

    def __iter__(self):
        return self._nl.__iter__()

    def __len__(self):
        acc = 0
        for v in self._nl.values():
            acc += len(v)
        return acc

    def keys(self):
        return self._nl.keys()

    def __str__(self):
        return nml2str(self._nl)

    def write(self, file_path, grp_names: list = []):
        with open(file_path, "w") as f:
            f.write(nml2str(self._nl, grp_names=grp_names))

class NamelistGroupMixin(object):
    def __init__(self, valid_params: list[str]):
        self._group_name = type(self).__name__
        self._parent: Namelist = None
        self._valid_params = valid_params

    def _get_param(self, key):
        if self._group_name in self._parent._nl:
            return self._parent._nl[self._group_name].get(key, None)
        else:
            return None
        
    def _set_param(self, key, value):
        if not self._group_name in self._parent._nl: self._parent._nl[self._group_name] = OrderedDict()
        self._parent._nl[self._group_name][key] = value

    def _del_param(self, key):
        if self._group_name in self._parent._nl:
           del self._parent._nl[self._group_name][key]

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def __iter__(self):
        if self._group_name in self._parent._nl:
            return self._parent._nl[self._group_name].__iter__()
        else:
            return {}.__iter__()

    def __contains__(self, item):
        return item in self._valid_params

    def __len__(self):
        if self._group_name in self._parent._nl:
            return len(self._parent._nl[self._group_name])
        else:
            return 0 

    def __str__(self):
        return nmlGroup2str(self._group_name, {p:self._get_param(p) for p in self._valid_params})

class namelist_group():
    def __init__(self, nl_grp):
        self._group_type = type(nl_grp.__name__, (nl_grp, NamelistGroupMixin), {})
        self._group = None
        self._params = [p for p in dir(nl_grp) if not p.startswith('_')]

    def __get__(self, nl_obj, objtype):
        if self._group is None: self._group = self._group_type(valid_params = self._params)
        self._group._parent = nl_obj
        return self._group

class namelist_item(object):
    def __init__(self, func):
        self._param_name = func.__name__.lower()
        self.__doc__ = func.__doc__

    def __get__(self, nl_grp, objtype):
        return nl_grp._get_param(self._param_name)

    def __set__(self, nl_grp, value):
        nl_grp._set_param(self._param_name, value)

    def __delete__(self, nl_grp):
        nl_grp._del_param(self._param_name)
from collections import OrderedDict
from .utils import nl_to_str

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
        return nl_to_str(self._nl)

    def write(self, nml_path):
        with open(nml_path, "w") as f:
            f.write(nl_to_str(self._nl))

class NamelistGroupMixin(object):
    def __init__(self):
        self._group_name = type(self).__name__
        self._parent: Namelist = None

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
        if self._group_name in self._parent._nl:
            return (item in self._parent._nl[self._group_name])
        else:
            return False

    def __len__(self):
        if self._group_name in self._parent._nl:
            return len(self._parent._nl[self._group_name])
        else:
            return 0 

    def __str__(self):
        return nl_to_str(self._parent._nl, self._group_name)

    def items(self):
        if self._group_name in self._parent._nl:
            return self._parent._nl[self._group_name].items()
        else:
            return {}.items()

class namelist_group():
    def __init__(self, nl_grp):
        self._group_type = type(nl_grp.__name__, (nl_grp, NamelistGroupMixin), {})
        self._group = None
        #self._nl_grp = ng()

    def __get__(self, nl_obj, objtype):
        if self._group is None: self._group = self._group_type()
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
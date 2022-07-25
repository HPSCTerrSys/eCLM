from collections import OrderedDict
from .utils import nml2str, nmlGroup2str

class Namelist(object):
    def __init__(self, nl_obj: dict = None):
        self._name = type(self).__name__
        self._valid_params = {}
        if nl_obj is None:
            self._nl = OrderedDict()
        else:
            self._nl = nl_obj

    def __iter__(self):
        return self._nl.__iter__()

    def __len__(self):
        param_count = 0
        for nl_group in self._nl.values():
            param_count += len(nl_group)
        return param_count

    def __getitem__(self, key):
        if key in self._valid_params:
            return self._nl[self._valid_params[key]].get(key, None)
        else:
            raise KeyError(f"'{key}' is not a valid {self._name} parameter.")

    def __setitem__(self, key, value):
        if key in self._valid_params:
            self._nl[self._valid_params[key]][key] = value
        else:
            raise KeyError(f"'{key}' is not a valid {self._name} parameter.")

    def __contains__(self, item):
        return item in self._valid_params.keys()

    def _update_valid_params(self, valid_params: dict):
        self._valid_params.update(valid_params)

    def keys(self):
        return self._nl.keys()

    def update(self, other=None, **kwargs):
        if other is not None:
            for k, v in other.items():
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def __str__(self):
        return nml2str(self._nl)

    def write(self, file_path, grp_names: list = []):
        with open(file_path, "w") as f:
            f.write(nml2str(self._nl, grp_names=grp_names))

class NamelistGroupMixin(object):
    def __init__(self, parent: Namelist, valid_params: dict):
        self._group_name = type(self).__name__
        self._parent = parent
        self._valid_params = valid_params
        self._parent._update_valid_params(valid_params)

    def __getitem__(self, key):
        if self._group_name in self._parent._nl:
            return self._parent._nl[self._group_name].get(key, None)
        else:
            return None
        
    def __setitem__(self, key, value):
        if not self._group_name in self._parent._nl: 
            self._parent._nl[self._group_name] = OrderedDict()
        self._parent._nl[self._group_name][key] = value

    def __delitem__(self, key):
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
        return item in self._valid_params.keys()

    def __len__(self):
        if self._group_name in self._parent._nl:
            return len(self._parent._nl[self._group_name])
        else:
            return 0 

    def __str__(self):
        return nmlGroup2str(self._group_name, {p:self[p] for p in self._valid_params})

class namelist_group():
    def __init__(self, nl_grp):
        self._group_type = type(nl_grp.__name__, (nl_grp, NamelistGroupMixin), {})
        self._group = None
        self._params = {p:nl_grp.__name__ for p in dir(nl_grp) if not p.startswith('_')}

    def __get__(self, nl_obj, objtype):
        if self._group is None: 
            self._group = self._group_type(parent = nl_obj, valid_params = self._params)
        return self._group

class namelist_item(object):
    def __init__(self, func):
        self._param_name = func.__name__.lower()
        self.__doc__ = func.__doc__

    def __get__(self, nl_grp, objtype):
        return nl_grp[self._param_name]

    def __set__(self, nl_grp, value):
        nl_grp[self._param_name] = value

    def __delete__(self, nl_grp):
        del nl_grp[self._param_name]
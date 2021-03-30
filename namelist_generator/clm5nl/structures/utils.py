from collections import OrderedDict
from itertools import filterfalse
from io import StringIO

def nml2str(nl: dict, ordered_grp_names: list = []) -> str:
    """
    Converts a namelist object (dict) into a Fortran namelist (string).
    """
    nl_str = StringIO()
    sort_grp_a2z = (len(ordered_grp_names) == 0)

    if sort_grp_a2z:
        nl_sorted = OrderedDict(sorted(nl.items(), key=lambda t: t[0]))
        [nmlGroup2str(grp, params, nl_str) for grp, params in nl_sorted.items()]
    else:
        for grp in ordered_grp_names:
            nmlGroup2str(grp, nl[grp] if grp in nl else {}, nl_str)

        # Add groups not included in ordered_grp_names
        missing_groups = filterfalse(lambda g : g in ordered_grp_names, nl.keys())
        [nmlGroup2str(grp, nl[grp], nl_str) for grp in missing_groups]

    return nl_str.getvalue()

def nmlGroup2str(grp_name: str, params: dict, buffer: StringIO = None):
    """
    Converts a namelist group (dict) into a Fortran namelist (string).
    """
    noBuffer = (buffer is None)
    if noBuffer: buffer = StringIO()

    p = OrderedDict(sorted(params.items(), key=lambda t: t[0]))
    buffer.write(f"&{grp_name}\n")
    for key, value in p.items():
        buffer.write(f" {key} = {py2fortran(value)}\n")
    buffer.write("/\n")

    if noBuffer: return buffer.getvalue()

def py2fortran(obj) -> str:
    """
    Converts a Python type to its equivalent Fortran syntax.
    """
    if isinstance(obj, bool):
        value = ".true." if obj else ".false."
    elif isinstance(obj, str):
        value = "'{}'".format(obj)
    elif isinstance(obj, list):
        if isinstance(obj[0], str):
            value = ", ".join("'{}'".format(s) for s in obj)
        else:
            value = ", ".join(str(s) for s in obj)
    else:
        value = str(obj)
    return value
from collections import OrderedDict
from itertools import filterfalse
from io import StringIO

NL_COLUMN_WIDTH_MAX = 60

def nml2str(nl: dict, grp_names: list = [], fill_missing_groups: bool = True) -> str:
    """
    Converts a namelist object (dict) into a Fortran namelist (string).
    """
    nl_str = StringIO()
    sort_grp_a2z = (len(grp_names) == 0)

    if sort_grp_a2z:
        nl_sorted = OrderedDict(sorted(nl.items(), key=lambda t: t[0]))
        [nmlGroup2str(grp, params, nl_str) for grp, params in nl_sorted.items()]
    else:
        for grp in grp_names:
            nmlGroup2str(grp, nl[grp] if grp in nl else {}, nl_str)

        # Add groups not included in grp_names
        if fill_missing_groups:
            missing_groups = filterfalse(lambda g : g in grp_names, nl.keys())
            [nmlGroup2str(grp, nl[grp], nl_str) for grp in missing_groups]

    return nl_str.getvalue()

def nmlGroup2str(grp_name: str, params: dict, buffer: StringIO = None):
    """
    Converts a namelist group (dict) into a Fortran namelist (string).
    """
    noBuffer = (buffer is None)
    if noBuffer: buffer = StringIO()

    sorted_params = OrderedDict(sorted(params.items(), key=lambda t: t[0]))
    buffer.write(f"&{grp_name}\n")
    for key, value in sorted_params.items():
        line = f" {key} = {py2fortran(value)}"
        if len(line) >= NL_COLUMN_WIDTH_MAX and isinstance(value, list):
            line = wrap(line)
        buffer.write(f"{line}\n")
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
            value = ", ".join(f"'{s}'" for s in obj)
        else:
            value = ", ".join(str(s) for s in obj)
    elif obj is None:
        value = "''"
    else:
        value = str(obj)
    return value

def wrap(line):
    """
    Breaks a single line with comma-separated values
    into a multiline string.
    """
    after_eq_sign = line.find("=") + 1
    key = line[:after_eq_sign]
    params = [p.strip() for p in line[after_eq_sign:].split(",")]
    if len(params) > 1:
        # Indent length includes the parameter, equal sign, and the space after it
        indent = " " * (len(key) + 1)

        wrapped_lines = []
        l = " " + params[0]        # 1st parameter
        for p in params[1:]:
            if len(l) < NL_COLUMN_WIDTH_MAX:
                l += ", " + p
            else:
                wrapped_lines.append(l)
                l = f"{indent}{p}" # start of new line
        wrapped_lines.append(l)    # last set of parameters
        return key + ",\n".join(wrapped_lines)
    else:
        return line

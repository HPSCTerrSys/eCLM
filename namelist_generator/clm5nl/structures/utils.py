from collections import OrderedDict
from itertools import filterfalse
from io import StringIO

NL_COLUMN_WIDTH_MAX = 80

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
        # Key length includes the equal sign and the space after it
        indent = " " * (len(key) + 1)
        # Indent parameters based on key length
        wrapped_lines =  [f"{indent}{p}" for p in params]
        # Replace indent on the 1st parameter with a leading space
        wrapped_lines[0] = " " + wrapped_lines[0].strip()
        return key + ",\n".join(wrapped_lines)
    else:
        return line

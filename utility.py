"""Utility functions for ensuring correct inputs

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import ndarray


# conversion from point to vector representation
vec = lambda constr: constr if type(constr) == ndarray else constr.coords

def modecheck_type(mode_var) -> str:
    """Checks whether user input for mode is string. If yes, makes sure that it is lowercase.
    ARGS:
        mode_var: user input for mode selection
    RETURNS:
        mode_lower (str): lowercase mode selection string
    """
    if type(mode_var) != str:
        raise TypeError("Expected type for mode: str")
    mode_lower = mode_var.lower()
    return mode_lower

def modecheck_val(mode_var):
    """Checks whether user input for mode is 'point' or 'vector'. If not, raises ValueError.
    ARGS:
        mode_var: user input for mode selection
    """
    if mode_var != 'point' and mode_var != 'vector':
        raise ValueError("Mode must be either \'point\' or \'vector\'")

def argcheck_dim(dim: int, *args):
    """Checks whether all arguments are of same dimension dim. If not, raises ValueError.
    ARGS:
        dim (int): required dimension of arguments
        *args: Point objects or ndarrays
    """
    arg_len = [len(vec(arg)) for arg in args]
    if min(arg_len) < dim < max(arg_len):
        raise ValueError("Mismatch in argument dimensions!")
    elif dim != min(arg_len):
        raise ValueError(f"Expected Argument of {dim} dimensions, got {min(arg_len)}")
    else:
        return
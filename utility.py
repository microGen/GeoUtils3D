"""Utility functions for ensuring correct inputs

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import ndarray


# conversion from point to vector representation
vec = lambda constr: constr if type(constr) == ndarray else constr.coords
# unpack list to comma-separated string
expand = lambda l: ", ".join(t.__name__ for t in l)

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

def modecheck_val(mode_var) -> bool:
    """Checks whether user input for mode is 'point' or 'vector'. If not, raises ValueError.
    ARGS:
        mode_var: user input for mode selection
    RETUNRS:
        True if mode_var is 'point' or 'vector'
    """
    mode_var = lower(mode_var)
    if mode_var != 'point' and mode_var != 'vector':
        raise ValueError("Mode must be either \'point\' or \'vector\'")
    else:
        return True

def argcheck_dim(dim: int, *args) -> bool:
    """Checks whether all arguments are of same dimension dim. If not, raises ValueError.
    ARGS:
        dim (int): required dimension of arguments
        *args: Point objects or ndarrays
    RETUNRS:
        True if arguments are of specified dimensions
    """
    arg_len = [len(vec(arg)) for arg in args]
    if min(arg_len) < dim < max(arg_len):
        raise ValueError("Mismatch in argument dimensions!")
    elif dim != min(arg_len):
        raise ValueError(f"Expected Argument of {dim} dimensions, got {min(arg_len)}")
    else:
        return True

def argcheck_type(types: list, argument) -> bool:
    """Checks whether argument is of at least one of the specified types.
    ARGS:
        types (list): list of types
        argument: argument to be checked
    RETURNS:
        True if argument is of specified type
    """
    arg_pass = False
    for t in types:
        arg_pass = arg_pass or type(argument) == t
    if not arg_pass:
        #raise ValueError(f"Type mismatch in argument. Calling function takes following types: {[t.__name__ for t in types]}")
        raise ValueError(f"Type mismatch in argument. Calling function takes following types: {expand(types)}")
    else:
        return True

def argcheck_minmax(min, max, argument) -> bool:
    """Checks whether argument is within minimum and maximum values.
    ARGS:
        min: Minimum value
        max: Maximum value
        argument: argument to be checked
    RETURNS:
        True if argument is within bounds
    """
    arg_within_bounds = min <= argument <= max
    if not arg_within_bounds:
        raise ValueError(f"Argument out of bounds. Minimum: {min}, maximum: {max}, received: {argument}")
    else:
        return True
"""Types for 3D geometry operations.

Copyright (c) 2019 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import array
from numpy import ndarray
from numpy import cross

# conversion between vector and point representation
vec = lambda constr: constr if type(constr) == ndarray else constr.coords
pt = lambda constr: constr if type(constr) == Point else Point(constr)

def _modecheck_type(mode_var) -> str:
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

def _modecheck_val(mode_var):
    """Checks whether user input for mode is 'point' or 'vector'. If not, raises ValueError.
    ARGS:
        mode_var: user input for mode selection
    """
    if mode_var != 'point' and mode_var != 'vector':
        raise ValueError("Mode must be either \'point\' or \'vector\'")

def _argcheck_dim(*args):
    """Checks whether all arguments are of same dimension. If not, raises ValueError."""
    arg_len = [len(vec(arg)) for arg in args]
    if min(arg_len) < max(arg_len):
        raise ValueError("Mismatch in argument dimensions!")

class Point:
    """Point primitive"""
    #TO DO: Implement type and value checking of setters!

    def __init__(self, *coords):
        """Creates point in 2D or 3D space.
        ARGS:
            coords: ndarray of 2 or 3 elements
                    or 2 or 3 float arguments
        """
        if len(coords) == 1 and type(coords[0]) == ndarray:
            if 2 <= len(coords[0]) <= 3:
                self.__coords = coords[0]
            else:
                raise ValueError("Point currently only works in 2D and 3D space.")
        elif 1 < len(coords) <= 3:
            self.__coords = array(coords)
        else:
            raise TypeError("Point constructor takes either one ndarray or 2 or 3 floats as arguments.")

        self.__x = self.__coords[0]
        self.__y = self.__coords[1]
        if len(coords) == 3:
            self.__z = self.__coords[2]
        else:
            self.__z = None

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x_coord):
        self.__coords[0] = x_coord
        self.__x = x_coord

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, y_coord):
        self.__coords[1] = y_coord
        self.__y = y_coord

    @property
    def z(self) -> float:
        return self.__z

    @z.setter
    def z(self, z_coord):
        self.__coords[2] = z_coord
        self.__z = z_coord

    @property
    def coords(self) -> ndarray:
        return self.__coords

    @coords.setter
    def coords(self, new_coords: ndarray):
        self.__coords = new_coords


class Line:
    """Line primitive"""

    def __init__(self, constraint_0, constraint_1, mode: str):
        """Creates line in 2D or 3D space
        ARGS:
            constraint_0:
                Point object or ndarray representing a vector to (first) base point
            constraint_1:
                Point object or ndarray representing a vector to second base point
                or ndarray representing vector parallel to line
            mode (str): 'point' for defining line with two points or 'vector' for point and vector form
        """
        mode = _modecheck_type(mode)
        if type(constraint_0) != Point and type(constraint_0) != ndarray:
            raise TypeError("Argument \'constraint_0\' takes Point object or ndarray.")
        _argcheck_dim(constraint_0, constraint_1)

        self.__point_a = vec(constraint_0)
        if mode == 'point':
            if type(constraint_1) != Point and type(constraint_1) != ndarray:
                raise TypeError("Argument \'constraint_1\' takes Point object or ndarray in mode \'point\'.")
            self.__point_b = vec(constraint_1)
            self.__vector = self.__point_b - self.__point_a
        elif mode == 'vector':
            if type(constraint_1) != ndarray:
                raise TypeError("Argument \'constraint_1\' takes ndarray in mode \'vector\'.")
            self.__vector = vec(constraint_1)
            self.__point_b = self.__point_a + self.__vector
        else:
            e_str = f"Line parameter \'mode\' takes either \'point\' or \'vector\' as argument. Unknown argument {mode}"
            raise ValueError(e_str)

    @property
    def point_a(self) -> ndarray:
        return self.__point_a

    @point_a.setter
    def point_a(self, new_const):
        self.__point_a = vec(new_const)
        self.__vector = self.__point_b - self.__point_a

    @property
    def point_b(self) -> ndarray:
        return self.__point_b

    @point_b.setter
    def point_b(self, new_const):
        self.__point_b = vec(new_const)
        self.__vector = self.__point_b - self.__point_a

    @property
    def vector(self) -> ndarray:
        return self.__vector

    @vector.setter
    def vector(self, new_vector: ndarray):
        self.__vector = new_vector
        self.__point_b = self.__point_a + self.__vector

    def point(self, scale: float) -> ndarray:
        """Returns a point on the line.
        ARGS:
            scale (float): scales the direction vector of the line extending from base point
        RETURNS:
            point_on_line (ndarray): Point on line, determined by scaling defining vectors
        """
        point_on_line = self.__point_a + scale * self.__vector
        return point_on_line


class Plane:
    "Plane primitive"

    def __init__(self, constraint_0, constraint_1, constraint_2, mode: str):
        """Creates a plane in 2D or 3D space. 3 forms of representation are possible:
        - three points
        - point and two vectors defining plane
        - point, vector parallel to plane and vector normal to plane
        ARGS:
            constraint_0:
                Point object or ndarray representing vector to base point
            constraint_1:
                Point object or ndarray representing vector to second base point
                or ndarray representing vector parallel to plane
            constraint_2:
                Point object or ndarray representing vector to third base point
                or ndarray representing second vector parallel to plane (non-parallel to constraint_1)
                or ndarray representing vector normal to plane
            mode (str): "point", "vector", "normal" for plane representation
        """
        mode = _modecheck_type(mode)
        if type(constraint_0) != Point and type(constraint_0) != ndarray:
            raise TypeError("Argument \'constraint_0\' takes Point object or ndarray.")
        _argcheck_dim(constraint_0, constraint_1, constraint_2)

        self.__point_a = vec(constraint_0)
        if mode == 'point':
            if type(constraint_1) != Point and type(constraint_1) != ndarray:
                raise TypeError("Argument \'constraint_1\' takes Point object or ndarray in mode \'point\'.")
            if type(constraint_2) != Point and type(constraint_2) != ndarray:
                raise TypeError("Argument \'constraint_2\' takes Point object or ndarray in mode \'point\'.")

            self.__point_b = vec(constraint_1)
            self.__point_c = vec(constraint_2)
            self.__vector_u = self.__point_b - self.__point_a
            self.__vector_v = self.__point_c - self.__point_a
        else:
            if type(constraint_1) != ndarray:
                raise TypeError(f"Argument \'constraint_1\' takes ndarray in mode \'{mode}\'.")
            if type(constraint_2) != ndarray:
                raise TypeError(f"Argument \'constraint_2\' takes ndarray in mode \'{mode}\'.")

            self.__vector_u = vec(constraint_1)
            self.__point_b = self.__point_a + self.__vector_u
            if mode == 'vector':
                self.__vector_v = vec(constraint_2)
            elif mode == 'normal':
                # generate second plane defining vector to calculate points on plane
                self.__vector_v = cross(self.__point_c, self.__vector_u)
            else:
                e_str = f"Plane parameter \'mode\' takes either \'point\', \'vector\' or \'normal\' as argument. " \
                        f"Unknown argument {mode}"
                raise ValueError(e_str)
            self.__point_c = self.__point_a + self.__vector_v
        self.__normal = cross(self.__vector_u, self.__vector_v)

    @property
    def point_a(self) -> ndarray:
        return self.__point_a

    @point_a.setter
    def point_a(self, new_const):
        self.__point_a = vec(new_const)

    @property
    def point_b(self) -> ndarray:
        return self.__point_b

    @point_b.setter
    def point_b(self, new_const):
        self.__point_b = vec(new_const)

    @property
    def point_c(self) -> ndarray:
        return self.__point_c

    @point_c.setter
    def point_c(self, new_const):
        self.__point_c = vec(new_const)

    @property
    def normal(self) -> ndarray:
        return self.__normal

    def point(self, scale_a: float, scale_b: float) -> ndarray:
        """Calculates a point on the plane
        ARGS:
           scale_a (float): scales vector a
           scale_b (float): scalse vector b
        RETURNS:
            point_on_plane (ndarray): Point on plane, determined by scaling defining vectors
        """
        point_on_plane = self.__point_a + scale_a * self.__vector_v + scale_b * self.__vector_v
        return point_on_plane

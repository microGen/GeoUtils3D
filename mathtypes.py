"""Types for 3D geometry operations.

Copyright (c) 2019 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import array as array
from numpy import ndarray as ndarray

# conversion between vector and point representation
vec = lambda constr: constr if type(constr) == ndarray else constr.coords
pt = lambda constr: constr if type(constr) == Point else Point(constr)

class Point:
    """Point primitive"""
    #TO DO: Allow point creation by numpy array

    def __init__(self, *coords):
        """Creates point in 2D or 3D space.
        ARGS:
            coords: ndarray of 2 or 3 elements
                    or 2 or 3 float arguments
        """
        if len(coords) == 1 and type(coords) == ndarray:
            if 2 <= len(coords) <= 3:
                self.__coords = coords
            else:
                raise ValueError("Point currently only works in 2D and 3D space.")
        elif 1 < len(coords) <= 3:
            self.__coords = array(coords)
            self.__x = coords[0]
            self.__y = coords[1]
            if len(coords) == 3:
                self.__z = coords[2]
            else:
                self.__z = None
        else:
            raise TypeError

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

    def __init__(self, constraint_0, constraint_1):
        """Creates line in 2D or 3D space
        ARGS:
            constraint_0: Point object or ndarray representing a vector to base point
            constraint_1: Point object or ndarray representing a vector parallel to line
        """
        if type(constraint_0) == Point:
            self.__base = constraint_0
        elif type(constraint_0) == ndarray:
            self.__base = Point(constraint_0)
        else:
            raise TypeError

        if type(constraint_1) == Point:
            self.__vector = constraint_1.coords - constraint_0.coords
        elif type(constraint_1) == ndarray:
            self.__vector = constraint_1
        else:
            raise TypeError

    @property
    def base(self) -> Point:
        return self.__base

    @base.setter
    def base(self, new_base: Point):
        self.__base = new_base

    @property
    def vector(self) -> ndarray:
        return self.__vector

    @vector.setter
    def vector(self, new_vector: ndarray):
        self.__vector = new_vector

    def point(self, scale: float) -> ndarray:
        """Returns a point on the line.
        ARGS:
            scale: float, scales the direction vector of the line extending from base point
        RETURNS:
            point_on_line: numpy array of point coordinates
        """
        point_on_line = self.__base.coords + scale * self.__vector
        return point_on_line


class Plane:
    "Plane primitive"

    #TO DO: implement methods to yield 1.) points on plane 2,) coordinate data / conversion between representations

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
            mode (str): "points", "vector", "normal" for plane representation
        """
        if type(mode) != str:
            raise TypeError("mode expected: str")
        else:
            self.__constraint_0 = vec(constraint_0)
            self.__constraint_1 = vec(constraint_1)
            self.__constraint_2 = vec(constraint_2)
            self.__mode = mode
            else:
                errstring = f"Unknown mode: {mode}"
                raise ValueError(errstring)

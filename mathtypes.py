"""Types for 3D geometry operations.

Copyright (c) 2019 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import array as array
from numpy import ndarray as ndarray
from numpy import cross as npcross

# conversion between vector and point representation
vec = lambda constr: constr if type(constr) == ndarray else constr.coords
pt = lambda constr: constr if type(constr) == Point else Point(constr)

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
            scale (float): scales the direction vector of the line extending from base point
        RETURNS:
            point_on_line (ndarray): point coordinates
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
        mode = self.__modecheck(mode)
        if mode != 'points' and mode != 'vector' and mode != 'normal':
            errstring = f"Unknown mode: {mode}"
            raise ValueError(errstring)

        self.__base = vec(constraint_0)
        self.__constraint_1 = vec(constraint_1)
        self.__constraint_2 = vec(constraint_2)

        if mode == 'points':
            self.__vector_a = self.__constraint_1 - self.__base
            self.__vector_b = self.__constraint_2 - self.__base
        else:
            self.__vector_a = self.__constraint_1
            if mode == 'vector':
                self.__vector_b = self.__constraint_2
            else:
                # generate second plane defining vector to calculate points on plane
                self.__vector_b = npcross(self.__constraint_2, self.__vector_a)
        self.__normal = npcross(self.__vector_a, self.__vector_b)

    def __modecheck(self, mode_var) -> object:
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

    def point(self, scale_a: float, scale_b: float, mode: str = "point"):
        """Calculates a point on the plane
        ARGS:
           scale_a (float): scales vector a
           scale_b (float): scalse vector b
           mode (str): swith between returning a Point object or an ndarray, default: Point
        RETURNS:
            point_on_plane: Point on plane, determined by scaling defining vectors. Either Point object or ndarray
        """
        mode = self.__modecheck(mode)
        if mode != 'point' and mode != 'vector':
            raise ValueError("Mode must be either \'point\' or \'vector\'")
        point_on_plane = self.__base + scale_a * self.__vector_b + scale_b * self.__vector_b
        if mode == 'point':
            return Point(point_on_plane)
        else:
            return point_on_plane

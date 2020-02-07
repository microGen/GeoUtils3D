"""Solid geometry (mesh) types derived from general 3D math geometry primitives.

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import array
from numpy import ndarray

import utility
from mathtypes import Point as __Point
from mathtypes import Line as __Line
from mathtypes import Plane as __Plane


class Vertex(__Point):
    """Vertex primitive in 3D space"""
    _dimension = 3

class Edge(__Line):
    """Edge primitive in 3D space"""
    _dimension = 3
    _argtypes_point = [ndarray, Vertex]

    def __init__(self, vert_0, vert_1):
        utility.argcheck_type(self._argtypes_point, vert_0)
        utility.argcheck_type(self._argtypes_point, vert_1)
        utility.argcheck_dim(self._dimension, vert_0, vert_1)
        super(Edge, self).__init__(vert_0, vert_1, 'point')

    def point(self, proportion: float):
        """Calculates a point on the edge.
        ARGS:
            proportion (float): Scalar between 0 and 1, representing the proportion of segment between first Vertex and
            point to total Edge length.
        RETURNS:
            point_on_edge (ndarray): Point on edge
        """
        utility.argcheck_type([int, float], proportion)
        utility.argcheck_minmax(0, 1, proportion)
        point_on_edge = self.point_a + self.vector * proportion
        return point_on_edge

class Face(__Plane):
    """Face primitive in 3D space"""
    # can be defined with points and edges
    # edges have to share vertices with next/previous edges
    # edges connect counter-clockwise
    # use edges to find neighboring face
    _dimension = 3
    _argtypes_point = [ndarray, Vertex]
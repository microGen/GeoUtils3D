"""Solid geometry (mesh) types derived from general 3D math geometry primitives.

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from mathtypes import Point
from mathtypes import Line
from mathtypes import Plane


class Vertex(Point):
    _dimension = 3
    pass

class Edge(Line):
    _dimension = 3
    pass

class Face(Plane):
    # can be defined with points and edges
    # edges have to share vertices with next/previous edges
    # edges connect counter-clockwise
    # use edges to find neighboring face
    _dimension = 3
    pass
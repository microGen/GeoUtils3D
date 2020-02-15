"""Utility functions for 3D geometry operations.

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

import numpy as np
import utility

from mathtypes import Point
from mathtypes import Line
from mathtypes import Plane

from uvtypes import UVPoint
from uvtypes import UVLine

#obsolete?
def calculate_normal(plane: Plane) -> np.ndarray:
    """Calculates normal of a face defined by 3 points in 3D space.
    ARGS:
        plane (Plane): Plane in 3D space defined by 3 points
    RETURNS:
        normal_vector (np.ndarray): vector normal to plane in 3D space
    """
    pl0, pl1, pl2 = [np.array(pli) for pli in plane]
    normal_vector = np.cross(pl1-pl0, pl2-pl0)
    return normal_vector

def dist_point_point(point_0: Point, point_1: Point) -> float:
    """Calculates the distance between two points in 3D space.
    ARGS:
        point_0, point_1 (Point): Points in 3D space
    RETURNS:
        dist (float): scalar distance between both points
    """
    vector = point_1.coords - point_0.coords
    dist = np.linalg.norm(vector)
    return dist

def dist_point_line(point: Point, line: Line) -> float:
    """Calculates the distance between a point and a line in 3D space.
    ARGS:
        point (Point): Point in 3D space
        line (Line): Line in 3D space defined by 2 points
    RETURNS:
        dist(float): scalar minimum distance between point and line
    """
    p = point.coords
    l_a = line.point_a
    l_vec = line.vector
    num = np.linalg.norm(np.cross(l_vec, (p - l_a)))
    dist = num / np.linalg.norm(l_vec)
    return dist

def dist_point_plane(point: Point, plane: Plane) -> float:
    """Calculates the distance of a point to a plane in 3D space.
    ARGS:
        point (Point): Point in 3D space
        plane (Plane): Plane in 3D space defined by 3 points
    RETURNS:
        dist(float): scalar minimum distance between point and line
    """
    p = point.coords
    pl_a = plane.point_a
    pl_norm = plane.normal
    num = np.linalg.norm(np.dot(pl_norm, (p - pl_a)))
    dist = num / np.linalg.norm(pl_norm)
    return dist

def intersection_line_plane(line: Line, plane: Plane) -> np.ndarray:
    """Calculates the intersection point between a line and a plane in 3D space.
    ARGS:
        line (Line): Line in 3D space defined by 2 points
        plane (Plane): Plane in 3D space defined by 3 points
    RETURNS:
        intersection_point (ndarray): intersection point of line and plane
    """
    l_a = line.point_a
    l_vec = line.vector
    pl_a = plane.point_a
    pl_norm = plane.normal
    num = np.dot(pl_norm, (pl_a - l_a))
    den = np.dot(pl_norm, l_vec)
    intersection = l_a + np.dot(num/den, l_vec)
    return intersection

def project_vector(vector_0: np.array, vector_1: np.array) -> np.array:
    """Projects vector_0 onto vector_1 and returns the resulting vector.
    ARGS:
        vector_0, vector_1 (np.array): vectors in 3D space
    RETURNS:
        projection (np.array): projected vector in 3D space
    """
    num = np.dot(vector_1, vector_0)
    den = np.dot(vector_1, vector_1)
    projection = num / den * vector_1
    return projection

def map_xyz_to_uv(origin, u_axis: np.ndarray, normal: np.ndarray, point, norm: bool = True) -> UVPoint:
    """Map coordinates of a point in 3D space to local UV coordinates.
    ARGS:
        origin: Origin of local coordinate system. Either Point object or vector.
        u_axis (np.ndarray): vector defining local U axis
        normal (np.ndarray): normal pointing out of UV plane
            i.e. the plane in 3D space on which the UV coordinate system resides
        point: Point to be translated to UV projection. Either Point object or vector.
        norm (bool): normalize UV coordinate system (default: True) or use U vector to scale UV system.
    RETURNS:
        uv_coords (UVPoint): UVPoint object on UV plane.
    """
    origin = utility.vec(origin)
    point = utility.vec(point)
    utility.argcheck_dim(3, origin, u_axis, normal, point)

    point = point - origin
    v_axis = np.cross(u_axis, -normal)
    if norm:
        #normalize coordinate system
        u_axis = u_axis / np.linalg.norm(u_axis)
        v_axis = v_axis / np.linalg.norm(v_axis)
    uv_system = np.stack((u_axis, v_axis))
    uv_coords = UVPoint(*np.dot(uv_system, point))
    return uv_coords

def left_of(uv_vector_0: np.ndarray, uv_vector_1: np.ndarray) -> bool:
    pass

# under construction
# needs implementation of Face class first
'''
def point_in_triangle(face_uv: Face, point_uv: PointUV) -> bool:
    """Calculates whether point is within bounds of given triangular face in 2D space.
    ARGS:
        face_uv (PlaneUV): triangle in UV space defined by 3 points
        point_uv (PlaneUV): point in UV space
    RETURNS:
        in_bounds (bool): True if point is in triangle, False if not
    """
    #check whether point is on the same side of an edge as the third vertex of the triangle
    alignment = lambda p0, p1, line: np.dot(np.cross(line[1] - line[0], p0 - line[0]),\
                                      np.cross(line[1] - line[0], p1 - line[0])) >= 0
    p_uv = np.array(point_uv)
    #create edges from vertices
    edges = []
    for i in range(3):
        edges.append(np.array([face_uv[i%3], face_uv[(i+1)%3]]))
    in_bounds = alignment(p_uv, face_uv[0], edges[1]) and alignment(p_uv, face_uv[1], edges[2]) and\
        alignment(p_uv, face_uv[2], edges[0])
    return in_bounds
'''
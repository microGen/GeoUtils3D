# GeoUtils3D
Compact packet of common 3D geometry calculations in Python 3.7+

## Basic Usage
There are three basic types of geometry classes:
* Math types (mathematical geometry objects) found in `mathtypes.py`
    * Point `Point`
    * Line `Line`
    * Plane `Plane`
* Mesh types (3D mesh / solid geometry objects) found in `meshtypes.py`
    * Vertex `Vertex`
    * Edge `Edge`
    * Face `Face`
* UV types (strictly 2D geometry objects, e.g. for projections onto a 3D plane) found in `uvtypes.py`
    * UV Point `UVPoint`
    * UV Line `UVLine`
    
### No inheritance?
Although it seems logical at first to let the Mesh and UV classes inherit their features from the Math classes,
this leads to a lot of naming problems.
Therefore, I limited the inheritance to cases where it makes sense.

## 3D geometry
The primitives `Point`, `Line` and `Plane` are defined via coordinates in 3D space.
Defining a `Point` is possible by using scalar coordinates or a vector (numpy array):

`p0 = Point(x, y, z)`

`p1 = Point(numpy.array([a,b,c]))`

Using points or vectors, lines and planes can be defined:

`l0 = Line(p0, p1)`

`pl0 = Plane(p0, numpy.array([a,b,c]), mumpy.array([u,v,w]))`

Multiple representation forms are possible. These are converted internally to yield the same set of data.

### UV geometry
The same goes for UV geometry

`pUV = UVPoint(u, v)`

However, since the `UVLine` only takes `UVPoint` or 2D-vectors, defining a `UVLine` object using 3D objects
as arguments will result in an error.

### Mesh geometry
The difference between a `Vertex` and a `Point` is just in naming, to keep respective geometry types consistent.
However, classes of higher orders exhibit greater differences: `Line` and `Plane` are infinite, whereas `Edge`
and `Face` are delimited by vertices. An attempt to use 3D calculations meant for the mathematical types on
mesh objects will result in errors.

Defining and using mesh geometry objects is similar to math geometry objects.

`Edge` will only take vectors or `Vertex` objects instead of `Point` objects.

`Face` is still work in progress.

## Functions
Functions usually take math types or vectors as arguments.

### General functions
`calculate_normal(plane: Plane) -> np.ndarray`

`intersection_line_plane(line: Line, plane: Plane) -> Point`

`project_vector(vector_0: np.array, vector_1: np.array) -> np.array`

### Calculating distances
`dist_point_point(point_0: Point, point_1: Point) -> float`

`dist_point_line(point: Point, line: Line) -> float`

`dist_point_plane(point: Point, plane: Plane) -> float`

### UV operations
`map_xyz_to_uv(origin: Point, u_axis: np.ndarray, normal: np.ndarray, point: Point) -> UVPoint`

`point_in_triangle(face_uv: PlaneUV, point_uv: PointUV) -> bool`

### To Do
- [ ] Distance Line - Line
- [ ] Distance Plane - Plane
- [ ] Checking whether planes are parallel
- [ ] Angle between lines
- [ ] Angle between planes
- [ ] Angle between vectors
- [ ] ...

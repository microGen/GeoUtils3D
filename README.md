# GeoUtils3D
Incomplete list of utility functions for 3D geometry operations. Will be updated irregularily.

## Basic Usage
Primitives are implemented as named tuples. See Python documentation `collections.namedtuple`

### 3D geometry
The primitives point, line and plane are defined via coordinates in 3D space.
Defining a point:

`p0 = Point(x, y, z)`

Using points, lines and planes can be defined:

`l1 = Line(p0, p1)`

### UV geometry
It is also possible to define the same primitives in UV space:

`pUV = PointUV(u, v)`


## Functions
Functions usually take primitives or vectors as arguments.

### General functions
`calculate_normal(plane: Plane) -> np.ndarray`

`intersection_line_plane(line: Line, plane: Plane) -> Point`

`project_vector(vector_0: np.array, vector_1: np.array) -> np.array`

### Calculating distances
`dist_point_point(point_0: Point, point_1: Point) -> float`

`dist_point_line(point: Point, line: Line) -> float`

`dist_point_plane(point: Point, plane: Plane) -> float`

### UV operations
`map_xyz_to_uv(origin: Point, u_axis: np.ndarray, normal: np.ndarray, point: Point) -> PointUV`

`point_in_triangle(face_uv: PlaneUV, point_uv: PointUV) -> bool`

### To Do
- [ ] Distance Line - Line
- [ ] Distance Plane - Plane
- [ ] Checking whether planes are parallel
- [ ] Angle between lines
- [ ] Angle between planes
- [ ] Angle between vectors
- [ ] ...

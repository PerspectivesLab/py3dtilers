# Ifc Tiler

## Installation

See [installation notes](https://github.com/VCityTeam/py3dtilers/blob/master/README.md)

## See also

- [Understanding ifc geometry and processing](IFC_Geometry.md)

## IfcTiler features

### Run the IfcTiler

```bash
(venv) ifc-tiler --file_path <path>
```

\<path\> should point to a directory holding an IFC file.
The resulting 3DTiles tileset will contain the ifc geometry, ordered by category :
each tile will contain an IFC Object Type, that can be found in the batch table, along with its GUID

This command should produce a directory named "ifc_tileset".

### Group by

The `--grouped_by` flag allows to choose how to group the objects. The two are options are `IfcTypeObject` and `IfcGroup` (by default, the objects are grouped by type).

Group by `IfcTypeObject`:

```bash
ifc-tiler --file_path <path> --grouped_by IfcTypeObject
```

Group by `IfcGroup`:

```bash
ifc-tiler --file_path <path> --grouped_by IfcGroup
```

### Unit of length

The flags `--originalUnit` and `--targetedUnit` respectively allow to choose the unit of length used to read the IFC file and the one used to write the features as 3DTiles. The default unit is meter. The options are millimeters (`mm`), centimeters (`cm`), meters (`m`) and kilometers (`km`).

```bash
ifc-tiler --file_path <path> --originalUnit cm --targetedUnit km
```

## Shared Tiler features

See [Common module features](../Common/README.md#common-tiler-features).

## About the tiler

- Projection system conversion using Pyproj :
  - Need to be used in CL

- Scale change of the geometry :
  - Actually, we can change from centimeter to meter
  - Need to be used or not in CL
  - Need to accept more units

- Support only IFC4 :
  - need to support IFC2XC3 :
    - test the file version
    - change the geometry access

- Support the following geometry types, ignore other types :
  - MappedRepresentation
  - Tesselation : desribe triangles and vertex in a classic way, they are used without modification
  - SweptSolid : describe a 2D area that needs to be extruded, using a direction.
    - Method used
      - To triangulate this type of geometry, first we triangulate the 2d area, using its center as a new vertex
      - Then we create another 2D area, using the extrusion information, triangulate with the same method.
      - Finally, the 2 area are linked with triangle between each "same" vertex (if there was no extrusion)
      - Needs and drawback :
        - Currently supports only OuterCurver 2D point list for the 2D area
        - The triangulation will not support hole in the 2D area
        - The triangulation may not be optimal

- All object position are relative to the site position (the higher node in the hierarchy ifc file). The position of the site is put in the transform field of the tileset.json of the generated 3DTiles, meaning that we can easily change the IFC position directly in the tileset.json file.

### Notes

Existing possible solutions for a few needs

#### __To use CSG representation type__

[IfcCSGSolid](https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD1/HTML/schema/ifcgeometricmodelresource/lexical/ifccsgsolid.htm) : Boolean results of operations between solid models, half spaces and Boolean results

Use [Trimesh](https://trimsh.org/index.html) to create [parametrable primitives](https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD1/HTML/schema/ifcgeometricmodelresource/lexical/ifccsgprimitive3d.htm)

```bash
mesh1 = shapely.geometry.box(minx, miny, maxx, maxy, ccw=True) 
mesh2 = trimesh.creation.cylinder(2,5)
trimesh.boolean.difference([mesh1,mes5h2],"scad")
```

#### __To extrude triangulated polygones__

Use [Trimesh](https://trimsh.org/index.html)

Transform the geometry into trimesh structure and then use :  
```trimesh.creation.extrude_triangulation()```

#### __To triangulate and extrud polygones__

Use [Trimesh](https://trimsh.org/index.html) and [OpenScad](https://openscad.org/) and [Shapely](https://pypi.org/project/Shapely/)

- needs the [Triangle](https://www.cs.cmu.edu/~quake/triangle.html) library (needs C++ 14+ and Visual Studio Installer) and the [python wrapper](https://pypi.org/project/triangle/)
- needs the mapbox_earcut library and Cmake

```bash
exterior = [(0, 0), (0, 20), (20, 20), (20, 0), (0, 0)]
interior = [(10, 0), (5, 5), (10, 10), (15, 5), (10, 0)][::-1]
polygon = Polygon(exterior, [interior])
trimesh.creation.extrude_polygon(polygon,50)
```

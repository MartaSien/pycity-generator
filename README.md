# 3D modeling with build123d

## Introduction

This repository contains 2 exercises to showcase the build123d library for 3D modeling in Python. Originally, it was prepared for a Lightning Talk for PyGda, alongside this [presentation](https://slides.com/martasienkiewicz/deck-a7dc81/edit).

### cube.py

Simple exercise to make a cube with a hole.

1. The cube's base is square
1. The hole's base is a circle
1. We want to input the following parameters:
   - r - radius of the hole
   - h - height of the cube
   - a - side of the cube

### city.py

Excercise to fetch OSM (Open Street Maps) data of buildings and display it as a 3D model.

## Development guidelines

### Managing dependencies

I highly recommend using a [virtual environment](https://docs.python.org/3/library/venv).

Then, follow the recommended way to install the `build123` package on [pypi](https://pypi.org/project/build123d/).

If you use Visual Studio Code, you can install OCP CAD Viewer extension to preview the model during development.

### On Python version

Currently, build123d doesn't support Python 3.13, that's why I'm using 3.12.

### Required:

- osmnx - to fetch and parse OSM data
- build123d - to make a 3D model based on OSM data

### Nice to have:

- ocp_vscode - part of a Visual Studio Plugin to preview the generated 3D model
- folium - to visualise OSM data on a map, to compare the results with the 3D model

Be mindful that osmnx and build123d have many dependencies on their own. For instance, osmnx represents data as Pandas dataframes.

## FAQ

### Why `build123d` and not `CadQuery`?

CadQuery is another great Python library for 3D modelling. However, I find Build123d's syntax easier to follow and maintain. This is a matter of my personal preference. I've prepared the first exercise both in CadQuery and Build123d, to compare the syntax.

## Accessing building outline data

To get the building outlines we can use the open source geospacial dataset Open Street Maps (OSM). Most of you are probably more familiar with Google Maps API, but I recommend checking out OSM's capabilities. It is not as user friendly, but it has a wealth of information gathered by the community and it doesn't limit you in terms of services and numbers of requests. 

OSM uses `labels` to organize the city data. I'm using the following ones:

## Model representation

Build123d uses BREP 3D model representation, which stands for 'boundary representation'. Offering precision, it is a commonly used technique in CAD (Computer-Aided Design).
It is a representation of the 3D shape by bounding its volume with surfaces, curves, points etc. Moreover, it offers many transformation methods, such as boolean operations.

To properly appreciate BREP let's consider another common 3D modelling representation method - mesh. In mesh, we represent a shape with edges and vertices.

If we were to make a 3D model of a square object like this, it seems perfect. We represent vertices and edges, it's elegant, simple and precise.

However, if we take a more complex shape, such as a curve things get more complicated. Remember, in mesh we have only straight edges and vertices. So we need to make this curve discrete, that is divide it into a finite number of elements.
We can decide how many vertices we have. The more vertices, the more precise is this representation and the more complex the final model. Each vertex has a defined point in the 2D or 3D space. We might have 10 such points of one, very imprecise circle.

On the other hand, using BREP we can represent this shape using a mathematical description. This way, we have a perfect circle - a bounding curve defined by its center and a diameter.
Curves clearly show the weakness of mesh representation.

## Beauty of 3D modeling in Python

This is just my personal opinion, but using Python to model shapes that you are not likely to want to change in a parametric way is usually an overkill. In a time that takes me to make a script to make such a shape, I can do it a few times more in a 3D modelling software like [Rhinoceros](https://www.rhino3d.com/), or, for a free alternative, Autodesk's [Fusion 360](https://www.autodesk.com/products/fusion-360/personal?msockid=1f1a99e05a7e6e1206748d9f5b7e6f34).

I think that the true power of using build123d is being able to combine it with other Python libraries. Our creativity is the limit here. That's why I'm showing a project that utilizes OSM.

## Attributions

This project was inspired by [Elk](https://www.food4rhino.com/en/app/elk). A plugin to Grasshopper that takes Open Street Maps (OSM) data and fetches outlines of buildings. I thought it would be interesting to try to recreate it in Python.

### Wonderfully documented libraries

- [Build123d](https://build123d.readthedocs.io/en/latest/index.html)
- [CadQuery](https://cadquery.readthedocs.io/en/latest/intro.html)

### Other sources I used when preparing this presentation

- https://pygis.io/docs/d_access_osm.html
- https://medium.com/@investince/gis-showdown-comparing-google-maps-openstreetmap-and-more-8c04cebe46d6
- https://osmbuildings.org/ - another project that uses OSM and 3D modeling (JavaScript)

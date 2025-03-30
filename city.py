import math

from build123d import *
from ocp_vscode import show
import osmnx as ox
import folium

MERIDIAN = 40008000  # Length of the meridian in meters
EQUATOR = 40075160  # Length of the equator in meters
LEVEL_HEIGHT = 3.2  # Approximate height of one level in meters

locations = {  # (lat, lon)
    "przymorze": (
        54.415888,
        18.591635,
    ),  # https://obliview.brg.gda.pl/?d=0&l=-1&r=11&z=17&x=2069584.0035238648&y=7249175.687452897&poz=3526131.73,1186084.53,5164519.10,-0.5515,-0.1855,-0.8133,-0.7708,-0.2593,0.5819,-0.3188,0.9478,-0.0000&k=N&akLay=empty&sv=false&panoId=undefined
    "zaspa": (
        54.394237,
        18.612325,
    ),  # https://obliview.brg.gda.pl/?d=0&l=-1&r=11&z=17&x=2071924.1871135524&y=7245145.238027415&poz=3527504.56,1187987.19,5163153.89,-0.5518,-0.1858,-0.8130,-0.7705,-0.2595,0.5822,-0.3192,0.9477,-0.0000&k=N&akLay=empty&sv=false&panoId=undefined
    "lawendowa": (54.352788, 18.652757),
    "garnizon": (54.354634, 18.651695),
}


def deg_to_rad(degrees: float) -> float:
    """
    Converts degrees to radians.
    """
    return degrees * math.pi / 180


def latlon_to_xy(center, p) -> tuple:
    """
    Approximates planar coordinates from geographic ones, in meters.
    Uses equirectangular projection.
    """
    lat_delta = p[0] - center[0]
    lon_delta = p[1] - center[1]
    lat_circum = EQUATOR * math.cos(deg_to_rad(center[0]))
    x = lon_delta * lat_circum / 360
    y = lat_delta * MERIDIAN / 360
    return x, y


def get_polygon_footprints(building_footprints: list) -> list:
    """
    Returns a list of building footprints.
    Each building footprints consists of a list of points, that form a polyline.
    """
    output_list = []
    for footprint in building_footprints:
        footprint_points = []
        lon, lat = footprint.exterior.coords.xy
        for i in range(len(lon)):
            footprint_points.append((lat[i], lon[i]))
        output_list.append(footprint_points)
    return output_list


def model_city(footprints, levels):
    """
    Creates a 3D model of a city from building footprints and building levels.
    """
    footprints_with_levels = zip(footprints, levels)
    buildings_xy = []
    for footprint, levels in footprints_with_levels:
        footprint_xy = []
        for point in footprint:
            pt = latlon_to_xy(target_location, point)
            footprint_xy.append(pt)
        pol = Polyline(footprint_xy, close=True)
        srf = make_face(pol)
        height = int(levels) * LEVEL_HEIGHT
        if height > 0:
            extr = extrude(srf, height).clean()
            buildings_xy.append(extr)
    return buildings_xy


def map_to_html(target_location, footprint_list) -> None:
    """
    Use folium to draw building outlines on a map.
    Save the map to html file.
    """
    m = folium.Map(location=target_location)
    folium.PolyLine(footprint_list, tooltip="Building").add_to(m)
    m.save("map.html")


if __name__ == "__main__":
    target_location = locations["garnizon"]
    tags = {"building": True, "building:levels": True}
    buildings = ox.features.features_from_point(target_location, tags, 300)
    building_heights = buildings[["building:levels"]].fillna(3)

    building_footprints = buildings.geometry
    footprint_list = get_polygon_footprints(building_footprints)

    map_to_html(target_location, footprint_list)

    city = model_city(footprint_list, building_heights.values)
    show(city)

    city_compound = Compound(label="city", children=city)
    export_stl(city_compound, "city.stl")

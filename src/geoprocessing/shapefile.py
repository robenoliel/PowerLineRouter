"""
    shapefile.py

    script responsable for handling shapefiles 
"""

import rasterio as rio
from shapely.geometry import Point, LineString
import geopandas as gpd
from shapely.geometry import Polygon

def path_coords_to_polyline(points, transform):

    coords = [rio.transform.xy(transform, coord[0], coord[1]) for coord in points]
    
    poly = LineString([Point(coord[0], coord[1]) for coord in coords]).wkt
    
    gdr = gpd.GeoDataFrame({'feature': [1], 'geometry': poly})#, crs=crs)

    return gdr
"""
    shapefile.py

    script responsable for handling shapefiles 
"""

import rasterio as rio
from shapely.geometry import Point, LineString
import geopandas as gpd
from shapely.geometry import Polygon

def export_point(x,y,path,crs='EPSG:32724'):
    d = {'name': ['point'], 'geometry': [Point(x, y)]}
    gdf = gpd.GeoDataFrame(d, crs=crs)
    gdf.to_file(path)


def path_coords_to_polyline(points, transform, crs):

    coords = [rio.transform.xy(transform, coord[0], coord[1]) for coord in points]
    
    poly = LineString([Point(coord[0], coord[1]) for coord in coords])
    
    gdr = gpd.GeoDataFrame({'feature': [1], 'geometry': poly}, geometry = 'geometry', crs=crs)

    return gdr
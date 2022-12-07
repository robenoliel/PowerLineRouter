"""
    raster.py

    script responsable for handling raster files 
"""

from email.mime import base
import geopandas as gpd
import rasterio as rio
from rasterio import features, merge
import numpy as np


def get_coordinates_from_xy(xy_list, base_raster):
    """
    Returns georeferenced coordinates of points in a raster according to its xy positions. Parameters:
        xy_list: List of tuples
        base_raster: Matrix position (int)
    """
    pass

def get_xy_from_coordinates(lat, lon, base_raster):

    shape = base_raster.read(1).shape
    transform = base_raster.transform
    crs = base_raster.crs

    geometry = gpd.points_from_xy([lat], [lon], crs=crs)
    p = [(p.x, p.y) for p in geometry]

    def sample_or_error(src, x, y):
        row, col = src.index(x, y)
        if any([row < 0, col < 0, row >= src.height, col >= src.width]):
            raise ValueError(f"({lon}, {lat}) is out of bounds from {src.bounds}")

    sample_or_error(base_raster, p[0][0], p[0][1])

    rasterized = features.rasterize(geometry                   ,
                                out_shape = shape              ,
                                fill = 0                       , # value outside geometry
                                out = None                     ,
                                transform = transform          ,
                                all_touched = True             ,
                                default_value = 1              , # value whitin geometry
                                dtype = None)

    val = np.where(rasterized != 0)
    return (val[0][0], val[1][0])
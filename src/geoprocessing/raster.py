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

    geometry = gpd.points_from_xy([lat], [lon], crs='WGS84').to_crs(crs)

    rasterized = features.rasterize(geometry                   ,
                                out_shape = shape              ,
                                fill = 0                       , # value outside geometry
                                out = None                     ,
                                transform = transform          ,
                                all_touched = True             ,
                                default_value = 1              , # value whitin geometry
                                dtype = None)

    val = np.where(rasterized == 1)

    return (val[0][0], val[1][0])
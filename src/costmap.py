"""
    costmap.py

    script responsable for building the costmap
"""

import rasterio as rio
from rasterio import features, merge
import fiona
import geopandas as gpd

def costmap(path_to_raster, path_to_shape, cost):
    
    # open raster file
    raster = rio.open(path_to_raster)

    # open shapefile
    shape = gpd.read_file(path_to_shape)
    geom = [shapes for shapes in shape.geometry]

    # add cost to raster according to the shapefile region

    #TODO: Check if basemap has proj. If not: raise error.
    #TODO: Check if shapes have proj. If not: disconsider it and raise warning.
    #TODO: Verify if shapes are in same proj as basemap. If not: reproj shapes.
    rasterized = features.rasterize(geom,
                                out_shape = raster.shape,
                                fill = 0,
                                out = None,
                                transform = raster.transform,
                                all_touched = False,
                                default_value = cost,
                                dtype = None)

    cost_map = raster.read(1) + rasterized

    with rio.open(r'D:\PowerLineRouter\test\data\temp\costmap.tiff', 'w', **raster.profile) as ff:
        ff.write(cost_map,1)

    return cost_map




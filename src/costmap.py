"""
    costmap.py

    script responsable for building the costmap
"""

import rasterio as rio
from rasterio import features, merge
import fiona
import geopandas as gpd
import pandas as pd
import os

def addCost(cost_map, filepath, cost, buffer, inside, base_trans):
    # open shapefile
    file_name = os.path.basename(filepath)

    if not os.path.exists(filepath):
        print('WARNING: {} file is missing and will be disconsidered.'.format(file_name))
        return cost_map

    shape = gpd.read_file(filepath)

    if shape.crs == None:
        print('WARNING: {} file is not georeferenced and will be disconsidered.'.format(file_name))
        return cost_map

    geom = [shapes.buffer(buffer) for shapes in shape.geometry]

    fill = 0
    if inside == 0:
        fill = cost
        cost = 0

    # add cost to raster according to the shapefile region
    rasterized = features.rasterize(geom,
                                out_shape = cost_map.shape,
                                fill = fill,
                                out = None,
                                transform = base_trans,
                                all_touched = False,
                                default_value = cost,
                                dtype = None)

    return cost_map + rasterized


def costmap(path_to_raster, path_to_constraints):
    
    # open raster file
    raster = rio.open(path_to_raster)
    cost_map = raster.read(1)
    base_proj = raster.crs
    base_trans = raster.transform
    
    if base_proj == None:
        raise Exception('Base map must be georeferenced')

    df_cons = pd.read_csv(path_to_constraints)

    for _, row in df_cons.iterrows():
        if row['consider']:
            cost_map = addCost(
                cost_map,
                os.path.join(os.path.dirname(path_to_constraints), row['filepath']),
                row['cost'],
                row['buffer'],
                row['inside'],
                base_trans
            )

    with rio.open(r'D:\PowerLineRouter\test\data\temp\costmap.tiff', 'w', **raster.profile) as ff:
        ff.write(cost_map,1)

    return cost_map




"""
    costmap.py

    script responsable for building the costmap
"""

import rasterio as rio
from rasterio import features, merge
import geopandas as gpd
import pandas as pd
import os

def addCost(cost_map, filepath, cost, buffer, inside, base_trans):
    # open shapefile
    file_name = os.path.basename(filepath)

    # check file
    if not os.path.exists(filepath):
        print('WARNING: {} file is missing and will be disconsidered.'.format(file_name))
        return cost_map

    # read shape
    shape = gpd.read_file(filepath)

    # check CRS
    if shape.crs == None:
        print('WARNING: {} file is not georeferenced and will be disconsidered.'.format(file_name))
        return cost_map

    # add buffer
    if buffer > 0.0:
        geom = [shapes.buffer(buffer) for shapes in shape.geometry]

    # swap
    fill = 0
    if inside == 0:
        fill, cost = cost, fill

    # add cost to raster according to the shapefile region
    rasterized = features.rasterize(geom                   ,
                                out_shape = cost_map.shape ,
                                fill = fill                , # value outside geometry
                                out = None                 ,
                                transform = base_trans     ,
                                all_touched = False        ,
                                default_value = cost       , # value whitin geometry
                                dtype = None)

    return cost_map + rasterized


def costmap(case_path):

    path_to_raster = os.path.join(case_path, 'basemap', 'slope_150m.tif')
    path_to_costmap = os.path.join(case_path, 'costmap', 'costmap.tif')
    path_to_constraints = os.path.join(case_path, 'constraints.csv')
    
    # open raster file
    raster = rio.open(path_to_raster)
    cost_map = raster.read(1)
    
    # check crs
    if raster.crs == None:
        raise Exception('Base map must be georeferenced')

    # read list of spatial constraints
    df_cons = pd.read_csv(path_to_constraints)

    # iterate over list and update cost map accordingly
    for _, row in df_cons.iterrows():
        if row['consider']:
            cost_map = addCost(
                cost_map,
                os.path.join(os.path.dirname(path_to_constraints), row['filepath']),
                row['cost'],
                row['buffer'],
                row['inside'],
                raster.transform
            )

    # write final cost map
    with rio.open(path_to_costmap, 'w', **raster.profile) as ff:
        ff.write(cost_map,1)

    return rio.open(path_to_costmap)

# associação dos pontos com as céluluas do raster (matriz)
def get_raster_cell(raster, point):
    
    costmap = raster.read(1)
    x, y = 1, 1
    costmap[x,y]

    return [x,y]
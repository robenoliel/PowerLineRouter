"""
    costmap.py

    script responsable for building the costmap
"""

from concurrent.futures.process import _chain_from_iterable_of_lists
import rasterio as rio
from rasterio import features, merge
from rasterio.windows import Window
import geopandas as gpd
import pandas as pd
import os
from geoprocessing.raster import *


def crop_raster(start_xy, stop_xy, raster):

    gt = raster.transform
    pixelSizeX = gt[0]
    pixelSizeY =-gt[4]

    extraSize = 1000 #meters
    extraPixelsX = int(extraSize/pixelSizeX)
    extraPixelsY = int(extraSize/pixelSizeY)
    
    xoff = start_xy[0] if start_xy[0] < stop_xy[0] else stop_xy[0]
    yoff = start_xy[1] if start_xy[1] < stop_xy[1] else stop_xy[1]

    xsize = abs(start_xy[0] - stop_xy[0])
    ysize = abs(start_xy[1] - stop_xy[1])

    xoff_extra = (xoff - extraPixelsX) if (xoff - extraPixelsX) > 0 else 0
    yoff_extra = (yoff - extraPixelsY) if (yoff - extraPixelsY) > 0 else 0

    xsize_extra = (xsize + extraPixelsX) if (xoff_extra + xsize + extraPixelsX) < raster.read(1).shape[0] else raster.read(1).shape[0] - xoff_extra
    ysize_extra = (ysize + extraPixelsY) if (yoff_extra + ysize + extraPixelsY) < raster.read(1).shape[1] else raster.read(1).shape[1] - yoff_extra
    
    window = Window(xoff_extra, yoff_extra, xsize_extra, ysize_extra)
    transform = raster.window_transform(window)
    profile = raster.profile
    profile.update({
        'height': xsize_extra,
        'width': ysize_extra,
        'transform': transform})

    return window, profile


def addCost(cost_map, filepath, cost, buffer, inside, base_trans, base_crs):
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

    if shape.crs != base_crs:
        shape = shape.to_crs(base_crs)

    # add buffer
    if buffer > 0.0:
        geom = [shapes.buffer(buffer) for shapes in shape.geometry]
    else:
        geom = shape.geometry

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

def getStartStop(case_path, base_raster, case_id):

    path_to_parameters = os.path.join(case_path, 'parameters.csv')
    df = pd.read_csv(path_to_parameters)
    id_candidate = df[df['id_case'] == case_id]['id_candidate'][0]
    path_to_candidates = os.path.join(case_path, 'candidates.csv')
    df = pd.read_csv(path_to_candidates)

    df_cand = df[df['id_candidate'] == id_candidate]

    start_lat, start_lon = df_cand['x_src'].values[0], df_cand['y_src'].values[0]
    stop_lat, stop_lon = df_cand['x_dst'].values[0], df_cand['y_dst'].values[0]

    if np.isnan(start_lat) or np.isnan(start_lon) or np.isnan(stop_lat) or np.isnan(stop_lon):
        raise Exception('Source or destination coordinates are missing')

    start_xy = get_xy_from_coordinates(start_lat, start_lon, base_raster)
    stop_xy = get_xy_from_coordinates(stop_lat, stop_lon, base_raster)
    
    return start_xy, stop_xy


def getPathToBaseRaster(case_path, case_id):

    path_to_parameters = os.path.join(case_path, 'parameters.csv')
    df = pd.read_csv(path_to_parameters)
    map_id = df[df['id_case'] == case_id]['id_map'][0]
    path_to_maps = os.path.join(case_path, 'maps.csv')
    df = pd.read_csv(path_to_maps)
    return os.path.join(case_path, df[df['id_map'] == map_id]['filepath'][0])


def costmap(case_path, case_id, study):

    path_to_raster = getPathToBaseRaster(case_path, case_id)
    path_to_costmap = os.path.join(case_path, 'costmap', 'costmap.tif')
    path_to_costmap_temp = os.path.join(case_path, 'costmap', 'costmap_temp.tif')
    path_to_constraints = os.path.join(case_path, 'constraints.csv')
    path_to_candidates = os.path.join(case_path, 'candidates.csv')

    # open raster file
    raster = rio.open(path_to_raster)

    #crop raster
    start_xy, stop_xy = getStartStop(case_path, raster, case_id)
    study.start = start_xy
    study.stop = stop_xy

    window, profile = crop_raster(start_xy, stop_xy, raster)

    with rio.open(path_to_costmap_temp, 'w', **profile) as ff:
        ff.write(raster.read(window = window))

    #load cropped raster
    raster = rio.open(path_to_costmap_temp)
    cost_map = raster.read(1)
    
    # check crs
    if raster.crs == None:
        raise Exception('Base map must be georeferenced')

    # read list of spatial constraints
    df_cons = pd.read_csv(path_to_constraints)

    # iterate over list and update cost map accordingly
    for _, row in df_cons.iterrows():
        if row['consider']:

            print("> adding layer: " + row['filepath'])

            cost_map = addCost(
                cost_map,
                os.path.join(os.path.dirname(path_to_constraints), row['filepath']),
                row['cost'],
                row['buffer'],
                row['inside'],
                raster.transform,
                raster.crs
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
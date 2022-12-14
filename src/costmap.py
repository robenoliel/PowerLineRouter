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
import geoprocessing.shapefile as sf
import math
from affine import Affine
from tqdm import tqdm


def crop_raster(start_xy, stop_xy, raster, extra_size=1000):
    """
    Crops a raster according to the routing starting and stopping points, so computing effort won't be wasted on uninteresting areas. Parameters:
        start_xy: Matrix coordinates (x,y) of the starting point (tuple)
        stop_xy: Matrix coordinates (x,y) of the stopping point (tuple)
        raster: the rasterio reader of the raster basemap (DatasetReader)
        extra_size: adds a margin to the cropped map (int)
    Returns:
        window_array: the array corresponding to the cropped map (ndarray)
        profile: the raster transform (affine)
        start_xy_new: the new starting point matrix coordinates at the cropped map (tuple)
        stop_xy_new: the new stopping point matrix coordinates at the cropped map(tuple)
    """


    print(rio.transform.xy(raster.transform, start_xy[0], start_xy[1]))
    start_ll = rio.transform.xy(raster.transform, start_xy[0], start_xy[1])
    stop_ll = rio.transform.xy(raster.transform, stop_xy[0], stop_xy[1])

    print(raster.crs)

    sf.export_point(start_ll[0],start_ll[1],r'D:\PowerLineRouter\test\data\01_RJ_SE1\temporary\start')
    sf.export_point(stop_ll[0],stop_ll[1],r'D:\PowerLineRouter\test\data\01_RJ_SE1\temporary\stop')

    gt = raster.transform
    pixelSizeX = gt[0]
    pixelSizeY =-gt[4]

    extraPixelsX = int(extra_size/pixelSizeX)
    extraPixelsY = int(extra_size/pixelSizeY)
    
    xoff = start_xy[0] if start_xy[0] < stop_xy[0] else stop_xy[0]
    yoff = start_xy[1] if start_xy[1] < stop_xy[1] else stop_xy[1]

    xsize = abs(start_xy[0] - stop_xy[0])
    ysize = abs(start_xy[1] - stop_xy[1])

    xoff_extra = (xoff - extraPixelsX) if (xoff - extraPixelsX) > 0 else 0
    yoff_extra = (yoff - extraPixelsY) if (yoff - extraPixelsY) > 0 else 0

    start_xy_new = (start_xy[0] - xoff_extra, start_xy[1] - yoff_extra)
    stop_xy_new = (stop_xy[0] - xoff_extra, stop_xy[1] - yoff_extra)

    #start_rc_new = [start_xy_new[1], start_xy_new[0]]
    #stop_rc_new = [stop_xy_new[1], stop_xy_new[0]]

    xsize_extra = (xsize + extraPixelsX + xoff - xoff_extra) if (xoff + xsize + extraPixelsX) < raster.read(1).shape[1] else raster.read(1).shape[1] - xoff_extra
    ysize_extra = (ysize + extraPixelsY + yoff - yoff_extra) if (yoff + ysize + extraPixelsY) < raster.read(1).shape[0] else raster.read(1).shape[0] - yoff_extra
    
    #xoff_extra = 0
    #yoff_extra = 0
    #xsize_extra = math.floor(raster.read(1).shape[0]/2)
    #ysize_extra = raster.read(1).shape[1]

    window_array = raster.read(1)[xoff_extra:xoff_extra+xsize_extra,yoff_extra:yoff_extra+ysize_extra]

    #profile = raster.profile
    #profile.update({
    #    'height': xsize_extra,
    #    'width': ysize_extra})

    window = Window(xoff_extra, yoff_extra, xsize_extra, ysize_extra)
    print(raster.transform)
    #transform = raster.window_transform(window)
    transform = raster.transform
    print(transform[0])
    upperleft = rio.transform.xy(raster.transform, xoff_extra, yoff_extra)
    transform = Affine(transform[0], transform[1], upperleft[0], transform[3], transform[4], upperleft[1])
    print(transform)
    profile = raster.profile
    profile.update({
        'height': xsize_extra,
        'width': ysize_extra,
        'transform': transform})

    return window_array, profile, start_xy_new, stop_xy_new

def addCost(cost_map, constraint, base_trans, base_crs):
    """
    Adds to the costmap the value corresponding to a constraint geometry. Parameters:
        costmap: costmap array (ndarray)
        constraint: constraint object (Constraint)
        base_trans: the basemap transform (affine)
        base_crs: the basemap crs (str)
    Returns:
        costmap: costmap array (ndarray)
    """

    cost = constraint.cost
    buffer = constraint.buffer
    inside = constraint.inside

    # read shape
    shape = constraint.geometry

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

def getStartStop(study):
    """
    Retrieves the study's matrix coordinates of its starting and stopping points. Parameters:
        study: study object (Study)
    Returns:
        start_xy: matrix coordinates of the starting point (tuple)
        stop_xy: matrix coordinates of the stopping point (tuple)
    """

    start_lat, start_lon = study.start[0], study.start[1]
    stop_lat, stop_lon = study.stop[0], study.stop[1]

    if np.isnan(start_lat) or np.isnan(start_lon) or np.isnan(stop_lat) or np.isnan(stop_lon):
        raise Exception('Source or destination coordinates are missing')

    start_xy = get_xy_from_coordinates(start_lat, start_lon, study.base_map.io)
    stop_xy = get_xy_from_coordinates(stop_lat, stop_lon, study.base_map.io)
    
    return start_xy, stop_xy

def getPathToBaseRaster(case_path, case_id):

    path_to_parameters = os.path.join(case_path, 'parameters.csv')
    df = pd.read_csv(path_to_parameters)
    map_id = df[df['id_case'] == case_id]['id_map'][0]
    path_to_maps = os.path.join(case_path, 'maps.csv')
    df = pd.read_csv(path_to_maps)
    return os.path.join(case_path, df[df['id_map'] == map_id]['filepath'][0])

def costmap(case, study):
    """
    Generates the study's costmap. Parameters:
        case: case object (Case)
        study: study object (Study)
    Returns:
        costmap: the rasterio reader of the raster costmap (DatasetReader)
    """

    path_to_costmap = os.path.join(case.path_to_case, 'costmap', 'costmap.tif')
    path_to_costmap_temp = os.path.join(case.path_to_case, 'costmap', 'costmap_temp.tif')

    # open raster file
    raster = study.base_map.io

    #crop raster
    start_xy, stop_xy = getStartStop(study)

    coords_start = rio.transform.xy(raster.transform, start_xy[0], start_xy[1])
    coords_stop  = rio.transform.xy(raster.transform, stop_xy[0] , stop_xy[1] )

    window, profile, start_xy_new, stop_xy_new = crop_raster(start_xy, stop_xy, raster, extra_size=1000)
    study.start = start_xy_new
    study.stop = stop_xy_new

    with rio.open(path_to_costmap_temp, 'w', **profile) as ff:
        ff.write(window,1)

    #load cropped raster
    raster   = rio.open(path_to_costmap_temp)
    coords_start_new = rio.transform.xy(raster.transform, study.start[0], study.start[1])
    coords_stop_new  = rio.transform.xy(raster.transform, study.stop[0] , study.stop[1] )

    cost_map = (raster.read(1) * 0.0) + study.base_cost
    
    # check crs
    if study.base_crs == None:
        raise Exception('Base map must be georeferenced')

    # read list of spatial constraints
    #df_cons = pd.read_csv(path_to_constraints)

    # iterate over list and update cost map accordingly
    for const in tqdm(study.spatial_constraints, desc = 'Loading constraints to costmap'):

        #print("> adding layer: " + row['filepath'])

        cost_map = addCost(
            cost_map,
            const,
            raster.transform,
            raster.crs
        )

    # calculate distance map
    dist_map = distmap(raster)

    # calculate $ cost map from $/km estimates
    cost_map *= dist_map 

    # write final cost map
    with rio.open(path_to_costmap, 'w', **raster.profile) as ff:
        ff.write(cost_map,1)

    return rio.open(path_to_costmap)

def distmap(raster):
    
    # resolu????o do raster (m)
    r, _ = raster.res

    # converter declividade para dist??ncia
    return np.sqrt(1 + raster.read(1)) * r

# associa????o dos pontos com as c??luluas do raster (matriz)
def get_raster_cell(raster, point):
    
    costmap = raster.read(1)
    x, y = 1, 1
    costmap[x,y]

    return [x,y]
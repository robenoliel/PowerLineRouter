"""
    costmap.py

    script responsable for building the costmap
"""
def costmap(path_to_raster, path_to_shape, cost):
    
    # open raster file
    raster = open_raster(path_to_raster)

    # open shapefile
    shape  = open_shape(path_to_shape)

    # add cost to raster according to the shapefile region
    raster_mod = add_cost_to_raster(raster, shape, cost)

    return raster_mod

def add_cost_to_raster(raster, shape, cost):
    return raster


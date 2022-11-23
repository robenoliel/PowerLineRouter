"""
    main.py

    script responsable for handling the software's workflow
"""

import os
os.chdir("src")
import classes
import io, log
import support
import router
import engineering.eng_tools as engt
import sys
import costmap
import rasterio as rio
import argparse
import algorithms.graph as grp
import algorithms.dijkstra as djk
import geoprocessing.shapefile as sf
import numpy as np
import support as spp
from classes import *
from algorithms.graph import *

def main():

    sys.path.append('geoprocessing')
    sys.path.append('engineering')
    sys.path.append('algorithms')

    #parser = argparse.ArgumentParser()
    #parser.add_argument('--path', type=str, required=True)

    # --- define path to case
    case_path = r'D:\PowerLineRouter\test\data\01_RJ_SE1'
    case_id = 1
    study = Study()
    #case_path = parser.parse_args().path

    # --- creates dir structure
    spp.setDirs(case_path)

    # --- build cost map
    print('1. Generating cost map')
    cost = costmap.costmap(case_path, case_id, study)
    print(study.start, study.stop)
    s = get_pos_from_coords(study.start, cost.read(1).shape)
    t = get_pos_from_coords(study.stop, cost.read(1).shape)
    W = cost.read(1)#[0:100, 0:90]
    
    # --- convert to graph
    print('2. Converting to graph structure')
    G, O = grp.matrix_to_weighted_graph(W)

    # --- 
    # s, t = find_source_and_taget_nodes(cost, coord_from, coord_to)
    s, t = 1071, 8190

    # --- find shortest path
    print('3. Run shortest path algorithm')
    dists, parents = djk.dijkstra(G, s, t)
    route_n = djk.get_dijkstra_path(parents, t)

    # --- convert nodes to matrix coordindates
    route_xy = [grp.get_coords_from_pos(node, W.shape) for node in route_n]

    # --- convert to spatial coordinates
    spline = sf.path_coords_to_polyline(route_xy, cost.transform, cost.crs)

    out_path = os.path.join(case_path, 'routes','optroute','case_' + str(case_id))
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    spline.to_file(os.path.join(out_path,'optroute.shp'))
    
    # --- export to shapefile
    # export shapefile here

    



    # --- reading execution parameters
    #log.console_print("reading execution parameters")
    #substations = engt.readSubstations(case_path)
    
    #transmission_lines = engt.readTransmissionLines(case_path, substations)
    #t1 = transmission_lines[0]

    # console_print("reading execution parameters")
    # classes.py
    # exc = read_execution(pathcase)

    # --- reading bus elements
    # console_print("reading bus elements")
    # ???.py
    # bus = psr_read_bus(pathcase)

    # --- reading circuit elements
    # console_print("reading circuit elements")
    # ???.py
    # cir = psr_read_circuit(pathcase)

    # --- reading constraint elements
    # console_print("reading constraint elements")
    # ???.py
    # ctr = read_constraints(pathcase, exc, cnd)

    # --- reading study map
    # console_print("reading map elements")
    # raster.py
    # map = read_map(pathcase, exc, cnd)

    # --- building cost map
    # console_print("building cost map")
    # costmap.py
    # cmp = build_costmap(exc, cnd, map, ctr)

    # --- find optimal route
    # console_print("optimizing route")
    # router.py 
    # rte <- optimize_route(exc, cnd, cmp)

    # --- find optimal 
    # console_print("exporting route")
    # io.py
    # export_optimal_routes(pathcase, 
    #                     list(SpatialLinesDataFrame(sl = rte, data = data.frame(line_id=1))),
    #                     as.geojson=F, ref_proj=projections_list$WGS84)

if __name__ == '__main__':
    main()


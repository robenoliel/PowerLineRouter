"""
    main.py

    script responsable for handling the software's workflow
"""

import classes
import io, log
import os
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

def main():

    sys.path.append('geoprocessing')
    sys.path.append('engineering')
    sys.path.append('algorithms')

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True)

    # --- define path to case
    #r'D:\PowerLineRouter\test\data\case_wgs84_utm_24'
    case_path = parser.parse_args().path

    # --- creates dir structure
    spp.setDirs(case_path)

    # --- build cost map
    

    cost = costmap.costmap(case_path)
    print('1')
    # --- convert to graph
    G, O = grp.matrix_to_weighted_graph(cost.read(1))
    print('2')

    # --- find shortest path
    s, t = 1, 2
    parents = djk.dijkstra(G, s, t)
    print('3')
    route_n = djk.get_dijkstra_path(parents, t)

    # --- convert nodes to matrix coordindates
    route_xy = [grp.get_coords_from_pos(node, (cost.width, cost.height) ) for node in route_n]

    # --- convert to spatial coordinates
    spline = sf.path_coords_to_polyline(route_xy, cost.transform)
    print(spline)
    
    # --- export to shapefile
    # export shapefile here

    








    # ---------------------------
    m = np.array([[1,2],[3,4]])
    print(grp.get_element(m, 3))
    print(grp.get_coords_from_pos(5, (3,3)))
    print(grp.get_pos_from_coords((2,2), (3,3)))
    # ---------------------------

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


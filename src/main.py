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

def main():

    sys.path.append('geoprocessing')
    sys.path.append('engineering')
    sys.path.append('algorithms')


    case_path = r'D:\PowerLineRouter\test\data\example_01'

    # --- reading execution parameters
    log.console_print("reading execution parameters")
    substations = engt.readSubstations(case_path)
    
    transmission_lines = engt.readTransmissionLines(case_path, substations)
    t1 = transmission_lines[0]

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


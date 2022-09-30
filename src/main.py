"""
    main.py

    script responsable for handling the software's workflow
"""

import classes
import io, log
import support
import router

def main():

    # --- reading execution parameters
    log.console_print("reading execution parameters")
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


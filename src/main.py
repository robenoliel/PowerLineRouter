"""
    main.py

    script responsable for handling the software's workflow
"""

import os
#os.chdir("src")
from classes import *
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
import logging as log
from distutils.util import strtobool
#from algorithms.graph import *

logger = log.getLogger(__name__)
handler = log.StreamHandler()
formatter = log.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--studies', help='delimited list input', nargs='?', type=lambda s: [int(item) for item in s.split(',')], required =False, const = [])
    parser.add_argument('-v', '--verbose', nargs='?', type = lambda x:bool(strtobool(x)), const = True)
    parser.add_argument('--path', type=str, required=True)
    args = parser.parse_args()
    case_path = args.path
    logger.setLevel(log.INFO if args.verbose else log.WARNING)
    handler.setLevel(log.INFO if args.verbose else log.WARNING)

    #case_path = r'D:\PowerLineRouter\test\data\01_RJ_SE1'
    plr = PowerLineRouter()
    logger.info('Loading case')
    plr.load_case(case_path)
    logger.info('Beginning power line routing')
    plr.run_router(studies=args.studies)
    logger.info('Routing complete, closing case')
    plr.close_case()

if __name__ == '__main__':
    main()


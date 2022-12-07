"""
    main.py

    script responsable for handling the software's workflow
"""

import os
os.chdir("src")
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
#from algorithms.graph import *

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--studies', help='delimited list input', type=lambda s: [int(item) for item in s.split(',')], required =False)
    parser.add_argument('--path', type=str, required=True)
    case_path = parser.parse_args().path

    #case_path = r'D:\PowerLineRouter\test\data\01_RJ_SE1'
    plr = PowerLineRouter()
    plr.load_case(case_path)
    plr.run_router()
    plr.close_case()

if __name__ == '__main__':
    main()


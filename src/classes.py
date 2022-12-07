"""
    classes.py

    script responsable for higher level classes 
"""

import os
import sys
import costmap
import pandas as pd
import rasterio as rio
import geopandas as gpd
import engineering.eng_tools as engt
import algorithms.graph as grp
import algorithms.dijkstra as djk
import geoprocessing.shapefile as sf
import numpy as np
import support as spp

from algorithms.graph import *
from shapely.geometry import Point
from classes import *

class PowerLineRouter:
    def __init__(self):
        self.case = None

    def load_case(self, path_to_case):
        self.case = Case(path_to_case)
        
    def run_router(self, studies = None):

        if self.case == None:
            raise Exception('ERROR: No case is loaded.')
        
        sys.path.append('geoprocessing')
        sys.path.append('engineering')
        sys.path.append('algorithms')

        # --- creates dir structure
        spp.setDirs(self.case.path_to_case)

        if studies == None:
            studies = self.case.studies
        else:
            studies = [study for study in self.case.studies if study.id in studies]
        
        for study in studies:

            # --- build cost map
            # logger.info('1. Generating cost map')
            
            print('1. Generating cost map')
            cost = costmap.costmap(self.case, study)
            source_node = get_pos_from_coords(study.start, cost.read(1).shape)
            target_node = get_pos_from_coords(study.stop, cost.read(1).shape)
            W = cost.read(1) # W = np.random.rand(3,3)

            # --- convert to graph
            print('2. Converting to graph structure')
            G, O = grp.matrix_to_weighted_graph(W)

            # # --- find shortest path
            print('3. Running shortest path algorithm')

            print('3.1 Run Dijkstra\'s algorithm')
            dists, parents = djk.dijkstra(G, source_node, target_node)

            print('3.2 Get optimal path')
            route_n = djk.get_dijkstra_path(parents, target_node)

            # # --- convert to spatial coordindates
            print('4. Exporting power line route')

            print('4.1 Node > Coords')
            route_xy = [grp.get_coords_from_pos(node, W.shape) for node in route_n]

            print('4.2 Coords > Line')
            spline   = sf.path_coords_to_polyline(route_xy, cost.transform, cost.crs)

            print('4.3 Line > .shp')
            out_path = os.path.join(self.case.path_to_case, 'routes','optroute','study_' + str(study.id))
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            spline.to_file(os.path.join(out_path,'optroute.shp'))

    def close_case(self):
        for study in self.case.studies:
            study.base_map.io.close()
            for map in study.maps:
                map.io.close()
        self.case = None

class Study:
    def __init__(self):
        self.id = None
        #self.name = None
        self.base_crs = None
        self.base_map = None
        self.start = None
        self.stop = None
        self.base_cost = None
        self.spatial_constraints = []
        self.maps = []

class Case:
    def __init__(self, path_to_case):
        #self.id = None
        self.studies = []
        #self.maps = []
        #self.spatial_constrains = []
        self.name = os.path.basename(path_to_case)
        self.path_to_case = path_to_case
        
        self._load_studies()

    def _load_studies(self):

        path_to_parameters = os.path.join(self.path_to_case, 'parameters.csv')
        path_to_candidates = os.path.join(self.path_to_case, 'candidates.csv')
        path_to_constraints = os.path.join(self.path_to_case, 'constraints.csv')
        path_to_maps = os.path.join(self.path_to_case, 'maps.csv')
        df_params = pd.read_csv(path_to_parameters)
        df_candidates = pd.read_csv(path_to_candidates)
        df_maps = pd.read_csv(path_to_maps)
        df_constraints = pd.read_csv(path_to_constraints)
        df_params = df_params.join(df_candidates, on = 'id_candidate', how = 'left', rsuffix = '_cand')

        for _, row in df_params.iterrows():
            study = Study()
            study.id = row['id_study']
            study.base_crs = row['projection']
            study.base_cost = row['base_cost']

            d = {'name': ['start', 'stop'], 'geometry': [Point(row['x_src'], row['y_src']), Point(row['x_dst'], row['y_dst'])]}
            gdf = gpd.GeoDataFrame(d, crs='WGS84')
            gdf = gdf.to_crs(study.base_crs)
            study.start = (gdf.loc[0,'geometry'].x, gdf.loc[0,'geometry'].y)
            study.stop = (gdf.loc[1,'geometry'].x, gdf.loc[1,'geometry'].y)

            for _, map_row in df_maps[df_maps['id_study'] == study.id].iterrows():
                map_path = os.path.join(self.path_to_case, map_row['filepath'])
                if not os.path.exists(map_path):
                    file_name = os.path.basename(map_path)
                    if map.type == 'basemap':
                        raise Exception('ERROR: {} file is missing.'.format(file_name))
                    else:
                        # logger.warning('{} file is missing and will be disconsidered.'.format(file_name))
                        continue
                map = Map()
                map.id = map_row['id_map']
                map.type = map_row['type']
                map.io = rio.open(map_path)
                if map.type == 'basemap':
                    study.base_map = map
                else:
                    study.maps.append(map)

            for _, constraint_row in df_constraints[df_constraints['id_study'] == study.id].iterrows():
                if constraint_row['consider'] == 1:
                    const_path = os.path.join(self.path_to_case, constraint_row['filepath'])
                    if not os.path.exists(const_path):
                        file_name = os.path.basename(const_path)
                        # logger.warning('WARNING: {} file is missing and will be disconsidered.'.format(file_name))
                        continue
                    constraint = SpatialConstraint()
                    constraint.id = constraint_row['id_constraint']
                    constraint.type = constraint_row['type']
                    constraint.cost = constraint_row['cost']
                    constraint.inside = constraint_row['inside']
                    constraint.buffer = constraint_row['buffer']
                    map_path = os.path.join(self.path_to_case, map_row['filepath'])
                    constraint.geometry = gpd.read_file(const_path)
                    study.spatial_constraints.append(constraint)

            self.studies.append(study)

class SpatialConstraint:
    def __init__(self):
        self.id = None
        self.name = None
        self.additional_cost = None
        self.inside = True
        self.buffer = 0
        self.geometry = None

class Map:
    def __init__(self):
        self.id = None
        self.io = None
        self.type = None


class Execution:
    def __init__(self):
        self.casepath = ""
        self.casepath = ""

    def add(self, casepath):
        self.casepath = casepath
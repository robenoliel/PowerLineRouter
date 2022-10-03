import pandas as pd
import numpy as np
import os
from engineering.eng_classes import Substation, TransmissionLine
from geoprocessing.geo_classes import Coordinate

def metadataSubstation():
    return {
        'id': np.int64,
        'name': str,
        'voltage':np.float64,
        'lat':np.float64,
        'lon':np.float64
    }

def metadataTransmissionLine():
    return {
        'id': np.int64,
        'name': str,
        'sub_id_from':np.int64,
        'sub_id_to':np.int64,
        'run':np.int64,
        'lat':str,
        'lon':str
    }


def readTransmissionLines(case_path, substations):
    '''
    Reads TransmissionLine objects from case files
    '''

    file_path = os.path.join(case_path, 'transmission_line.csv')
    md = metadataTransmissionLine()
    df = pd.read_csv(file_path, dtype = md)
    print(df)

    transmissionLines = []
    for _, row in df.iterrows():

        id = row['id']
        name = row['name']
        sub_from = [sub for sub in substations if sub.id == row['sub_id_from']][0]
        sub_to = [sub for sub in substations if sub.id == row['sub_id_to']][0]

        if row['run'] != 0 and row['run'] != 1:
            raise Exception('`run` parameter must be either 1 or 0')
        run_router = True if row['run'] == 1 else False

        coordinates = []
        lat = [np.float64(val) for val in row['lat'].split(' ')]
        lon = [np.float64(val) for val in row['lon'].split(' ')]
        if len(lat) != len(lon):
            raise Exception('`lat` and `lon` must have the same length')
        for i in range(len(lat)):
            coord = Coordinate()
            coord.add(lat[i], lon[i])
            coordinates.append(coord)

        tl = TransmissionLine()
        tl.add(
            id,
            name,
            sub_from,
            sub_to,
            coordinates,
            run_router
        )
        transmissionLines.append(tl)

    return transmissionLines


def readSubstations(case_path):
    '''
    Reads Substation objects from case files
    '''

    file_path = os.path.join(case_path, 'substation.csv')
    md = metadataSubstation()
    df = pd.read_csv(file_path, dtype = md)

    substations = []
    for _, row in df.iterrows():

        id = row['id']
        name = row['name']
        voltage = row['voltage']
        coord = Coordinate()
        coordinate = coord.add(row['lat'], row['lon'])

        sub = Substation()
        sub.add(
            id,
            name,
            voltage,
            coordinate
        )
        substations.append(sub)

    return substations
    

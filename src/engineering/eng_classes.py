"""
    eng_classes.py

    script responsable for building the 
"""

from geoprocessing import geo_classes as geo

class Substation:
    def __init__(self):
        self.id          = 0
        self.name        = ""
        self.voltage     = 0
        self.coordinate  = geo.Coordinate()

    def add(self, id, name, voltage, coordinate):
        self.id          = id
        self.name        = name
        self.voltage     = voltage
        self.coordinate = coordinate    


class TransmissionLine:
    def __init__(self):
        self.id          = 0
        self.name        = ""
        self.sub_from    = Substation()
        self.sub_to      = Substation()
        self.coordinates = []
        self.run_router  = False


    def add(self, id, name, sub_from, sub_to, coordinates, run_router):
        self.id          = id
        self.name        = name
        self.sub_from    = sub_from
        self.sub_to      = sub_to
        self.coordinates = coordinates
        self.run_router  = run_router
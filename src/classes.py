"""
    classes.py

    script responsable for higher level classes 
"""

class Study:
    def __init__(self):
        self.start = None
        self.stop = None

class PowerLineRouter:
    def __init__(self):
        self.casepath = ""

    def add(self, casepath):
        self.casepath = casepath


class Execution:
    def __init__(self):
        self.casepath = ""
        self.casepath = ""

    def add(self, casepath):
        self.casepath = casepath

class SpatialConstraint:
    def __init__(self):
        self.cost    = 1.0
        self.type    = ""  # point, line, polygon
        self.buffer  = 0.0
        self.active  = False
        self.element = []

    def add(self, cost, type, buffer, active, element):
        self.cost    = cost
        self.type    = type
        self.buffer  = buffer
        self.active  = active
        self.element = element
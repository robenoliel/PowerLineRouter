"""
    geo_classes.py

    script responsable for building the 
"""

class Coordinate:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
    
    def add(self, x, y):
        self.x = x
        self.y = y
    
    def convert(self, projection):
        """
            should we add a method for converting coordinates according to projections?
        """
        self.x = self.x
        self.y = self.y

"""
    support.py

    script responsable for auxiliary functions
"""

import os

def setDirs(case_path):
    dirs = ['basemap', 'candidates', 'corridor', 'costmap', 'enviromental', 'facilities', 'limits', 'railways', 'results', 'routes', 'temporary', 'transmission', 'urban']
    for dir in dirs:
        path = os.path.join(case_path, dir)
        isExist = os.path.exists(path)
        if not isExist:
           os.makedirs(path)
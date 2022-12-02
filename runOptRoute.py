import os
os.chdir("src")
import sys
import argparse
from src.classes import *

def main():

    sys.path.append('src')
    
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
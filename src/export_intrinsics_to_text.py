# Please use colmap\scripts\python\database.py to import the txt file created by this script
import json
import os
from os import walk
from os.path import isfile, join


def main(path):
  file_path, filename = os.path.split(path)
  with open(path, 'r') as f:
    views = json.load(f)
  
  with open(os.path.join(file_path+"/cam_intrin.txt"), 'w+') as file:
    for i in range(45): # since there are 46 cameras
      view = views[i]
      
      file.write("{0} RADIAL_FISHEYE 2560 1920 {1}, {2}, {3}, {4}, {5}\n".format(
        i+1, 
        view['focal_length'], 
        view['principal_point'][0], view['principal_point'][1], 
        view['radial_distortion'][0], view['radial_distortion'][0])
        )
      
if __name__ == "__main__":
  import sys
  main(sys.argv[1])


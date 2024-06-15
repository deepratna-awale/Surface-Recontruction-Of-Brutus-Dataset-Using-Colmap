# Undistort without intrinsics
# Execute this file with the path of dir containing the distorted images.
# An 'Undistorted' dir would be created in the same directory  

from defisheye import Defisheye
import os
from os import walk
from os.path import join

def undistort(source_img):
    dtype = 'linear'
    format = 'fullframe'
    
    fov = 180
    pfov = 120

    obj = Defisheye(source_img, dtype=dtype, format=format, fov=fov, pfov=pfov)
    return obj


def main(file_directory):
    # Get filenames of all distorted images  
    files = []    
    for (dirpath, dirnames, filenames) in walk(file_directory):
        files.extend(filenames)
        break
    print(f"{len(files)} images found.")

    # Make a new directory for Undistorted Images
    undistorted_img_dir = os.path.join(dirpath, "Undistorted")
    if not os.path.isdir(undistorted_img_dir):
        os.mkdir(undistorted_img_dir)
    print(f"Created directory 'Undistorted' at: {dirpath}")
    
    print("\nUndistorting images...")
    for file in files:
        source_img = os.path.join(dirpath, file)
        filename, ext = os.path.splitext(file) #seperate file name and extension
        destination_img = os.path.join(undistorted_img_dir, f"{filename}{ext}")
        obj = undistort(source_img)
        obj.convert(destination_img)
        print(f"Undistorted {destination_img}.")

if __name__ == "__main__":
    import sys
    source_directory = sys.argv[1]
    main(source_directory)
    print("Done.")
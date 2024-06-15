import argparse
import json
import os
import sys
sys.path.append('../')

import numpy as np

import database as colmapDB


def CreateDB():
    path = "D:\Downloads\Data\01_Welder\models.json"
    file_path, filename = os.path.split(path)

    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", default="database.db")
    args = parser.parse_args()

    with open(path, 'r') as f:
        views = json.load(f)

    if os.path.exists(args.database_path):
        print("ERROR: database path already exists -- will not modify it.")
        return

    db = colmapDB.COLMAPDatabase.connect(args.database_path)
    db.create_tables()

    for i in range(45):  # since there are 46 cameras
        view = views[i]
        model, width, height, params = \
            2, 2560, 1920, np.array((view['focal_length'],
                                     view['principal_point'][0], view['principal_point'][1],
                                     view['radial_distortion'][0], view['radial_distortion'][0]))
        camera_id = db.add_camera(model, width, height, params)
        image_id = db.add_image(
            ("D:\Downloads\Data\01_Welder\Frames\camera_{:04d}").format(i), camera_id)
    
    db.commit()

if __name__ == "__main__":
    CreateDB()    


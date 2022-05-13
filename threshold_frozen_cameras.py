# remove all cameras from the list with >= 10 frozen weeks ("frozen" determined by camera_filter.py on Cooley)

import argparse
import json

CAMERAS_V2 = 'cameras_v2.json'

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Remove cameras with >= 10 frozen weeks. Save a new output json')
    parser.add_argument('--file', '-f', type=str, help='Dictionary of {camera_id: num_frozen_weeks}')

    args = parser.parse_args()

    camera_dict = {}
    with open(args.file, 'r') as f:
        camera_dict = json.load(f)

    # list of cameras with less than 10 frozen weeks
    new_camera_dict = {}
    for camera_id, num_frozen in camera_dict.items():
        if num_frozen < 10:
            new_camera_dict[camera_id] = num_frozen

    with open(CAMERAS_V2, 'w') as f:
        json.dump(new_camera_dict, f)

    print('Done')



import json
import os
import csv
import argparse

import camera_filter
import classif_cams-gpu
import place_country


def main():

    # USAGE:
    # 
    # camera_vetting_pipeline.py takes in the arguments:
    #   - cameras_parent_dir: path to directory containing all the camera folders
    #   - name of file with country code CSVs
    #   - database_link
    #
    # and outputs analysis_cameras.json, which is a json 
    # containing the camera id's and all relevent metadata
    # if you run into any problems please file an issue on github,
    # and/or send an email to shane@allcroft.net

    parser = argparse.ArgumentParser()
    parser.add_argument('--cameras_parent_dir', help='a path to a directory containing all the camera folders, where all the camera subdirectories contain properly named raw image data', default=None)
    parser.add_argument('--database_link', default=None)
    parser.add_argument('--camera_metadata_csv', help='a path to a locally stored camera metadata file in csv format', default=None)
    parser.add_argument('--analysis_regions', help='string of region codes for geographical regions of interest for analysis, values separated by "."s default is all regions', default='')
    
    args = parser.parse_args()

    camera_db_dir = args.cameras_parent_dir
    db_link = args.database_link
    camera_metadata_csv_path = args.camera_metadata_csv
    analysis_regions_str = args.analysis_regions
    analysis_regions_list = analysis_regions_str.split('.')

    analysis_cams = {}
    with open(camera_metadata_csv_path) as f:
        analysis_cams = dict(filter(None, csv.reader(f)))
        

    # STEP 1: FILTER OUT DEAD/OFFLINE CAMERAS
    frozen_cameras = camera_filter.filter_cameras(len(analysis_cams.keys()), time_granularity=35, acceptable_threshold=10, parent_directory=camera_db_dir)
    for frozen_cam_id in frozen_cameras.keys():
        # remove frozen cams from the analysis pool
        analysis_cams.pop(frozen_cam_id)

    # STEP 2: Run classification on cameras
    cam_pred_dict = classif_cams_gpu(db_link)
    combined_dictionary = place_country.filter_by_place(cam_pred_dict)
    
    # STEP 3: Filter cameras based on countries of interest and place relevance
    for cam_id in analysis_cams.keys():
        if not cam_id in combined_dictionary.keys():
            analysis_cams.pop(cam_id)
            continue
        relevance_info = combined_dictionary[cam_id]
        country = relevance_info[1]
        if not country in analysis_regions_list:
            analysis_cams.pop(cam_id)
    
        
    for cam_id, relevance_info in combined_dictionary.items():
        country = relevance_info[1]
        if not not country in analysis_regions_list:
            
        
    # STEP 4:
    with open("analysis_cameras.json", "w") as f:
        json.dump(combined_dictionary, f)

        
if __name__ == '__main__':
    main()

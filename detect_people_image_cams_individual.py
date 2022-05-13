#!/usr/bin/env python

import json
import os
import argparse
import numpy as np
import cv2
import torch
import glob
from PIL import Image


from Tools.database_iterator_30kcams import database_iterator
from Tools.scene_detection_30kcams import SceneDetectionClass
from Pedestron.mmdet.apis import init_detector, inference_detector


if __name__ == "__main__":
    valid_cams = {}
    with open("cameras_v4_person_only.json", 'r') as fp:
        valid_cams = json.load(fp)
    parser = argparse.ArgumentParser(description='Run person detections on all videos')
    parser.add_argument('--config', help='test config file path', default='Pedestron/configs/elephant/cityperson/cascade_hrnet.py')
    parser.add_argument('--checkpoint', help='checkpoint file', default='Pedestron/models_pretrained/epoch_19.pth.stu')
    parser.add_argument('--path', help = 'path to videos', default='/eagle/SE_HPC/covid-images/')
    parser.add_argument('--camera', required=True)
    parser.add_argument('--start_month', required=True)
    parser.add_argument('--end_month', required=True)
        
    args = parser.parse_args()
    
    start_month = int(args.start_month)
    end_month = int(args.end_month)
    if end_month == 1 or end_month == 2 or end_month == 3:
        end_month += 12
    if start_month == 1 or start_month == 2 or start_month == 3:
        start_month += 12

    cam = args.camera
    
    model = init_detector(
        args.config, args.checkpoint, device=torch.device('cuda:0'))

    path = args.path




    detections = {}

    detections[cam] = dict()

    for image in os.listdir(path + cam):
        month = int(image[30:32])
        day = int(image[33:35])
        year = int(image[25:29])
        if year == 2021:
            month += 12
        if not (month >= start_month and month <= end_month):
            continue
        detections[cam][image] = dict()
        f = open('individual_output_file.txt', 'w+')
        
        f.write('start month ' + str(start_month) + '\n')
        f.write('end month ' + str(end_month) + '\n')
        f.write('current_month ' + str(month) + '\n')
        f.close()
        try:
            pil_image = Image.open(path + cam + '/' + image)
            img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            # day night calculation


            results = inference_detector(model, img)
            if isinstance(results, tuple):
                bbox_result, segm_result = results
            else:
                bbox_result, segm_result = results, None
            bboxes = np.vstack(bbox_result)
            bboxes = bboxes.tolist()
            bbox_dict = dict()
            for each in bboxes:
                bbox_dict[each[4]] = each[0:4]
            detections[cam][image] = bbox_dict
        except:
            print('error on image')
            continue

        f = open("individual_cam_detect_folder/ALL_VALID_CAMERAS_person_detections_image" + str(cam)+ '.txt', "w+")
        f.write(json.dumps(detections))
        f.close()

    print('successfully output')

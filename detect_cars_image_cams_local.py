
# This script was written to be run many times
# in parallel as jobs on a computing cluster.
#
# I would recommended the use a bash script to
# call this script many times to
# iterate over a range of cameras.

import json
import argparse
import numpy as np
import cv2
import torch
import sys
import matplotlib.pyplot as plt
import time
# add the path ../ to import functions from the yolov3 module
sys.path.append("../")
sys.path.append("./")

from yolov3.utils.datasets import *
from yolov3.utils.utils import *
from yolov3.detect import Vehicle_Detector
from Tools.scene_detection_30kcams import SceneDetectionClass
from Tools.database_iterator_30kcams import database_iterator

WEIGHTS = 'yolov3/weights/yolov3-spp-ultralytics.pt'
CFG = 'yolov3/cfg/yolov3-spp.cfg'
NAMES = 'yolov3/data/coco.names'
IOU_THRES = 0.3
IMG_SIZE = 512
COUNTRY = 'AU'



if __name__ == "__main__":
    valid_cams = {}
    with open('cameras_v4.json', 'r') as fp:
        valid_cams = json.load(fp)

    with open('cameras_v3.json', 'r') as fp:
        cam_country = json.load(fp)
 


    parser = argparse.ArgumentParser(description='YOLO People Detector')
    parser.add_argument('--cfg', type=str,
                        default='yolov3/cfg/yolov3-spp.cfg', help='*.cfg path')
    parser.add_argument('--names', type=str,
                        default='yolov3/data/coco.names', help='*.names path')
    parser.add_argument('--weights', type=str,
                        default='yolov3/weights/yolov3-spp-ultralytics.pt', help='weights path')
    # input file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=512,
                        help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float,
                        default=0.2, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float,
                        default=0.3, help='IOU threshold for NMS')
    parser.add_argument('--half', action='store_true',
                        help='half precision FP16 inference')
    parser.add_argument('--device', default='0',
                        help='device id (i.e. 0 or 0,1) or cpu')
    parser.add_argument('--save-path', default='results',
                        help='directory to save results')                        
    parser.add_argument('--filename', default='filename',
                        help='filename to read data from')
    parser.add_argument('--month',type=int)

    args = parser.parse_args()
    args.cfg = check_file(args.cfg)  # check file
    args.names = check_file(args.names)  # check file
    file_to_read = args.filename
    print("Yolo for vehicle detection configuration:")
    print(args)
    directory_exists = os.path.isdir(args.save_path)
    if not directory_exists:
        os.mkdir(args.save_path)
        
    vehicle_detector = Vehicle_Detector(weights=WEIGHTS, cfg=CFG, names=NAMES, iou_thres=IOU_THRES,conf_thres=0.2, imgsz=IMG_SIZE, device_id='0')


    detections = dict()
    day_night = dict()
    count = 0
    text_file = open(file_to_read, 'r')
    lines = text_file.read().split('\n')
    cam_l = lines
    print(cam_l)
    cams = valid_cams.keys()
    
    filename = os.path.join("vehicle_detections_image_" + COUNTRY + "_augtodec.json")
    numcams = len(cams)
    count = 0
    for cam in cams:    
        if valid_cams[cam][0] == 'people':
            continue
        if cam_country[cam][1] != COUNTRY:
            continue
        count += 1
        print(cam)
        detections[cam] = dict()
        day_night[cam] = dict()
        counter = 0
        error_counter = 0

        detections[cam] = dict()
        day_night[cam] = dict()


        for image in os.listdir(os.path.join('./camera_images_temp/', cam)):
            month = int(image[30:32])
            day = int(image[33:35])
            year = int(image[25:29])

            if (month == 3 or month == 2 or month == 1):
                continue
            try:
                pil_image = Image.open(os.path.join('./camera_images_temp/', cam, image))
                img = np.array(pil_image)

                if img is None:
                    print('really peep this none')
                    continue
                results = vehicle_detector.detect(img, view_img=False)
                detections[cam][image] = results
                #print(results)
            except Exception as e:
                print('in exception ', e)
                continue

        print(str(count) + " out of " + str(numcams) + " cameras done.")

    f = open(filename, "w+")
    # write to the file at the end of every camera instead of when the entire process is complete
    # Helps if it gets disconnected in between
    f.write(json.dumps(detections))
    f.close()

    print("Done")

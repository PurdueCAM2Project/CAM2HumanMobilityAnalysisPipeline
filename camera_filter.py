#usage "python filter.py [multiple cameras 1 or 0 (yes or no)] [directory path] [minimum number of days]" where the first argument is a 1 or a 0, 1 denoting that the [directory path] should be treated as a parent directory containing folders each subfolder denoting a single camera, a 0 denotes that [directory path] is the path to the folder of a single camera [directory path] is replaced by the path of the directory you want to iterate over and number of days is the minimum number of days that a camera has to have usable data for to be considered viable 

import json
import cv2 as cv
import sys
import os
import numpy as np
import csv 
import pandas as pd
import argparse
import email

CAMERA_DICTIONARY = {}

PARENT_DIRECTORY = '/projects/SE_HPC/covid-images' # TODO 



def filter_cameras(number_of_cameras, time_granularity, acceptable_threshold=10, parent_directory=None):
    # we're analyzing multiple cameras, so we should iterate over all the subdirectories contained in the current directory
    if parent_directory:
        PARENT_DIRECTORY = parent_directory
    
    SAVED_ALREADY = False
    print('script starting')

    total_viable_cameras = 0
    total_unviable_cameras = 0
    counter = 0
    for camera_id in os.listdir(PARENT_DIRECTORY):
        counter += 1
        if counter > number_of_cameras:
            break
        if os.path.isdir(os.path.join(PARENT_DIRECTORY, camera_id)):
            # the number of unacceptable (frozen / dead frames found on the camera)
            unacceptable_count = inspect_camera(os.path.join(PARENT_DIRECTORY, camera_id), time_granularity)
            if unacceptable_count < acceptable_threshold:
                CAMERA_DICTIONARY[camera_id] = unacceptable_count
            #TODO stop in january !!!!!!!
            #print('Camera id:', camera_id)
            #print('Unacceptable count: ', unacceptable_count, '\n')
    #TODO output camera dictionary to csv 
    with open('jsons/camera_viability.json', 'w') as outfile:
        json.dump(CAMERA_DICTIONARY, outfile)
    return CAMERA_DICTIONARY

                    
def inspect_camera(directory_path, time_granularity):
    unacceptable_count = 0 
    #iterate over the directory for images
    sorted_filenames = sorted(os.listdir(directory_path))
    counter = 0
    first_image = None
    second_image = None
    for filename in sorted_filenames:
        date = filename.split('_')[1] 
        month = date[5:7]
        year = date[0:4]
        if month == '03' or year == '2021': # no march
            continue
        counter += 1       
        if counter % 3 == 0 and first_image is not None:            
            #print('second_image', filename)
            second_image = cv.imread(os.path.join(directory_path, filename), 0)
        elif counter % time_granularity == 0:
            #print('first_image', filename)
            first_image = cv.imread(os.path.join(directory_path, filename), 0)
        else:
            continue
        if first_image is not None and second_image is not None:
            first_image = crop_img(first_image)
            SAVED_ALREADY = True
            second_image = crop_img(second_image)
            #print(filename)
            if np.array_equal(first_image, second_image):
                unacceptable_count += 1
            first_image = None
            second_image = None
    return unacceptable_count
                
                
                    
def crop_img(image): #this image check function is incomplete TODO: implement further image scrutiny
    #to determine if the image is blurry see if it is a gaussian blur or laplacian blur
    #to subvert the fact that many many of the images have text alongside the border of the image, we will only analyze the middle of it
    dimensions = image.shape
    height = dimensions[0] 
    width = dimensions[1] 
    height = int(height/4)
    width = int(width/4)
    cropped_image = image[height:(3*height), width:(3*width)]
    #cv.imwrite('temp.png', cropped_image)
    return cropped_image


if __name__ == "__main__":
    parser = argparse.ArgumentParser('vet frozen cameras and offline camera streams')
    parser.add_argument('--number_of_cameras', '-n', type=int) # if -1, vet all cameras
    parser.add_argument('--time_granularity', '-t',type=int)
    parser.add_argument('--acceptable_threshold', '-at',type=int)
    args = parser.parse_args()
    
    filter_cameras(args.number_of_cameras, args.time_granularity, args.acceptable_threshold)

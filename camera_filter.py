#usage "python filter.py [multiple cameras 1 or 0 (yes or no)] [directory path] [minimum number of days]" where the first argument is a 1 or a 0, 1 denoting that the [directory path] should be treated as a parent directory containing folders each subfolder denoting a single camera, a 0 denotes that [directory path] is the path to the folder of a single camera [directory path] is replaced by the path of the directory you want to iterate over and number of days is the minimum number of days that a camera has to have usable data for to be considered viable 

import cv2 as cv
import sys
import os
import numpy as np
import csv 
import pandas as pd

CAMERA_DICTIONARY = {}

PARENT_DIRECTORY = '~cv/images/' # TODO 


def main():
    # we're analyzing multiple cameras, so we should iterate over all the subdirectories contained in the current directory
    parser = argparse.ArgumentParser('vet frozen cameras and offline camera streams')
    parser.add_argument('--number_of_cameras', '-n') # if -1, vet all cameras
    parser.add_argument('--time_granularity', '-t')
    parser.add_argument('--acceptable_threshold', '-at')
    args = parser.parse_args()
    total_viable_cameras = 0
    total_unviable_cameras = 0
    for camera_id in os.listdir(PARENT_DIRECTORY):
        if os.path.isdir(os.path.join(parent_directory_path, camera_id)):
            # the number of unacceptable (frozen / dead frames found on the camera)
            unacceptable_count = inspect_camera(os.path.join(camera_id), min_data_count_threshold)
            if unacceptable_count < args.acceptable_threshold:
                CAMERA_DICTIONARY[camera_id] = unacceptable_count
    #TODO output camera dictionary to csv 
    pd.to_csv(CAMERA_DICTIONARY,'cameras.csv')

                    
def inspect_camera(sample_size, min_data_count_threshold):
    unacceptable_count = 0 
    #iterate over the directory for images
    sorted_filenames = sorted(os.listdir(directory_path))
    counter = 0
    first_image = None
    second_image = None
    for filename in sorted_filenames:
        date = filename.split('_')[1] 
        month = date[5:6]
        if month == '03': # no march
            continue
        counter += 1
        if counter % 3 == 0:            
            if first_image is None:
                first_image = cv.imread(os.path.join(directory_path, filename), 0)
            else:
                second_image = cv.imread(os.path.join(directory_path, filename), 0)
        if first_image is not None and second_image is not None:
            first_image = crop_img(first_image)
            second_image = crop_img(second_image)
            if first_image == second_image:
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
    cropped_image = np.arange(1)
    cropped_image = cropped_image.reshape(height/2, width/2)
    #check for middle of image being all black / all white
    for i in range(height/2):
        for j in range(width/2):
            cropped_image[i][j] = image[i + (height/2)][j + (width/2)]
            
                

    return True


if __name__ == "__main__":
    main()

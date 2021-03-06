import numpy


def determine_day_night(image):  # determines whether or not an image is captured during the day or night
    # 0 denotes night, 1 denotes day
    return np.mean(image)

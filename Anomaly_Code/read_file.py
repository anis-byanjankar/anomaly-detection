import cv2
import numpy as np

def read_file(file_name):
    ''' Input: a video file name
        Output: frames and fps
    '''
    video = cv2.VideoCapture(file_name)
    fps = video.get(cv2.CAP_PROP_FPS)
    success,image = video.read()
    count = 0
    success = True
    frames = []
    while success:
        frames.append(image)
        success,image = video.read()
        count += 1
    return frames, fps

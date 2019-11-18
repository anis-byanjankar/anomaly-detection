import os
from extract_pixel import *

def compute_features(frame, topleft, bottomright):
    ''' Input: frame - a specific frame
               topleft - y, x coordinates of topleft point of the tile
               bottomright - y, x coordinates of bottomright point of the tile
        Output: one row of vector with all the features
    '''
    pixel_data = extract_pixel(frame, topleft, bottomright)
    blue = pixel_data[::,0]
    green = pixel_data[::,1]
    red = pixel_data[::,2]
    features = []
    features.append(np.mean(red))
    features.append(np.mean(green))
    features.append(np.mean(blue))
    features.append(np.std(red))
    features.append(np.std(green))
    features.append(np.std(blue))
    return features

def get_features(frames, topleft, bottomright):
    ''' Input: frames - all frames for one tile
               topleft - y, x coordinates of topleft point of the tile
               bottomright - y, x coordinates of bottomright point of the tile
        Output: a matrix containing feature information, each row represents
                a frame, and the whole matrix represents a tile
    '''
    tile_list = []
    for i in range(len(frames)):
        frame_features = compute_features(frames[i], topleft, bottomright)
        tile_list.append(frame_features)
    tile_list = np.array(tile_list)
    return tile_list

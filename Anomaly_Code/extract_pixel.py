import cv2
import numpy as np

def extract_pixel(frame, topleft, bottomright):
    '''Input: tile coordinates[y,x]
       Output: a matrix with pixel data
    '''
    tile = frame[topleft[0]:bottomright[0], topleft[1]:bottomright[1],:]
    return tile

def tile_list(size, row, videolength = 384):
    '''Input: size: width of the tile
              row: starting x axis number for the top of the box
       Output:
    '''
    tiles = []
    grid = videolength // size
    for i in range(0, grid):
        tiles.append([size * i, row, size * (i+1), row + size - 5])
    return tiles

import cv2
import numpy as np


def findCorners(img):
    # Only use for size chess board is 8x8
    pattern_size = (7, 7) 
    flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
    
    # Convert image BRG to GRAY
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find chess corners 
    ret, corners = cv2.findChessboardCorners(imgGray,
                                                pattern_size,
                                                None,
                                                flags)
    
    # Convert float in corners to int corners
    corners, shape = corners.astype(int), corners.shape
    
    corners = corners.reshape(shape[0], -1)
    return corners
        

def convert_corners_to_coordinates(corners):
    """
        The purpose of this function converts coordinates into corresponding values
            + First bring the coordinates to the rectangles
            + From the rectangle see if it belongs to A1 or A2 or B7 ??
    """        
    if isinstance(corners, list):
        corners = np.array(corners)
            
    # Convert to bounding box
    x_coordinates = list(set(corners[:, 0]))
    y_coordinates = list(set(corners[:, 1]))
    x_coordinates.sort()
    y_coordinates.sort()
    
    len_row_col = len(x_coordinates)
    bounding_box = []
    j = 0
    while j < len_row_col - 1:
        for i in range(len_row_col - 1):
            x_min, y_min = x_coordinates[i], y_coordinates[j]
            x_max, y_max = x_coordinates[i + 1], y_coordinates[j + 1]
            bounding_box.append([x_min, y_min, x_max, y_max])
        j += 1
    return bounding_box
        
    
if __name__ == '__main__':
    img = cv2.imread('D:/Machine_Learning/Chess_Robot/test_img/images.png')
    corners = findCorners(img)
    convert_corners_to_coordinates(corners)
    
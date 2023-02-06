import cv2
import numpy as np

__KEY_COLS__ = {
    '1': 'A',
    '2': 'B',
    '3': 'C',
    '4': 'D',
    '5': 'E',
    '6': 'F',
    '7': 'G',
    '8': 'H',
    '9': 'I',
    '10': 'J',
    '11': 'K',
    '12': 'L',
    '13': 'M',
    '14': 'N',
    '15': 'O',
    '16': 'P',
    '17': 'Q',
    '18': 'R',
    '19': 'S',
    '20': 'T',
    '21': 'U',
    '22': 'V',
    '23': 'W',
    '24': 'X',
    '25': 'Y',
    '26': 'Z'
}


__KEY_ROWS__ = {
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': '10',
    '11': '11',
    '12': '12',
    '13': '13',
    '14': '14',
    '15': '15',
    '16': '16',
    '17': '17',
    '18': '18',
    '19': '19',
    '20': '20',
    '21': '21',
    '22': '22',
    '23': '23',
    '24': '24',
    '25': '25',
    '26': '26'
}


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
    
    # get the coordinates of the margin of the chessboard
    x_corners, y_corners = list(set(corners[:, 0])), list(set(corners[:, 1]))
    x_corners.sort()
    y_corners.sort()
    delta_x = x_corners[1] - x_corners[0]
    delta_y = y_corners[1] - y_corners[0]
    x_corners.insert(0, delta_x)
    y_corners.insert(0, delta_y)
    x_corners.append(x_corners[-1] + delta_x)
    y_corners.append(y_corners[-1] + delta_y)

    # Combine coordinates in 8x8
    rows, cols = len(x_corners), len(y_corners)
    new_corners = np.zeros((rows*cols, 2))
    for i in range(rows):
        for j in range(cols):
            new_corners[9*i + j, 0], new_corners[9*i + j, 1] = x_corners[i], y_corners[j]
    return new_corners.astype(int)
        

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
    bounding_box = {}
    j = 0
    while j < len_row_col - 1:
        for i in range(len_row_col - 1):
            x_min, y_min = x_coordinates[i], y_coordinates[j]
            x_max, y_max = x_coordinates[i + 1], y_coordinates[j + 1]
            bounding_box[__KEY_ROWS__[str(i + 1)] + __KEY_COLS__[str(j + 1)]] = [x_min, y_min, x_max, y_max]
        j += 1    
    
    print(bounding_box)
    return bounding_box
        
    
if __name__ == '__main__':
    img = cv2.imread('D:/Machine_Learning/Chess_Board/test_img/images.png')
    corners = findCorners(img)
    convert_corners_to_coordinates(corners)
    
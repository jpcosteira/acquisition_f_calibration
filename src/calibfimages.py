# imports 
import numpy as np 
import cv2 as cv 
import glob 
import os
import json
  
#FROM:  https://www.geeksforgeeks.org/calibratecamera-opencv-in-python/
# termination criteria 
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001) 

chessboard_size = (9,6)

# Real world coordinates of circular grid 
#obj3d = np.zeros((44, 3), np.float32) 
# As the actual circle size is not required, 
# the z-coordinate is zero and the x and y coordinates are random numbers. 
#a = [0, 36, 72, 108, 144, 180, 216, 252, 288, 324, 360] 
#b = [0, 72, 144, 216, 36, 108, 180, 252] 
#for i in range(0, 44): 
#    obj3d[i] = (a[i // 4], (b[i % 8]), 0) 
    # print(objp[i]) 
# Prepare object points
obj3d = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
obj3d[:,:2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# Vector to store 3D points 
obj_points = [] 
# Vector to store 2D points 
img_points = [] 
  
# Extracting path of individual image stored in a given directory 
images = glob.glob('./Images/*.png') 
for f in images: 
    # Loading image 
    img = cv.imread(f) 
    # Conversion to grayscale image 
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
  
    # To find the position of circles in the grid pattern 
   # ret, corners = cv.findCirclesGrid( 
   #     gray, (4, 11), None, flags=cv.CALIB_CB_ASYMMETRIC_GRID) 
    ret, corners = cv.findChessboardCorners(gray, chessboard_size, None)
    # If true is returned,  
    # then 3D and 2D vector points are updated and corner is drawn on image 
    if ret == True: 
        obj_points.append(obj3d) 
  
        corners2 = cv.cornerSubPix(gray, corners, chessboard_size, (-1, -1), criteria) 
        # In case of circular grids,  
        # the cornerSubPix() is not always needed, so alternative method is: 
        # corners2 = corners 
        img_points.append(corners2) 
  
        # Drawing the corners, saving and displaying the image 
        cv.drawChessboardCorners(img, chessboard_size, corners2, ret) 
        cv.imwrite('output.jpg', img) #To save corner-drawn image 
        cv.imshow('img', img) 
        cv.waitKey(1) 
cv.destroyAllWindows() 
  
"""Camera calibration:  
Passing the value of known 3D points (obj points) and the corresponding pixel coordinates  
of the detected corners (img points)"""
print("Calibrating camera")
ret, camera_mat, distortion, rotation_vecs, translation_vecs = cv.calibrateCamera( 
    obj_points, img_points, gray.shape[::-1], None, None) 
calib_params = {
            'camera_matrix': camera_mat.tolist(),
            'dist_coeffs': distortion.tolist(),
            'resolutionx': img.shape[0],
            'resolutiony': img.shape[1],
            'error': ret
        }
#SAVE CALIBRATION
os.makedirs("CamParams", exist_ok=True)
with open("CamParams/camera_params.json", 'w') as f:
        json.dump(calib_params, f)
        print(f"Saved camera parameters to CamParams/calib_params",calib_params)
print("Error in projection : \n", ret) 
print("\nCamera matrix : \n", camera_mat) 
print("\nDistortion coefficients : \n", distortion) 
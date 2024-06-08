import cv2
import numpy as np
import os
import json

#CAMERA CALIBRATION - Script para calibração de intrinsecos das câmaras

# Parameters
CAM_INDEX=1 #camara usb - 0 default
chessboard_size = (9, 6)  # Dimensions of the chessboard pattern
chessboard_sq_size = (16.8, 16.8)  # Dimensions of the chessboard pattern
min_displacement = 100  # Minimum displacement in pixels between acquisitions
quiet_displacement = 15 # Max displacement to be accepted as quiet

# Create a directory to save images if it does not exist
output_dir = "calibration_images"
os.makedirs(output_dir, exist_ok=True)

# Initialize the webcam
cap = cv2.VideoCapture(CAM_INDEX,cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Set max resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,10000)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,10000)

# Initialize variables

last_corners = None
image_counter = 0
corner_coordinates_list = []

def save_image(frame, counter):
    filename = f"{output_dir}/chessboard_{counter:04d}.png"
    cv2.imwrite(filename, frame)
    print(f"Saved {filename}")

def calibrate_camera(corner_coords_file, chessboard_sq_size, output_params_file):
    # Read corner coordinates from file
    with open(corner_coords_file, 'r') as f:
        corner_coords_list = json.load(f)
    
    # Prepare object points
    objp = np.zeros((chessboard_sq_size[0]*chessboard_sq_size[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboard_sq_size[0], 0:chessboard_sq_size[1]].T.reshape(-1, 2)

    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane.

    for corners in corner_coords_list:
        objpoints.append(objp)
        imgpoints.append(np.array(corners, dtype=np.float32))

    # Calibrate camera
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    if ret:
        # Save camera parameters to a file
        calib_params = {
            'camera_matrix': camera_matrix.tolist(),
            'dist_coeffs': dist_coeffs.tolist()
        }
        with open(output_params_file, 'w') as f:
            json.dump(calib_params, f)
        print(f"Saved camera parameters to {output_params_file}")
    else:
        print("Camera calibration failed")
mostra=1,

def acquire_gray(cap):
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        return False,False,False

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return True,gray,frame

# MAIN LOOP -
# acquire image, detect corner if image changed, wait to be quiet, acquire final

while True:

    # Capture a frame from the webcam
    retg,gray,frame=acquire_gray(cap)

    # Find the chessboard corners
    if retg :
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    else:
        print('Erro acquisition')
        ret = False

    if ret:
        # If first image, save it immediately
        if last_corners is None:
            image_counter += 1
            last_corners = corners
        else:
            # Calculate displacement
            displacement = np.max(np.abs(corners - last_corners))
            if displacement > min_displacement:  # only if board moved
                displacement2 =100;#some value big - 100 pxls!
                # Keep the board quiet
                while displacement2 > quiet_displacement:#only if board is still
                    retg,gray,frame=acquire_gray(cap)
                    ret, corners2 = cv2.findChessboardCorners(gray, chessboard_size, None)
                    if ret:
                        displacement2 = np.max(np.abs(corners - corners2))
                        corners =corners2
                        print(f"Be quiet")
                save_image(frame, image_counter)
                image_counter += 1
                last_corners = corners
                corner_coordinates_list.append(corners.tolist())
                # Draw and display the corners
                cv2.drawChessboardCorners(frame, chessboard_size, corners, ret)

    # Display the frame
    frame=cv2.resize(frame,(640,480))
    cv2.imshow('Webcam', frame)

    # Check for 'W' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('w'):
        break

# Save corner coordinates to a file
corner_coords_file = f"{output_dir}/corner_coordinates.json"
with open(corner_coords_file, 'w') as f:
    json.dump(corner_coordinates_list, f)

print(f"Saved corner coordinates to {corner_coords_file}")

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()

# Calibrate the camera and save the parameters
output_params_file = f"{output_dir}/camera_params.json"
calibrate_camera(corner_coords_file, chessboard_size, output_params_file)

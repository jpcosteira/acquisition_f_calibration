import cv2
import os
import json
import time

#SCRIPT TO ACQUIRE IMAGES FROM CALIBRATION OBJECT

CAM_INDEX=1
#camera resolution
resolution_width=800 #max resolution put 100000
resolution_height=600
# Set up webcam capture
cap = cv2.VideoCapture(CAM_INDEX,cv2.CAP_DSHOW)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Set max resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution_height)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,resolution_width)

# Create ArUco dictionary and parameters
#aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
parameters = cv2.aruco.DetectorParameters_create()

# Directory to save the images and data
save_dir = 'aruco_images'
os.makedirs(save_dir, exist_ok=True)

img_num=0
# Capture and process 100 images
#Adquire N imagens com arucos e guarda-as de acordo com o protocolo do Gabriel bem como um json com os arucos detectados

while img_num <100 :
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Could not read frame {img_num}.")
        continue
    
    # Detect ArUco markers
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    
    
    # Wait for a short period to display the window, press 'q' to quit early
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    if ids is not None:
        img_num+=1
    # Create a folder for the current image
        img_folder = os.path.join(save_dir, f'{img_num:03}')
        os.makedirs(img_folder, exist_ok=True)
    
    # Save the image
        img_path = os.path.join(img_folder, f'{img_num:03}.png')
        cv2.imwrite(img_path, frame)
    
        # Prepare the data to be saved
        aruco_data = {
            'corners': [corner.tolist() for corner in corners],
            'ids': ids.tolist() if ids is not None else []
        }

        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        
        # Save the ArUco marker data to a file
        data_path = os.path.join(img_folder, f'aruco_data_{img_num:03}.json')
        with open(data_path, 'w') as f:
            json.dump(aruco_data, f)
            print(f"Processed and saved image {img_num}.")

    # Display the image with detected markers

    cv2.imshow('ArUco Markers', frame)
    # Check for 'W' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('w'):
        break
    time.sleep(1)
    
    

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Resources / websites that have been used to get inspiration and help to solve this project.

# https://github.com/CreepyD246/Simple-Color-Detection-with-Python-OpenCV/blob/main/color_detection.py
# http://www.linoroid.com/2016/12/detect-a-green-color-object-with-opencv/
# https://pysource.com/2019/06/05/control-webcam-with-servo-motor-and-raspberry-pi-opencv-with-python/

import cv2
import numpy as np
import ArduinoToPython as atpt


def make_720p():
    # Converts the resolution of webcam_video to 720p
    webcam_video.set(3, 1280)
    webcam_video.set(4, 720)


# Choose which color you want to detect, here is it green!
#(hue, saturation, value)
lower = np.array([65, 60, 60])
upper = np.array([80, 255, 255])

# Connecting to webcam
webcam_video = cv2.VideoCapture(2)
make_720p()

# Reads from webcamera
success, video = webcam_video.read()
cols, rows, _ = video.shape  # rows = 1280 and cols = 720

# Columns are a group of cells aligned vertically
# Rows are a group of cells arranged horizontally

# Initiate some variables
y_medium = int(cols / 2)
x_medium = int(rows / 2)

center_x = int(rows / 2)
center_y = int(cols / 2)

position_x = 90  # degrees
position_y = 90  # degrees

# Makes an array with size 5,5 as type int and saves it in kernel.
kernel = np.ones((5, 5), 'int')

while True:
    # Reads the video stream
    success, video = webcam_video.read()
    # Blur the video to remove some noise
    bluredVideo = cv2.GaussianBlur(video, (5, 5), 2)

    # Convert the video from BGR colorspace to HSV colorspace
    img = cv2.cvtColor(bluredVideo, cv2.COLOR_BGR2HSV)
    # Checks if array elements lie between the elements of lower and upper array and store the result in mask
    mask = cv2.inRange(img, lower, upper)

    # Morphological transformation for removing noise
    dilated = cv2.dilate(mask, kernel)
    erosion = cv2.erode(dilated, kernel)

    # Finds the contour of the object / correct color and saves it in a list named mask_contours
    mask_contours, hierarchy = cv2.findContours(
        erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Finding contours in mask image

    # Sorting the mask_contours list
    contours = sorted(
        mask_contours, key=lambda x: cv2.contourArea(x), reverse=True)

    # Draws the largest contour in the image
    cv2.drawContours(video, contours, 0, (255, 0, 0), 2)

    # Finds the position of the largest contour and finds the center inside the contour
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        y_medium = int((y + y + h) / 2)
        x_medium = int((x + x + w) / 2)
        break

    # Line Vertically goes horizontally (right and left)
    cv2.line(video, (x_medium, 0), (x_medium, 720), (0, 255, 0), 2)
    cv2.line(video, (center_x, 320), (center_x, 400), (0, 0, 255), 2)
    # Line horizontally goes verticaly (up and down)
    cv2.line(video, (0, y_medium), (1280, y_medium), (0, 255, 0), 2)
    cv2.line(video, (600, center_y), (680, center_y), (0, 0, 255), 2)

    # Displays regular video and mask
    cv2.imshow("Video", video)
    cv2.imshow('erosion', erosion)

    # Ends the while loop if "ESC" is pressed.
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    # Moves both servomotors relative to the position of the largest contour
    # x_medium = 0 -> 1280
    # y_medium = 0 -> 780
    # center_x = 640
    # center_y = 390

    if (x_medium < center_x - 30):

        if(position_x >= 180):
            position_x = 180
        else:
            position_x += 1

    elif (x_medium > center_x + 30):

        if(position_x <= 0):
            position_x = 0
        else:
            position_x -= 1

    if (y_medium < center_y - 30):

        if (position_y >= 180):
            position_y = 180
        else:
            position_y += 1

    elif (y_medium > center_y + 30):

        if (position_y <= 0):
            position_y = 0
        else:
            position_y -= 1

    # Transmits the position to both servo motors. (bottom, top)
    atpt.getPosition(position_x, position_y)

webcam_video.release()
cv2.destroyAllWindows()

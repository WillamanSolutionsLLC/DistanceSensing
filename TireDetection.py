import cv2
import numpy as np
from datetime import datetime

start_time = datetime.utcnow()
image = cv2.imread('TruckTires.jpg')
output = image.copy()
height, width = image.shape[:2]
maxRadius = int(1.1*(width/12)/2)
minRadius = int(0.9*(width/12)/2)


def get_grayscale_image(in_image):
    return cv2.cvtColor(in_image, cv2.COLOR_BGR2GRAY)


def get_circles(in_image):
    grayscale_img = get_grayscale_image(in_image)
    return cv2.HoughCircles(image=grayscale_img, method=cv2.HOUGH_GRADIENT, dp=1.2, minDist=2*minRadius, param1=50,
                            param2=80, minRadius=minRadius, maxRadius=maxRadius)


def main():
    circles = get_circles(image)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circlesRound = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circlesRound:
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            print('X: %s, Y: %s, R: %s' % (x, y, r))

        cv2.imshow('Tires Detected: %s' % len(circlesRound.round()), output)
        end_time = datetime.utcnow()
        print('Process Time: %s' % (end_time-start_time))
        cv2.waitKey(0)
    else:
        print('No circles found')


main()

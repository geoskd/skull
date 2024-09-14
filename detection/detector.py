#!/usr/bin/python3

import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('/home/schu/opencv/data/haarcascades/haarcascade_fullbody.xml')

def detect_faces(image):
    coordinates = face_cascade.detectMultiScale(image)
    for( x,y,w,h) in coordinates:
        cv2.rectangle(image,(x,y), (x+w, y+h), (255,255,255), 5)
        print( coordinates)
    return image


cv2.startWindowThread()
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while(True):
    # reading the frame
    ret, frame = cap.read()
    frame = detect_faces(frame)
    # displaying the frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # breaking the loop if the user types q
        # note that the video window must be highlighted!
        break

cap.release()
cv2.destroyAllWindows()
# the following is necessary on the mac,
# maybe not on other platforms:
cv2.waitKey(1)

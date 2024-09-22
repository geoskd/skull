#!/usr/bin/python

import sys
import time
import cv2

from picamera2 import Picamera2 as picam
from pwm import servo
from eyes import eyes

pose = servo()


#time.sleep(1)
#pose.set_Position(4.5,2.0)
#time.sleep(1)
#pose.set_Position(4.5,8.0)
#time.sleep(1)

#pose.set_Position(4.5,5.0)
#time.sleep(1)
#pose.set_Position(9.5,5.0)
#time.sleep(1)

#pose.set_Position(7.0,5.0)
#time.sleep(1)
look = eyes()
look.test()

look.render()
time.sleep(1)
look.draw_pixel( 0, 3,5,1)
look.draw_pixel( 1, 1,1,1)
look.render()

pose.end()
sys.exit()

face_cascade = cv2.CascadeClassifier('/home/schu/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

pic = picam()
imgname = "test.jpg"
cam_conf = pic.create_preview_configuration(main={"format":'XRGB8888', "size":(640,480)})
pic.configure(cam_conf)
pic.start() 

def detect_faces(image):
    coordinates = face_cascade.detectMultiScale(image)
    for( x,y,w,h) in coordinates:
        cv2.rectangle(image,(x,y), (x+w, y+h), (255,255,255), 5)
        print( coordinates)
    return image

while True:
    image = pic.capture_array()
    image = detect_faces( image )
    cv2.imshow('Preview', image )
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




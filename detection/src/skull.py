#!/usr/bin/python

import sys
import time
import cv2
import threading

from picamera2 import Picamera2 as picam
from pwm import servo
from eyes import eyes


look = eyes()

look.render()
time.sleep(1)
look.draw_pixel( 0, 3,5,1)
look.draw_pixel( 1, 1,1,1)
look.render()

face_cascade = cv2.CascadeClassifier('/home/schu/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

pic = picam()
imgname = "test.jpg"
cam_conf = pic.create_preview_configuration(main={"format":'XRGB8888', "size":(640,480)})
pic.configure(cam_conf)
pic.start() 

current_x = 0
current_y = 0

def detect_faces(image):
    global current_x
    global current_y
    coordinates = face_cascade.detectMultiScale(image)
    w_max = 0
    h_max = 0
    x_cent = -1
    y_cent = -1
    for( x,y,w,h) in coordinates:
        if (h + w) > (h_max + w_max):
            h_max = h
            w_max = w
            x_cent = x
            y_cent = y
    if x_cent >= 0:
        x = int(x_cent + ( w_max / 2 ))
        y = int(y_cent + ( h_max / 2 ))
        current_x = 320 - x
        current_y = y - 240
        x = (current_x * 4) / 640
        y = (current_y * 5) / 480
        x = int(x + 3.5)
        y = int(y + 4.5)

        look.reset_buffer()
        look.draw_pixel(0, x, y, 1 )
        look.draw_pixel(1, x, y, 1 )
        look.render()
    else:
        current_x = 0
        current_y = 0


def movement_thread():
    global current_x
    global current_y
    pose = servo()
    pose.set_Position(7.0,5.0)
    time.sleep(1)

    while True:
        time.sleep(0.05)
        move_x = 0
        move_y = 0
        if current_x > 0:
            move_x = 0.02
        if current_x < -60:
            move_x = -0.02
        if current_y > 55:
            move_y = -0.02
        if current_y < -5:
            move_y = +0.02
        pose.move_position_by(move_x, move_y)
    pose.end()

movement_thread = threading.Thread(target=movement_thread, args=())

movement_thread.start()

while True:
    image = pic.capture_array()
    image = cv2.rotate(image, cv2.ROTATE_180)
    image = detect_faces( image )

movement_thread.join()



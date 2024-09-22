#!/usr/bin/python

import time
from rpi_hardware_pwm import HardwarePWM as PWM

class servo:

    def __init__(self, frequency=50, x_limits=[4.5,9.5], y_limits=[2.5,7.5]):
        self.x_min = x_limits[0]
        self.x_max = x_limits[1]
        self.x = (self.x_min + self.x_max ) / 2
        self.y_min = y_limits[0]
        self.y_max = y_limits[1]
        self.y = (self.y_min + self.y_max ) / 2
        self.pwm_x = PWM(pwm_channel=1, hz=frequency)
        self.pwm_y = PWM(pwm_channel=0, hz=frequency)
        self.pwm_x.start(self.x)
        self.pwm_y.start(self.y)

    def set_Position(self,x,y):
        if y < self.y_min:
            y = self.y_min
        if y > self.y_max:
            y = self.y_max
        self.y = y
        if x < self.x_min:
            x = self.x_min
        if x > self.x_max:
            x = self.x_max
        self.x = x
        self.pwm_x.change_duty_cycle(x)
        self.pwm_y.change_duty_cycle(y)
    
    def move_position_by(self,x,y):
        self.set_Position(self.x + x, self.y + y)        
    
    def end(self):
        self.pwm_x.stop()
        self.pwm_y.stop()



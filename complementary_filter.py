#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import math
import numpy as np
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32

cmd_vel = "/cmd_vel"
Imu_topic = "/imu"

class SelfBalance:
    def __init__(self):
        self.new_roll = 0.0
        self.new_pitch = 0.0
        self.k = 0.6
        self.dt = 0
        self.flg = 0
        self.roll_error = 0
        self.pitch_error = 0
        self.now = time.time()
        self.pub = rospy.Publisher(cmd_vel,Twist,queue_size =1)
        self.subscriber = rospy.Subscriber(Imu_topic,Imu,self.callback)

    def callback(self,data):
        #setPoint = 0
        x = data.angular_velocity.x
        y = data.angular_velocity.y
        z = data.angular_velocity.z
        a = data.linear_acceleration.x
        b = data.linear_acceleration.y
        c = data.linear_acceleration.z
        #print x, y, z, a, b, c

        roll = math.atan2(y , math.sqrt(x**2 + z**2))
        pitch = math.atan2(x , math.sqrt(y**2 + z**2))        

        a *= math.pi/180
        b *= math.pi/180
        c *= math.pi/180

        self.new_roll = self.k*(self.new_roll + a*self.dt) + (1 - self.k)*roll
        self.new_pitch = self.k*(self.new_pitch + b*self.dt) + (1 - self.k)*pitch

        roll = math.degrees(self.new_roll)
        pitch = math.degrees(self.new_pitch)

        if(self.flg < 20):
            self.roll_error = -roll
            self.pitch_error = -pitch
            #yaw_error = -yaw
        self.flg += 1

        roll += self.roll_error
        pitch += self.pitch_error                

        print("roll:{}".format(round(roll,2)))
        print("pitch:{}".format(round(pitch,2)))
        #print("yaw:{}".format(round(yaw,2)))
        print("\n")
        rospy.sleep(0.1)

def main(args):
    '''Initializes and cleanup ros node'''
    rospy.init_node('SelfBalance', anonymous=True)
    ic = SelfBalance()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS "

if __name__ == "__main__":
    main(sys.argv)  

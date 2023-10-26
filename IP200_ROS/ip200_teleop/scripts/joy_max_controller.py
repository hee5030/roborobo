#!/usr/bin/env python3
import rospy
from std_msgs.msg import UInt16, Float32
from nav_msgs.msg import Odometry
import time
import math

class JoyMaxControl():
    def __init__(self):
        self.joy_sub = rospy.Subscriber('/onoff', UInt16, self.sub_callback)
        self.pub_max = rospy.Publisher('/onoff', UInt16, queue_size=5)
        # self.pub_timer = rospy.Publisher('/timer', Float32, queue_size=5)
        self.sub_timer = rospy.Subscriber('/odom', Odometry, self.sub_time_callback) 
        self.duration = 10
        self.pre_time = 0
        self.time = 0
        self.isZero = False
        self.timer_on = False
        self.count = 0

    def sub_callback(self, onoff_msg):
        # up
        if onoff_msg.data == 0:
            self.isZero = True
            if self.timer_on == False:
                rospy.loginfo("Timer Start!")
                self.pre_time = self.time
                self.timer_on = True

        elif onoff_msg.data == 1:
            if self.timer_on == True:
                self.timer_on = False
                rospy.loginfo("Timer Stop!")
            self.isZero = False

        elif onoff_msg.data == 2:
            if self.timer_on == True:
                self.timer_on = False
                rospy.loginfo("Timer Stop!")
            self.isZero = False
        
        # if ((self.time - self.pre_time) > self.duration) & self.timer_on == True :
        #     self.pub_stop()
        #     self.isZero = False
        #     self.timer_on = False
        # rospy.loginfo(self.time - self.pre_time)

    def pub_stop(self):
        up_down = UInt16()
        up_down.data = 2
        self.pub_max.publish(up_down)
    
    # def pub_time(self):
    #     time_ = Float32()
    #     time_.data = math.ceil(time.time())
    #     self.pub_timer.publish(time)
    #     rospy.Rate(10)
        
    def sub_time_callback(self, odom_msg):
        self.time = odom_msg.header.stamp.secs
        if ((self.time - self.pre_time) > self.duration) & self.timer_on == True :
            self.pub_stop()
            self.isZero = False
            self.timer_on = False
        
        if self.count % 20 == 0:
            rospy.loginfo(self.time - self.pre_time)
        self.count += 1

if __name__ == '__main__':
    rospy.init_node('joy_max_controller', anonymous=True)
    joy_max_controller = JoyMaxControl()
    rospy.spin()
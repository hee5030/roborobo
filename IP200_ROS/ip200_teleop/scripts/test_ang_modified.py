#!/usr/bin/env python3
# Lift model

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math
class RotateRobot:
    def __init__(self):
        rospy.init_node('rotate_robot')
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.current_angle = 0
        self.target_angle = 0
        self.rate = rospy.Rate(50)
        self.roll = 0.0
        self.pitch = 0.0
        self.cnt = 0

    def odom_callback(self, data):
        orientation_q = data.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        self.roll, self.pitch, self.yaw = euler_from_quaternion(orientation_list)
        self.current_angle = self.yaw

    def rotate(self, target_angle):
        self.target_angle = target_angle
        vel_msg = Twist()
        rospy.loginfo(self.current_angle)

        while abs(self.target_angle - self.current_angle) > 0.04125 and not rospy.is_shutdown():
            if self.current_angle < 0:
                self.current_angle += 2 * math.pi
            # vel_msg.angular.z = math.pi/10
            vel_msg.angular.z = 0.2
            self.velocity_publisher.publish(vel_msg)
            # rospy.loginfo("rotate")
            # rospy.loginfo(self.target_angle)
            rospy.loginfo(self.current_angle)
            self.rate.sleep()

        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        rospy.loginfo("send_vel")
        self.cnt += 1
        rospy.loginfo(self.cnt)
        rospy.sleep(1)
    
if __name__ == '__main__':
    try:
        robot = RotateRobot()
        while not rospy.is_shutdown():
            robot.rotate(robot.current_angle + 1.57) # rotate 90 degrees
    except rospy.ROSInterruptException:
        pass
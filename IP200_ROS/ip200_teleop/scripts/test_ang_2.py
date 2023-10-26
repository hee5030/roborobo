#!/usr/bin/env python3
# Non-lift model

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from std_srvs.srv import Trigger, TriggerRequest
import math
class RotateRobot:
    def __init__(self):
        rospy.init_node('rotate_robot')
        self.reset_odom()
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.current_angle = 0
        self.target_angle = 0
        self.rate = rospy.Rate(50)
        self.roll = 0.0
        self.pitch = 0.0
        self.cnt = 0

    def reset_odom(self):
        try:
            rospy.wait_for_service('reset_odometry')
            reset = rospy.ServiceProxy('reset_odometry', Trigger)
            req = TriggerRequest()
            result = reset(req)
            rospy.loginfo("odom_reset")
        except rospy.service.ServiceException:
            rospy.loginfo("odom_reset")
            pass

    def odom_callback(self, data):
        orientation_q = data.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        self.roll, self.pitch, self.yaw = euler_from_quaternion(orientation_list)
        self.current_angle = self.yaw

    def rotate(self, target_angle):
        self.target_angle = target_angle
        vel_msg = Twist()
        rospy.loginfo(self.current_angle)

        # vel_ang_z = 0.2 -> 0.025
        if self.current_angle == 0.0:
            while abs(self.target_angle - self.current_angle) > 0.06 and not rospy.is_shutdown():
                if self.current_angle < 0:
                    self.current_angle += 2 * math.pi
                # vel_msg.angular.z = math.pi/10
                vel_msg.angular.z = 0.3
                self.velocity_publisher.publish(vel_msg)
                # rospy.loginfo("rotate")
                # rospy.loginfo(self.target_angle)
                rospy.loginfo(self.current_angle)
                self.rate.sleep()

            self.cnt += 1
            rospy.loginfo(self.cnt)

        vel_msg.angular.z = 0.0
        self.velocity_publisher.publish(vel_msg)
        rospy.loginfo("send_vel")

        self.reset_odom()
        self.target_angle = 1.57
        rospy.sleep(1)
    
if __name__ == '__main__':
    try:
        robot = RotateRobot()
        while not rospy.is_shutdown():
            robot.rotate(robot.current_angle + 1.57) # rotate 90 degrees
    except rospy.ROSInterruptException:
        pass
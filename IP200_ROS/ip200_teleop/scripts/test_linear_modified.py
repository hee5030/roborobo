#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist, Vector3, Point
from nav_msgs.msg import Odometry

class RobotControl():
    def __init__(self):
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.current_position_x = None
        self.move_forward = True
        self.distance = rospy.get_param('~distance', 1.0)
        # self.target_position_x = None
        self.rate = rospy.Rate(20)
        self.count = 0

    def odom_callback(self, odom_msg):
        self.current_position_x = odom_msg.pose.pose.position.x
        # if self.target_position_x is None:
        #     self.target_position_x = 0.0 + self.distance
        
    def run(self):
        vel_msg = Twist()
        velocity = 0.15

        while not rospy.is_shutdown(): # or (self.count <= 10):
            if self.current_position_x is not None:
                if self.move_forward:
                    if self.current_position_x < self.distance - (velocity/4):
                        vel_msg.linear.x = velocity
                        # rospy.loginfo(f"Target_pose: {self.target_position_x}")
                        rospy.loginfo(f"Move forward: {self.current_position_x}")
                    else:
                        self.move_forward = False
                        # self.target_position_x = self.current_position_x - self.distance
                        vel_msg.linear.x = 0.0

                else:
                    if self.current_position_x < 0.0 + (velocity/4):
                        vel_msg.linear.x = -velocity
                        rospy.loginfo(f"Move backward: {self.current_position_x}")
                    else:
                        self.move_forward = True
                        # self.target_position_x = self.current_position_x + self.distance
                        vel_msg.linear.x = 0.0
                        self.count += 1
                        rospy.loginfo(f"Count: {self.count}")

            self.vel_pub.publish(vel_msg)
            self.rate.sleep()

    def stop(self):
        vel_msg = Twist()
        vel_msg.linear.x = 0.0
        self.vel_pub.publish(vel_msg)
        rospy.loginfo("Stop")
        self.rate.sleep()

if __name__ == '__main__':
    rospy.init_node('robot_control_node', anonymous=True)
    robot_control = RobotControl()
    robot_control.run()
    robot_control.stop()
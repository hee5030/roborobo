#!/usr/bin/env python3
# Lift Model

import rospy
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist, Vector3, Point
from nav_msgs.msg import Odometry
from std_srvs.srv import Trigger, TriggerRequest

class RobotControl():
    def __init__(self):
        rospy.init_node('robot_control_node', anonymous=True)
        self.reset_odom()
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(20)
        self.current_pos = Point()
        self.count = 0

    def reset_odom(self):
        try:
            rospy.wait_for_service('reset_odometry')
            reset = rospy.ServiceProxy('reset_odometry', Trigger)
            req = TriggerRequest()
            result = reset(req)
            rospy.loginfo("odom_reset")
        except rospy.service.ServiceException:
            rospy.loginfo("odom_reset")
            rospy.sleep(0.5)
            pass

    def odom_callback(self, odom_msg):
        self.current_pos = odom_msg.pose.pose.position
        
    def run(self):
        vel = 0.15
        # vel = 0.125
        while not rospy.is_shutdown():
            if self.current_pos.x == 0.0:
            # 전진 0.5m
                move_cmd = Twist()
                move_cmd.linear = Vector3(vel, 0.0, 0.0)
                move_cmd.angular = Vector3(0.0, 0.0, 0.0)
                while self.current_pos.x < 1.0 - (vel/4) and not rospy.is_shutdown():
                    self.pub.publish(move_cmd)
                    self.rate.sleep()
                    rospy.loginfo(f"Move forward: {self.current_pos.x}")
                move_cmd.linear = Vector3(0.0, 0.0, 0.0)
                self.pub.publish(move_cmd)
                rospy.sleep(1.0)

                # 후진 0.5m
                move_cmd = Twist()
                move_cmd.linear = Vector3(-vel, 0.0, 0.0)
                move_cmd.angular = Vector3(0.0, 0.0, 0.0)
                while self.current_pos.x > 0.0 + (vel/4) and not rospy.is_shutdown():
                    self.pub.publish(move_cmd)
                    self.rate.sleep()
                    rospy.loginfo(f"Move backward: {self.current_pos.x}")
                move_cmd.linear = Vector3(0.0, 0.0, 0.0)
                self.pub.publish(move_cmd)

                self.count += 1
                rospy.loginfo(f"Count: {self.count}")
                if self.count == 10:
                    break

            self.reset_odom()
            # self.current_pos.x = 0.0
            rospy.sleep(1.0)

    def stop(self):
        move_cmd = Twist()
        move_cmd.linear = Vector3(0.0, 0.0, 0.0)
        self.pub.publish(move_cmd)
        self.rate.sleep()
        rospy.loginfo('Stop')

if __name__ == '__main__':
    robot_control = RobotControl()
    robot_control.run()
    robot_control.stop()


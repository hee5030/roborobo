#! /usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point, Quaternion
from move_base_msgs.msg import RecoveryStatus
from std_srvs.srv import Empty
class RAINBOW():
    def __init__(self):
        rospy.init_node('scout_nav', anonymous=False)
        self.goal = MoveBaseGoal()
        self.i = 0
        self.flag = True
        self.flag_red = False
        self.status_msg = "empty"
        self.rcvy_status_msg = -1
        #self.rate = rospy.Rate(0.25)
        self.ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.mb_status_sub = rospy.Subscriber("/move_base/result",MoveBaseActionResult,self.mb_CB)
        self.rcvy_status_sub = rospy.Subscriber("/move_base/recovery_status", RecoveryStatus, self.rcvy_CB)
        rospy.Timer(rospy.Duration(1),callback = self.renew_goal)
        rospy.spin()
    def mb_CB(self,data):
        # try:
        #     self.status_msg = data.status.text
        # except:
        #     self.status_msg = "empty"
        self.status_msg = data.status.text
    def rcvy_CB(self,data):
        self.rcvy_status_msg = data.current_recovery_number
    def renew_goal(self,event):
        # lst = ["red", "orange", "yellow", "green", "blue", "navy", "purple", "white"]
        # lst = ["red", "orange", "yellow", "green", "blue"]
        lst = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "end"]
        #self.rate.sleep()
        if self.status_msg == "Goal reached.":
            self.flag = True
            # self.i = (self.i + 1) % 8
            # self.i = (self.i + 1) % 6
            self.i = (self.i + 1) % 10
            rospy.loginfo("---------------------------")
            rospy.loginfo("----- Reached at Goal -----")
            rospy.loginfo("---------------------------")
            self.status_msg = "empty_red"
        elif self.rcvy_status_msg == 1:
            self.flag = True
            rospy.loginfo("-----------------------------")
            rospy.loginfo(" Cancle Rotate & Resend Goal ")
            rospy.loginfo("-----------------------------")
            self.rcvy_status_msg = -1
        elif self.status_msg == "Failed to find a valid plan. Even after executing recovery behaviors.":
            self.flag = True
            rospy.loginfo("---------------------------")
            rospy.loginfo("------- Resend Goal -------")
            rospy.loginfo("---------------------------")
            self.status_msg = "empty"
        self.move_to(lst[self.i])
        #rospy.loginfo("Move to {}".format(i))
    def move_to(self, color):
        if color == "A":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(  1.8085702657699585,-6.4053425788879395,0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,0.045438531331644876,0.9989671365317395)
            # rospy.ServiceProxy("request_nomotion_update",Empty)()
        elif color == "B":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(11.113164901733398, -5.4133076667785645, 0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,0.7275429968961279, 0.6860620873269422)
            # rospy.ServiceProxy("request_nomotion_update",Empty)()
            if self.status_msg == "empty_red":
                self.flag_red = True     
        elif color == "C":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(10.01771354675293, 15.55501937866211, 0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,0.7479708937956597, 0.6637315285825451)
            if self.status_msg == "empty_red":
                self.flag_red = True
        elif color == "D":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(11.068178176879883, -5.210854530334473 ,0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,-0.6798240660497804, 0.7333752376645558)
        elif color == "E":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(21.136066436767578, -4.304326057434082 ,0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,0.040369080509592106, 0.9991848364235769)
        elif color == "F":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(19.323345184326172, 17.328039169311523 ,0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,0.739401904617625, 0.6732643043024252)
        elif color == "G":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(21.39333152770996, -4.453098773956299 ,0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0, -0.663731784190051, 0.7479706669755783)
        elif color == "H":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(2.659773588180542, -5.978487968444824 ,0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0, -0.9996249609498016, 0.027384985778848153)
        elif color == "I":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(-0.24619770050048828, 3.790066957473755 ,0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0, -0.999526115697004, 0.0307822032944266)
        elif color == "end":
            self.status_msg = "empty"
            self.flag == False
        if self.flag_red == True:
            time_past = rospy.Time.now().to_sec()
            time_now = rospy.Time.now().to_sec()
            while (time_now - time_past) < 3.0:
                # rospy.ServiceProxy("request_nomotion_update",Empty)()
                # rospy.loginfo("Request_nomotion_update...")
                time_now = rospy.Time.now().to_sec()
                rospy.sleep(0.3)
                rospy.ServiceProxy('move_base/clear_costmaps',Empty)()
                rospy.loginfo("Costmaps are cleared...")
            self.flag_red = False
            self.status_msg = "empty"
        if self.flag == True:
            rospy.ServiceProxy('move_base/clear_costmaps',Empty)()
            rospy.loginfo("Costmaps are cleared...")
            self.ac.send_goal(self.goal)
            rospy.loginfo("Send new goal...")
            self.flag = False              
        rospy.loginfo("Move to {}".format(color))
        
if __name__ =="__main__":
    RAINBOW()
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
        # Wait for the action server to start
        self.ac.wait_for_server()

        self.mb_status_sub = rospy.Subscriber("/move_base/result",MoveBaseActionResult,self.mb_CB)
        self.rcvy_status_sub = rospy.Subscriber("/move_base/recovery_status", RecoveryStatus, self.rcvy_CB)
        rospy.Timer(rospy.Duration(1), callback = self.renew_goal)
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
        # lst = ["A", "B", "C", "D", "E", "F", "end"]
        lst = ["A", "B", "C", "D", "end"]

        #self.rate.sleep()
        if self.status_msg == "Goal reached.":
            self.flag = True

            # self.i = (self.i + 1) % 8
            # self.i = (self.i + 1) % 6
            self.i = (self.i + 1) % 5

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
            self.goal.target_pose.pose.position = Point(-0.2712320638719675, 1.376306961141111, 0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,0.9330109847585047,0.3598478877525409)
            # rospy.ServiceProxy("request_nomotion_update",Empty)()

            
        elif color == "B":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(4.802488177775798, -0.5430740457450429, 0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,-0.8901016420862816, 0.4557620725283151)
            # rospy.ServiceProxy("request_nomotion_update",Empty)()


            if self.status_msg == "empty_red":
                self.flag_red = True      
            
        elif color == "C":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(4.735605219983144, -3.9528112886891726, 0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,0.7479708937956597, 0.6637315285825451)

            if self.status_msg == "empty_red":
                self.flag_red = True 


        elif color == "D":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(11.068178176879883, -5.210854530334473 ,0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,-0.9953826293777014, 0.0959865674619819)
        
        elif color == "E":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(-0.44639249654556, -3.2143829852262185, 0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,-0.9953826293777014, 0.0959865674619819)


        elif color == "F":
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
            self.goal.target_pose.pose.position = Point(1.996473789215088, -5.938211441040039 ,0)
            self.goal.target_pose.pose.orientation = Quaternion(0,0,-0.999526115697004, 0.0307822032944266)



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
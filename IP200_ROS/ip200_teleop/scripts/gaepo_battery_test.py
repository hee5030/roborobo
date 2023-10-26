#! /usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

# A, B, C, D 지점의 좌표와 회전을 저장합니다.
waypoints = [
    {'position': {'x': -1.8698510486323314, 'y': -0.8959684703619186}, 'orientation': {'z': 0.46092382784427227, 'w': 0.8874397021349584}},
    {'position': {'x': -0.7576991717764965, 'y': 2.086859691442056}, 'orientation': {'z': 0.1995542841740053, 'w': 0.9798867728813367}},
    {'position': {'x': 1.2629914252752457, 'y': 2.996913233709273}, 'orientation': {'z': 0.0690428990085385, 'w': 0.9976136918148711}},
    {'position': {'x': 3.4793171057516092, 'y': 2.3784314267635196}, 'orientation': {'z': -0.6297781490659945, 'w': 0.7767750529973334}},
    {'position': {'x': 1.381294589908936, 'y': -1.1841256362654848}, 'orientation': {'z': -0.9767546586014619, 'w': 0.21436029693098835}},
]

def move_base_goal(waypoint):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = waypoint['position']['x']
    goal.target_pose.pose.position.y = waypoint['position']['y']
    goal.target_pose.pose.orientation.z = waypoint['orientation']['z']
    goal.target_pose.pose.orientation.w = waypoint['orientation']['w']
    return goal

def move_robot_sequence():
    # rospy.init_node('move_robot_sequence')

    # move_base 서버와 통신하기 위한 action client 생성
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    def feedback_callback(feedback):
        # 이 부분에서 feedback를 처리하고 원하는 동작을 수행합니다.
        rospy.loginfo(f"Feedback: {feedback}")

    while not rospy.is_shutdown():
        for waypoint in waypoints:
            goal = move_base_goal(waypoint)
            client.send_goal(goal, feedback_cb=feedback_callback)
            client.wait_for_result()

            if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
                rospy.loginfo(f"목적지에 도착: {waypoint}")
            else:
                rospy.logerr(f"이동 실패: {waypoint}")
                break

if __name__ == '__main__':
    rospy.init_node('move_robot_sequence')
    try:
        move_robot_sequence()
    except rospy.ROSInterruptException:
        pass
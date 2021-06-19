#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import actionlib
import tf
import math
from geometry_msgs.msg import PoseStamped, Quaternion, TransformStamped, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

rospy.init_node('test')

navclient = actionlib.SimpleActionClient('/move_base', MoveBaseAction)

def quaternion_from_euler(roll, pitch, yaw):
    q = tf.transformations.quaternion_from_euler(roll / 180.0 * math.pi,
                                                 pitch / 180.0 * math.pi,
                                                 yaw / 180.0 * math.pi, 'rxyz')
    return Quaternion(q[0], q[1], q[2], q[3])

def move_base_goal(x, y, theta):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation = quaternion_from_euler(0, 0, theta)
    navclient.send_goal(goal)
    navclient.wait_for_result()
    state = navclient.get_state()
    return True if state == 3 else False

if __name__=='__main__':
    navclient.wait_for_server()

    try:
        # move in front of the long table
        move_base_goal(1, 0.5, 90)
    except:
        rospy.logerr('fail to move')
        sys.exit()

    try:
        # move in front of the tray
        move_base_goal(1.8, -0.1, -90)
    except:
        rospy.logerr('fail to move')
        sys.exit()

#!/usr/bin/env python
# coding=utf-8
import rospy
import os
import time
import math
import random
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf_conversions import transformations
from math import pi
from std_msgs.msg import String
import socket
import tf
from geometry_msgs.msg import Twist
from get_message import goal_pose
import actionlib
from multiprocessing import Process, Value
import threading


class Robot:
    def __init__(self):
        self.tf_listener = tf.TransformListener()
        try:
            self.tf_listener.waitForTransform('/map', '/base_link', rospy.Time(), rospy.Duration(1.0))
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            return

    def get_pos(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform('/map', '/base_link', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.loginfo("tf Error")
            return None
        euler = transformations.euler_from_quaternion(rot)
        # print euler[2] / pi * 180

        x = trans[0]
        y = trans[1]
        th = euler[2] / pi * 180
        return (x, y, th)


def server_start():
    # create a sender
    ip_port = tuple()
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    # create a node to connect the server
    # rospy.init_node('send_to',anonymous=True)
    # create a instance
    robot = Robot()
    # num_pos is used to save key-value like num:position
    num_pos = {}
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    # we will get server IP from system en
    network = os.getenv('ROKIN_IP')
    s.bind(('192.168.31.148', 1234))
    init_pos = [0.710, -1.373, -2.117]
    while not rospy.is_shutdown():
        # the data structs we predefined are all small ,must shorter than 1024B,and especially the MTU should shorter than 1500B.
        try:
            msg = s.recv(1024)
        except:
            continue
        # print msg
        data = eval(msg)
        if data['code'] == 0:
            # if code is 0 , run way-finding alg (explorer uav)
            # run w-f a
            # return init position
            # print robot.get_pos()
            start_way = Value("i", 1)
            thread = threading.Thread(target=way_finding, args=(start_way,))
            thread.start()
            sender.sendto(str({"code": 200, "pos": list(init_pos)}), ip_port)
        elif data['code'] == 1:
            # print "code is 1"
            x, y, z = robot.get_pos()
            num_pos[data['num']] = [x, y, z]
        # print [x,y,z]
        elif data['code'] == 2:
            # if code is 2 ,that means the server has distingguished the obj man,
            # when we receive this command ,we should stop way-finding's algorithm soon.
            # the server send the picture's num to us,we should find this num's position,and send it to server,
            # so that the server could dispatch other uav run to the obj's position, and kill him
            # and next return back to it,to wait the server's next command

            # when we get this command, we should stop the way-finding's algorithm
            start_way.value = 0
            # we find the obj's position
            obj_num = data['num']

            curr_pos = robot.get_pos()
            # we send it to server
            if obj_num in num_pos.keys():
                sender.sendto(str({"code": 2, "pos": num_pos[obj_num]}), ip_port)
                # print "send", obj_num, num_pos[obj_num]
                curr_pos = num_pos[obj_num]
                client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
                client.wait_for_server()
                goal = goal_pose(num_pos[obj_num - 2][0], num_pos[obj_num - 2][1], num_pos[obj_num - 2][2])
                client.send_goal(goal)
                client.wait_for_result()
            else:
                sender.sendto(str({"code": 2, "pos": list(curr_pos)}), ip_port)


        elif data['code'] == 3:
            # if this uav is the explorer's uav, you don't need act this command
            #    pass      

            # if this uav is coordinative uav , you should active this several codes,or not you should freeze them
            # get position from data
            obj_position = data['pos']
            # get to obj's pos
            # 创建MoveBaseAction client
            client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
            # 等待MoveBaseAction server 启动
            client.wait_for_server()
            goal = goal_pose(obj_position[0], obj_position[1] - 1.0, obj_position[2])
            client.send_goal(goal)
            client.wait_for_result()
            # if we get there , we should send msg to the server
            sender.sendto(str({"code": 4}), ip_port)
        elif data['code'] == 100:
            ip_port = data['ip_port']
            sender.sendto(str({"code": 200}), ip_port)
        else:
            time.sleep(3)
            # if we get this command, we should return back to init position,
            # if we get to the init's position ,we should send msg to server ,to tell it,we finished this task!

            # get init pos from data
            # print "init_pos", init_pos
            # return back to init's position
            client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
            client.wait_for_server()
            goal = goal_pose(init_pos[0], init_pos[1], init_pos[2])
            client.send_goal(goal)
            client.wait_for_result()

            # send success msg to server
            sender.sendto(str({"code": 5}), ip_port)
            break
    s.close()
    sender.close()


def way_finding(start_way):
    while start_way.value == 0:
        time.sleep(1)
    # 创建MoveBaseAction client
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    # 等待MoveBaseAction server 启动
    client.wait_for_server()
    positions = [[-5.112, -4.377, 0.524], [-2.061, -4.190, 1.038]]

    for i in positions:
        if start_way.value == 1:
            goal = goal_pose(i[0], i[1], i[2])
            client.send_goal(goal)
            client.wait_for_result()
            print
            "get to ", str(i)
        else:
            print
            "stop way_finding"
            break


if __name__ == "__main__":
    rospy.init_node('move_base', anonymous=True)
    start_way = Value("i", 0)
    # server = threading.Thread(target = server_start, args = (start_way,))
    server_start()

#!/usr/bin/env python
# coding=utf-8
import socket

import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty


def main():
    pass

#以字符串格式返回当前速度
def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

#主函数
if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin) #获取键值初始化，读取终端相关属性
    
    rospy.init_node('target_follow') #创建ROS节点
    pub = rospy.Publisher('~cmd_vel', Twist, queue_size=5) #创建速度话题发布者，'~cmd_vel'='节点名/cmd_vel'

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    server.bind(('192.168.31.148', 1234))

    control_speed = 0 #前进后退实际控制速度
    control_turn  = 0 #转向实际控制速度

    twist = Twist()  # 创建ROS速度话题变量
    twist.linear.x = 0
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0

    while not rospy.is_shutdown():
        try:
            msg = server.recv(1024)
            data = eval(msg)
            control_speed = data['speed']
            control_turn = data['turn']
            twist.linear.x = control_speed
            twist.angular.z = control_turn
            pub.publish(twist)  # ROS发布速度话题
        except Exception as e:
            print(e)
        # 程序结束前发布速度为0的速度话题
        finally:
            twist.linear.x = 0
            twist.angular.z = 0
            pub.publish(twist)

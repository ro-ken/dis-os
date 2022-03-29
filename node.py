import time

import server_node
from module.sched import sched_api
from module.node_helper.node_struct import *
from module.node_helper import node_settings as settings
from module.node_helper import node_handler
import os


class Node:
    # 节点资源映射关系
    # {"localhost:50051":resource}
    node_resources = {}

    def __init__(self, port):
        self.server_t = server_node.ServerThread(self,settings.server_ip, port)    # 节点的 server 线程
        self.node_list = settings.node_list     # 可连接的节点列表
        self.scheduler = sched_api.Scheduler(self, self.node_list, self.node_resources)     # 初始化调度器
        self.handler = node_handler.NodeHandler(self)   # 节点的辅助类，一些业务函数在里面
        self.client_list = []   # 可有多个发送者，每个client连接一个server
        self.task_queue = []  # 本节点待处理的任务队列

    # 运行grpc server, 调用do_work
    def start(self):
        self.server_t.start()
        time.sleep(1)
        self.handler.create_clients()
        self.handler.do_work()


if __name__ == '__main__':
    node = Node(50051)
    node.start()

    time.sleep(60 * 60 * 24)

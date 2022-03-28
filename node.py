
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

    server_t = None
    # 可有多个发送者，每个client连接一个server
    client_list = []

    # 本节点待处理的任务队列
    task_queue = []

    def __init__(self, server_t):
        server_t.node = self
        self.server_t = server_t
        self.node_list = settings.node_list
        self.scheduler = sched_api.Scheduler(self, self.node_list, self.node_resources)
        self.handler = node_handler.NodeHandler(self)

    # 运行grpc server, 调用do_work
    def start(self):
        self.server_t.start()
        time.sleep(1)
        self.handler.create_clients()
        self.handler.do_work()


if __name__ == '__main__':
    server_t = server_node.ServerThread("server", 50051)
    node = Node(server_t)
    node.start()

    time.sleep(60 * 60 * 24)

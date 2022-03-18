import asyncio
import time

import server_node
import client_node
from tools import utils
from tools import sched
from tools import settings
import os

'''
    Class:      Node
    功能：      节点特征刻画
    function:
                __init__    - 初始化线程类
                start       - 启动线程, 开始测试
                do_work     - 测试代码封装
    attribute: 
                node            - 节点拓扑图, 存储集群中已知的所有节点的地址
                node_resources  - 节点资源抽象特征, 存储节点当前资源使用情况
                server_t        - grpc server 线程
                client_t        - client线程, 封装测试代码
                self.sched      - 调度策略
'''


class Node:
    # all available nodes
    nodes = [
        # ['localhost', 50051]
        # ,['localhost', 50052]
        # ,['localhost', 50053]
    ]

    # 节点资源映射关系
    # {"localhost:50051":resource}
    node_resources = {}

    server_t = None
    # 可有多个发送者，每个client连接一个server
    client_list = []
    # 任务节点性能表
    task_node_table = {"smp": [], "ywd": [], "hwj": []}

    def __init__(self, server_t):
        server_t.node = self
        self.server_t = server_t
        self.scheduler = sched.Scheduler(self, self.nodes, self.node_resources)
        self.init_table()
        if settings.env == "dev":
            self.nodes = [
                ['localhost', 50051]
            ]
        else:
            self.nodes = [
                ['localhost', 50051]
                , ['localhost', 50052]
                , ['localhost', 50053]
            ]

    # 运行grpc server, 调用do_work
    def start(self):
        # start server
        self.server_t.start()
        time.sleep(1)
        self.create_clients()
        self.do_work()

    # 通过调度模块方法获取节点地址, 开始进行测试
    def do_work(self):
        # 本机测试
        if settings.env == "dev":
            for client in self.client_list:
                # 给每个client添加任务
                client.add_tasks(range(7))
        else:
            # 联机测试
            task_list = utils.get_random()
            print(task_list)
            res = self.scheduler.divide_tasks(task_list, self.node_resources, self.task_node_table)
            print(res)
            for i in range(3):
                self.client_list[i].add_tasks(res[i])

    # 对每个node建立一个client与之连接
    def create_clients(self):
        for node in self.nodes:
            ip, port = node[0], node[1]
            client_t = client_node.ClientThread("client", ip, port, self.server_t.addr)
            client_t.start()
            self.client_list.append(client_t)
            time.sleep(1)

    # init task_node_table
    def init_table(self):
        smp1 = sched.TaskCost(2.5, 300, 4000, 200)
        smp2 = sched.TaskCost(8.6, 300, 4000, 200)
        smp3 = sched.TaskCost(15.7, 300, 4000, 200)
        smp4 = sched.TaskCost(0.3, 300, 4000, 200)
        smp5 = sched.TaskCost(1, 300, 4000, 200)

        ywd1 = sched.TaskCost(2.6, 300, 4000, 200)
        ywd2 = sched.TaskCost(7.3, 300, 4000, 200)
        ywd3 = sched.TaskCost(30, 300, 4000, 200)
        ywd4 = sched.TaskCost(0.4, 300, 4000, 200)
        ywd5 = sched.TaskCost(0.9, 300, 4000, 200)

        hwj1 = sched.TaskCost(0.9, 300, 4000, 200)
        hwj2 = sched.TaskCost(4.7, 300, 4000, 200)
        hwj3 = sched.TaskCost(10.5, 300, 4000, 200)
        hwj4 = sched.TaskCost(0.2, 300, 4000, 200)
        hwj5 = sched.TaskCost(0.3, 300, 4000, 200)

        smp = [smp1, smp2, smp3, smp4, smp5]
        hwj = [hwj1, hwj2, hwj3, hwj4, hwj5]
        ywd = [ywd1, ywd2, ywd3, ywd4, ywd5]

        self.task_node_table = {"smp": smp, "ywd": ywd, "hwj": hwj}


if __name__ == '__main__':
    server_t = server_node.ServerThread("server", 50051)
    node = Node(server_t)
    node.start()

    time.sleep(60 * 60 * 24)

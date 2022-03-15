import time

import server_node
import client_node
from tools import utils
from tools import sched
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
        ['localhost', 50051],
        ['localhost', 50052],
        ['localhost', 50053]
    ]

    # 节点资源映射关系
    # {"localhost:50051":resource}
    node_resources = {}

    server_t = None
    client_t = None

    def __init__(self, server_t):
        server_t.node = self
        self.server_t = server_t
        self.sched = sched.Scheduler(self, self.nodes, self.node_resources)

    # 运行grpc server, 调用do_work
    def start(self):
        # start server
        self.server_t.start()
        time.sleep(1)
        self.do_work()

    # 通过调度模块方法获取节点地址, 开始进行测试
    def do_work(self):
        ip, port = self.sched.sched()
        client_t = client_node.ClientThread("client", ip, port, self.server_t.addr)
        client_t.start()
        time.sleep(1)


if __name__ == '__main__':
    server_t = server_node.ServerThread("server", 50051)
    node = Node(server_t)
    node.start()

    time.sleep(60 * 60 * 24)

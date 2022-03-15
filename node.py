import time

import server_node
import client_node
from tools import utils
from tools import sched
import os


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

    def start(self):
        # start server
        self.server_t.start()
        time.sleep(1)
        self.do_work()

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

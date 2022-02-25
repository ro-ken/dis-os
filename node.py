import time

import server_node
import client_node
from proto import task_pb2, task_pb2_grpc


def calc_weight(resource):
    cpu = resource.cpu
    mem = resource.mem
    cpu_weight = cpu.logic_num * cpu.use_ratio
    mem_weight = mem.available
    weight = cpu_weight * 0.8 + mem_weight * 0.2
    return weight


def select_max_weight(weights):
    key = None
    max_weight = 0
    for item in weights:
        if weights[item] > max_weight:
            key = item
    return key


def select_by_resource(node_resources):
    weights = {}
    for item in node_resources:
        weight = calc_weight(node_resources[item])
        weights[item] = weight

    key = select_max_weight(weights)
    ip = key.split(':')[0]
    port = key.split(':')[1]

    addr = task_pb2.Addr(ip=ip, port=port)
    return addr


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

    loop_turn = 0

    server_t = None
    client_t = None

    def __init__(self, server_t):
        server_t.node = self
        self.server_t = server_t

    def start(self):
        # start server
        self.server_t.start()
        time.sleep(1)
        self.do_work()

    def do_work(self):
        ip, port = self.sched()
        client_t = client_node.ClientThread("client", ip, port, self.server_t.addr)
        client_t.start()
        time.sleep(1)

    # 选择一个ip，port
    def sched(self):
        # return self.sched_by_loop()
        return self.sched_by_resource()

    # 轮询调度算法
    def sched_by_loop(self):
        ip = self.nodes[self.loop_turn][0]
        port = self.nodes[self.loop_turn][1]
        self.loop_turn += 1
        self.loop_turn %= len(self.nodes) - 1
        return ip, port

    # 根据资源调度
    def sched_by_resource(self):
        if len(self.node_resources) == 0:
            ip = self.server_t.addr.ip
            port = self.server_t.addr.port
            return ip, port
        else:
            addr = select_by_resource(self.node_resources)
            return addr.ip, addr.port


if __name__ == '__main__':
    # server_node.start('50051')
    # client_node.start('localhost','50051')
    server_t = server_node.ServerThread("server", 50051)
    node = Node(server_t)
    node.start()

    time.sleep(60 * 60 * 24)

import json
from datetime import time

import numpy as np

from tools import utils


class Scheduler:

    def __init__(self, node, nodes, node_resources):
        self.node = node  # 本节点
        self.nodes = nodes  # 所有节点
        self.node_resources = node_resources
        self.loop_turn = 0

    # 根据调度原则选择一个ip，port
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
            ip = self.node.server_t.addr.ip
            port = self.node.server_t.addr.port
            return ip, port
        else:
            addr = utils.select_by_resource(self.node_resources)
            return addr.ip, addr.port

    def divide_tasks(self, task_list, node_resources, task_node_table):
        res = {"smp": [], "ywd": [], "hwj": []}
        t_time = {"smp": 0, "ywd": 0, "hwj": 0}

        for task in task_list:
            node = self.select_min_time_node(task_node_table, t_time, task)
            res[node].append(task)
            t_time[node] += task_node_table[node][task].time
        print(t_time)
        return [res["smp"], res["ywd"], res["hwj"]]
        # return res

    def select_min_time_node(self, task_node_table, t_time, task) -> str:
        node = "smp"
        next_node = "hwj"
        if task_node_table[node][task].time + t_time[node] > task_node_table[next_node][task].time + t_time[next_node]:
            node = next_node
        next_node = "ywd"
        if task_node_table[node][task].time + t_time[node] > task_node_table[next_node][task].time + t_time[next_node]:
            node = next_node
        return node


class TaskCost:

    def __init__(self, time, cpu, mem, disc):
        self.time = time
        self.cpu = cpu
        self.mem = mem
        self.disc = disc


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)

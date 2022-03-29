from tools import utils

# 调度器接口，具体的调度器要实现里面的调度方法
class IScheduler:

    def __init__(self, node):
        self.node = node  # 本节点
        self.nodes = node.conn_node_list  # 所有节点
        self.loop_turn = 0

    # 动态选择一个节点
    def choose_node(self):
        pass

    # 从任务集群中划分出几个任务
    def divide_tasks(self, task_list) -> list:
        pass


class TaskCost:

    def __init__(self, time, cpu, mem, disc):
        self.time = time
        self.cpu = cpu
        self.mem = mem
        self.disc = disc

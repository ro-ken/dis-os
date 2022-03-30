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
    def divide_tasks(self, task_list, node_list) -> map:
        """

        Args:
            node_list: 可划分的节点集合,例如{key1:node1,key2:node2}
            task_list: 待划分的任务集合，例如[1,1,2,2,3,3,4,4]

        return 划分的任务列表
                划分列表的个数为当前节点连接的其他节点个数
                例如：{key1:[1,2,3],key2:[2,3,4],key3:[1,4]}

        """
        pass


class TaskCost:

    def __init__(self, time, cpu, mem, disc):
        self.time = time
        self.cpu = cpu
        self.mem = mem
        self.disc = disc

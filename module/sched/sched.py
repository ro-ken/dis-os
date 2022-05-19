import settings
from tools import utils


# 调度器接口，具体的调度器要实现里面的调度方法
class IScheduler:

    def __init__(self, node):
        self.node = node  # 本节点
        self.nodes = node.conn_node_list  # 所有节点

    # 从当前节点中选择一个节点
    def get_node(self):
        raise NotImplementedError

    # 把任务切分
    def sched(self, task_list, node_list):
        """

        Args:
            node_list: 可划分的节点集合,例如{key1:node1,key2:node2}
            task_list: 待划分的任务集合，例如[1,1,2,2,3,3,4,4]

        return 划分的任务列表
                划分列表的个数为当前节点连接的其他节点个数
                例如：{key1:[1,2,3],key2:[2,3,4],key3:[1,4]}

        """
        if settings.single_task:
            task = task_list.pop(0)  # 每次分配一个任务
            return self.single_task_sched(task, node_list)
        else:
            return self.multi_task_sched(task_list, node_list)

    # 单任务分配，可以重写,默认调用多任务分配方案
    def single_task_sched(self, task, node_list):
        return self.multi_task_sched([task], node_list)

    # 多任务分配，必须重写
    def multi_task_sched(self, task_list, node_list):
        raise NotImplementedError

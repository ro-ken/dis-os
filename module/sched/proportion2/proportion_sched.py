import settings
from module.sched.sched import IScheduler
from .static_tbl import prop_tbl_api
from .static_tbl import *
from threading import Lock


# 增强的比例分配，选取前面能用的进行分配

class Scheduler(IScheduler):

    def __init__(self, node):
        super().__init__(node)
        self.send_node = settings.arch      # 发送节点
        self.lock = Lock()      # 下面两个函数不能交替运行

    # 实现接口,选择权重最大的节点进行分配
    def get_node(self):
        self.lock.acquire()

        max_w = 0   # 最大权值
        max_node = None  # 最大权值的节点

        for node in self.nodes.values():
            if node.rank >= 0:   # 默认 -1 , rank >= 0说明性能较好
                prop = prop_tbl_api(self.send_node,node.name)
                weight = prop / node.allocated_num      # 计算权重
                if weight > max_w:
                    max_w = weight
                    max_node = node

        print('max_node:{}  weight={}'.format(max_node.name,max_w))
        max_node.allocated_num += 1

        self.lock.release()
        return max_node


    # 按照性能强弱排序所有已连接的表
    def sort_node_list(self):

        self.lock.acquire()

        for node in self.nodes.values():
            node.rank = -1  # 重置排名
            node.allocated_num = 1  # 重置分配帧数

        # 选出前need_node_num个节点
        for i in range(need_node_num):
            max_val = 0
            max_node = None
            for node in self.nodes.values():
                if node.can_allocated and (node.rank == -1):
                    val = prop_tbl_api(None, node.name)
                    if val > max_val:
                        max_val = val
                        max_node = node

            if max_node is not None:
                max_node.rank = i
                print("rank {} :{}".format(i,max_node.name))

        self.lock.release()
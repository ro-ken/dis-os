import settings
from module.sched.sched import IScheduler
from .static_tbl import prop_tbl_api

# 按照固定比例分配
class Scheduler(IScheduler):

    def __init__(self, node):
        super().__init__(node)
        self.send_node = settings.arch      # 发送节点

    # 实现接口,选择权重最大的节点进行分配
    def get_node(self):

        max_w = 0   # 最大权值
        max_node = None  # 最大权值的节点

        for node in self.nodes.values():
            prop = prop_tbl_api(self.send_node,node.name)
            weight = prop / node.allocated_num      # 计算权重
            if weight > max_w:
                max_w = weight
                max_node = node

        print('max_node:{}  weight={}'.format(max_node.name,max_w))
        max_node.allocated_num += 1
        return max_node

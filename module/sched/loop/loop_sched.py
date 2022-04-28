from module.sched.sched import IScheduler


# 轮转调度，每个节点依次循环调度
class Scheduler(IScheduler):

    def __init__(self, node):
        super().__init__(node)
        self.loop_turn = 0  # 轮转值

    # 实现接口
    def get_node(self):
        node_list = list(self.nodes.values())  # 获取所有节点组成一个list
        self.loop_turn += 1
        self.loop_turn %= len(node_list)
        print('now turn num is : {}'.format(self.loop_turn))
        node = node_list[self.loop_turn]  # 当前选择的节点
        return node

from tools import utils

class Scheduler:

    def __init__(self,node,nodes,node_resources):
        self.node = node # 本节点
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


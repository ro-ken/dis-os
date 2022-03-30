from tools import utils
from module.sched.sched import IScheduler


class Scheduler(IScheduler):

    # 根据调度原则选择一个ip，port
    def choose_node(self):
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
        if len(self.node.node_resources) == 0:
            ip = self.node.server_t.addr.ip
            port = self.node.server_t.addr.port
            return ip, port
        else:
            addr = utils.select_by_resource(self.node.node_resources)
            return addr.ip, addr.port

    def divide_tasks(self, task_list,node_list):
        pass

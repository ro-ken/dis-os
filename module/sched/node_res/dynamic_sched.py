from tools import utils
from module.sched.sched import IScheduler

# 根据资源调度，过时了，未更新
class Scheduler(IScheduler):

    # 根据资源调度
    def sched_by_resource(self):
        if len(self.node.node_resources) == 0:
            ip = self.node.server_t.addr.ip
            port = self.node.server_t.addr.port
            return ip, port
        else:
            addr = utils.select_by_resource(self.node.node_resources)
            return addr.ip, addr.port

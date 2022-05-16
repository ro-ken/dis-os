
# 已连接其他节点的一些信息
class NodeInfo:

    def __init__(self, key, client, name):
        self.key = key              # key = "ip:port"
        self.client = client        # 连接的client线程
        self.res = None             # 该node的资源
        self.name = name            # 该node的name

        # 调度
        self.tasks = []             # 该node的运行任务队列

        self.run_tasks = []         # 该节点分配给本节点的任务序列
        self.task_start_time = 0    # 该节点派发到本节点运行任务的起始时间 后面程序用 time.time()获取

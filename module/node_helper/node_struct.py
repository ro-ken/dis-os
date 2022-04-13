class NodeInfo:

    def __init__(self, key, client):
        self.key = key          # key = "ip:port"
        self.client = client    # 连接的client线程
        self.res = None         # 该node的资源
        self.name = ''          # 该node的name
        self.tasks = []         # 该node的运行任务队列

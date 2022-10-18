
import socket

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

        # proportion  调度
        self.allocated_num = 1      # 已分配的帧数
        self.can_allocated = True   # 该节点是否可以分配任务
        self.rank = -1              # 强弱排名，到时候会选择几个较强的节点


# udp的client和server

class UDPClient:
    def __init__(self, server, ip, port):
        self.server = server  # 负责接受的server
        self.ip_port = (ip, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    # 发送消息
    def send(self, msg):
        print("send data", msg)
        self.client.sendto(msg.encode(), self.ip_port)

    # 发送并接受
    def send_recv(self, msg):
        self.send(msg)
        data = self.server.recv()
        return data


class UDPServer:
    def __init__(self, ip, port):
        self.ip_port = (ip, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.server.bind(self.ip_port)

    def recv(self):
        data = self.server.recv(1024).strip().decode()
        print("recv data:", data)
        return data

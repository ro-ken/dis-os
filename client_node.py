import asyncio
import threading
import time
from time import sleep

import grpc

from module.proto import task_pb2_grpc
from module.task_helper import client_handler
from module.task_helper import task_testy

# 客户端线程，发送任务
class ClientThread(threading.Thread):

    def __init__(self, ip, port, node):
        threading.Thread.__init__(self)
        self.ip = ip  # 要连接的server的ip
        self.port = port  # 要连接server的port
        self.node = node  # client依附的节点
        self.task_queue = []  # 待处理队列，里面存任务编号 [序号1，序号2...]
        self.handler = None  # 客户节点的辅助类
        self.stub = None    # grpc 代理
        self.stop = False  # 若为True 该线程结束
        self.frame_queue = [] # 待处理帧的队列 [（帧1，序号1），（帧2，序号2）...]
        self.frame_fin = False      # 主节点的帧是否处理完成

    # 启动client发送任务
    def run(self) -> None:
        with grpc.insecure_channel(self.ip + ":" + str(self.port)) as channel:
            stub = task_pb2_grpc.TaskServiceStub(channel)
            self.stub = stub
            self.handler = client_handler.ClientHandler(self, stub)

            self.handler.task_running()             # 任务运行
            # self.handler.task_test()              # 任务测试

            self.wait_for_stop()

    def wait_for_stop(self):
        while not self.stop:
            time.sleep(1)


# 启动测试代码
def start(ip, port):
    client = ClientThread(ip, port, None)
    client.start()
    sleep(1)
    client.handler.add_tasks(range(7))
    client.join()


if __name__ == '__main__':
    start('localhost', 50051)

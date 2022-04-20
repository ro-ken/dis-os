import asyncio
import threading
import time
from time import sleep

import grpc

from module.proto import task_pb2_grpc
from module.task_helper import client_handler


class ClientThread(threading.Thread):

    def __init__(self, ip, port, node):
        threading.Thread.__init__(self)
        self.ip = ip    # 要连接的server的ip
        self.port = port   # 要连接server的port
        self.node = node  # client依附的节点
        self.task_queue = []  # 待处理队列
        self.handler = None # 客户节点的辅助类
        self.stop = False   # 若为True 该线程结束

    # 启动client发送任务
    def run(self) -> None:
        with grpc.insecure_channel(self.ip + ":" + str(self.port)) as channel:
            stub = task_pb2_grpc.TaskServiceStub(channel)
            self.handler = client_handler.ClientHandler(self, stub)

            time.sleep(1)  # 等node把表项先创建好
            asyncio.run(self.handler.async_task())

# 启动测试代码
def start(ip, port):
    client = ClientThread(ip, port, None)
    client.start()
    sleep(1)
    client.handler.add_tasks(range(7))
    client.join()


if __name__ == '__main__':
    start('localhost', 50051)

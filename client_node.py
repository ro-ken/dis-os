import asyncio
import threading
import time
from time import sleep

import grpc

from module.proto import task_pb2_grpc
from module.task_helper import client_handler

'''
    Class:      ClientThread
    功能：      线程, 封装了客户端调用grpc和应用的函数, 继承threading模块的Thread类
    function:
                __init__    - 初始化线程类的属性
                run         - 封装测试代码, 模拟client调用grpc server方法
                task_test   - 封装应用接口, 调用全部的应用
                five_solution   - 应用性能测试, 测试应用的运行时间, 消耗资源(CPU, 内存)[特定于指定的五种分配方案]
                solution        - 节点环境检测, 根据不同的节点调用不同的应用接口
    attribute: 
                stub            - grpc客户端, 通过这个调用grpc server方法
                task_handler    - 未知
                self.name       - 
                self.port       - grpc server的端口号
                self.addr       - grpc server的ip地址
                self.node       - 当前节点硬件资源特征抽象
'''


class ClientThread(threading.Thread):

    def __init__(self, ip, port, node):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.node = node  # client依附的节点
        self.task_queue = []  # 待处理队列
        self.disconnect = False  # 连接是否已经断开
        self.handler = None
        self.stop = False

    # 启动client发送任务
    def run(self) -> None:
        with grpc.insecure_channel(self.ip + ":" + str(self.port)) as channel:
            stub = task_pb2_grpc.TaskServiceStub(channel)
            self.handler = client_handler.ClientHandler(self, stub)

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


# packge
import threading
import time
from concurrent import futures
import grpc
import numpy as np
from cv2 import cv2

# tool
from tools import utils
from settings import arch
from module.task_helper.task_service import TaskService
from tools.utils import ROOT
from module.proto import task_pb2_grpc, task_pb2

# model
from app.app_api import *

'''
    Class:      ServerThread
    功能：      线程, 封装grpc的服务器启动代码, 继承threading模块的Thread类, 重写了run方法,
    function:
                __init__    - 初始化线程类的属性
                run         - 封装grpc的服务器启动代码
    attribute: 
                self.name - 
                self.port - grpc server的端口号
                self.addr - grpc server的ip地址
                self.node - 当前节点硬件资源特征抽象
'''
class ServerThread(threading.Thread):
    def __init__(self, name, port):
        threading.Thread.__init__(self)
        self.name = name
        self.port = port
        self.addr = None
        self.node = None

    # 开启服务器
    def run(self) -> None:
        # 初始化 grpc server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service = TaskService(self.node)
        task_pb2_grpc.add_TaskServiceServicer_to_server(service, server)

        # 配置端口
        while True:
            try:
                server.add_insecure_port("[::]:" + str(self.port))
                break
            except:
                # print(str(self.port) + "端口已被占用！")
                self.port += 1

        # 运行grpc server
        server.start()
        self.addr = task_pb2.Addr(ip='localhost', port=self.port)
        print("server start... port = " + str(self.port))
        server.wait_for_termination()


def start(port):
    server = ServerThread("server", port)
    server.start()
    return server


if __name__ == '__main__':
    server = start(50051)
    server.join()

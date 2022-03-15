
# packge
import threading
import time
from concurrent import futures
import grpc
import numpy as np
from cv2 import cv2

# tool
from tools import utils
from tools.settings import arch
from tools.task_service import TaskService
from tools.utils import ROOT
from tools.proto import task_pb2_grpc, task_pb2

# model
from model.api import *

# 服务器线程
class ServerThread(threading.Thread):
    def __init__(self, name, port):
        threading.Thread.__init__(self)
        self.name = name
        self.port = port
        self.addr = None
        self.node = None

    # 开启服务器
    def run(self) -> None:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service = TaskService(self.node)
        task_pb2_grpc.add_TaskServiceServicer_to_server(service, server)
        while True:
            try:
                server.add_insecure_port("[::]:" + str(self.port))
                break
            except:
                # print(str(self.port) + "端口已被占用！")
                self.port += 1

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

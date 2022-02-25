import threading
import time
from concurrent import futures
from model.ai import ai

import grpc
import numpy as np
from cv2 import cv2

from proto import task_pb2_grpc, task_pb2
from model.yolox.tools import demo

def addr2key(addr):
    return addr.ip + ":" + str(addr.port)


# 实现服务
class TaskService(task_pb2_grpc.TaskServiceServicer):

    def __init__(self, node):
        self.node = node

    def task_service_1(self, request, context):
        print("收到请求：", request)
        reply = task_pb2.CommonReply(success=True)
        return reply

    def send_file(self, request, context):
        file_name = request.file_name
        file_data = request.file_data
        f = open(file_name + '.bak', 'wb')
        f.write(file_data)
        f.close()
        reply = task_pb2.CommonReply(success=True)
        return reply

    def send_resource(self, request, context):
        addr = request.addr
        resource = request.resource
        # 把资源放入节点资源表中
        self.node.node_resources[addr2key(addr)] = resource
        print(self.node.node_resources)
        reply = task_pb2.CommonReply(success=True)
        return reply

    def send_image(self, request, context):
        str_encode = request.img
        nparr = np.frombuffer(str_encode, np.uint8)
        img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img_res = demo.start(img_decode)
        cv2.imshow('img', img_res)
        cv2.waitKey()
        return task_pb2.CommonReply(success=True)

    def send_ai(self, request, context):
        ai.run()
        return task_pb2.CommonReply(success=True)

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

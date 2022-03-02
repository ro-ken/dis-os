import threading
import time
from concurrent import futures
from model.ai import ai

import grpc
import numpy as np
from cv2 import cv2

from my_tools import ROOT
from proto import task_pb2_grpc, task_pb2
from model.yolox.tools import demo
from model.yolo5 import detect
from model.face_ai.faceai import compose
import my_tools


# 实现服务
class TaskService(task_pb2_grpc.TaskServiceServicer):

    def __init__(self, node):
        self.node = node

    def task_service_1(self, request, context):
        print("收到请求：", request)
        reply = task_pb2.CommonReply(success=True)
        return reply

    def send_file(self, request, context):
        path = ROOT + request.file_name + '.bak'
        my_tools.write_file(path, request.file_data)
        reply = task_pb2.CommonReply(success=True)
        return reply

    def send_resource(self, request, context):
        addr = request.addr
        resource = request.resource
        # 把资源放入节点资源表中
        self.node.node_resources[my_tools.addr2key(addr)] = resource
        print(self.node.node_resources)
        reply = task_pb2.CommonReply(success=True)
        return reply

    def send_image(self, request, context):
        str_encode = request.img
        img = my_tools.img_decode(str_encode)
        img_res = demo.start(img)
        cv2.imshow('img', img_res)
        cv2.waitKey()
        return task_pb2.CommonReply(success=True)

    def send_image_2(self, request, context):
        str_encode = request.img
        img = my_tools.img_decode(str_encode)
        img_res = demo.start(img)
        str_encode = my_tools.img_encode(img_res, '.jpg')
        reply = task_pb2.Image(img=str_encode)
        return reply

    def send_vedio(self, request_iterator, context):
        for image in request_iterator:
            str_encode = image.img
            img = my_tools.img_decode(str_encode)
            img_res = demo.start(img)
            cv2.imshow('img', img_res)
            cv2.waitKey(1)
            str_encode = my_tools.img_encode(img_res, '.jpg')
            reply = task_pb2.Image(img=str_encode)
            yield reply

    def send_yolo5(self, request, context):
        print('--------------------start deal with yolo5 request-----------')
        in_path = ROOT + 'model/yolo5/input/' + request.file_name
        my_tools.write_file(in_path, request.file_data)
        detect.start(in_path)
        out_path = ROOT + 'model/yolo5/output/' + request.file_name
        img_req = my_tools.get_image_req(out_path)
        print('--------------------finish deal with yolo5 request-----------')
        return img_req

    def send_ai(self, request, context):
        ai.run()
        return task_pb2.CommonReply(success=True)

    def send_face_ai(self, request, context):
        print('--------------------start deal with face_ai request-----------')
        str_encode = request.img
        img = my_tools.img_decode(str_encode)
        str_encode = request.img_compose
        img_compose = my_tools.img_decode(str_encode)
        img_out = compose.start(img, img_compose)
        str_encode = my_tools.img_encode(img_out, '.png')
        reply = task_pb2.Image(img=str_encode)
        print('--------------------finish deal with face_ai request-----------')
        return reply


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

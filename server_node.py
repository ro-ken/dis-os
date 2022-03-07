import threading
import time
from concurrent import futures
from model.ai import ai

import grpc
import numpy as np
from cv2 import cv2

from tools.utils import ROOT
from proto import task_pb2_grpc, task_pb2
from model.yolox.tools import demo
from model.yolo5 import detect
from model.face_ai.faceai import compose
from model.lic_detect import detect_rec_img
from model.style_transfer import train
from tools import utils


# 实现服务
class TaskService(task_pb2_grpc.TaskServiceServicer):

    def __init__(self, node):
        self.node = node

    def task_test(self, request, context):
        print("收到请求：", request)
        reply = task_pb2.CommonReply(success=True)
        return reply

    def task_transfer_file(self, request, context):
        path = ROOT + request.file_name + '.bak'
        utils.write_file(path, request.file_data)
        reply = task_pb2.CommonReply(success=True)
        return reply

    def task_get_res(self, request, context):
        addr = request.addr
        resource = request.resource
        # 把资源放入节点资源表中
        self.node.node_resources[utils.addr2key(addr)] = resource
        print(self.node.node_resources)
        reply = task_pb2.CommonReply(success=True)
        return reply

    def send_image(self, request, context):
        str_encode = request.img
        img = utils.img_decode(str_encode)
        img_res = demo.start(img)
        cv2.imshow('img', img_res)
        cv2.waitKey()
        return task_pb2.CommonReply(success=True)

    def task_yolox_image(self, request, context):
        print('--------------------start deal with yolox image request-----------')
        str_encode = request.img
        img = utils.img_decode(str_encode)
        img_res = demo.start(img)
        str_encode = utils.img_encode(img_res, '.jpg')
        reply = task_pb2.Image(img=str_encode)
        print('--------------------finish deal with yolox image request-----------')
        return reply

    def task_yolox_vedio(self, request_iterator, context):
        print('--------------------start deal with yolox vedio request-----------')
        for image in request_iterator:
            str_encode = image.img
            img = utils.img_decode(str_encode)
            img_res = demo.start(img)
            # cv2.imshow('img', img_res)
            # cv2.waitKey(1)
            str_encode = utils.img_encode(img_res, '.jpg')
            reply = task_pb2.Image(img=str_encode)
            yield reply
        print('--------------------finish deal with yolox vedio request-----------')

    def task_yolo5(self, request, context):
        print('--------------------start deal with yolo5 request-----------')
        in_path = ROOT + 'model/yolo5/input/' + request.file_name
        utils.write_file(in_path, request.file_data)
        detect.start(in_path)
        out_path = ROOT + 'model/yolo5/output/' + request.file_name
        img_req = utils.get_image_req(out_path)
        print('--------------------finish deal with yolo5 request-----------')
        return img_req

    def task_style_transfer(self, request, context):
        print('--------------------start deal with style_transfer request-----------')
        content_path = ROOT + 'model/style_transfer/input/' + request.content.file_name
        utils.write_file(content_path, request.content.file_data)
        style_path = ROOT + 'model/style_transfer/input/' + request.style.file_name
        utils.write_file(style_path, request.style.file_data)
        train.start(content_path,style_path)
        out_path = ROOT + 'model/style_transfer/output/' + 'out.jpg'
        img_req = utils.get_image_req(out_path)
        print('--------------------finish deal with style_transfer request-----------')
        return img_req


    def task_ai(self, request, context):
        ai.run()
        return task_pb2.CommonReply(success=True)

    def task_lic_detect(self, request, context):
        print('--------------------start deal with lic detect request-----------')
        str_encode = request.img
        img = utils.img_decode(str_encode)
        img_res = detect_rec_img.start(img)
        str_encode = utils.img_encode(img_res, '.jpg')
        reply = task_pb2.Image(img=str_encode)
        print('--------------------finish deal with lic detect request-----------')
        return reply

    def task_face_ai(self, request, context):
        print('--------------------start deal with face_ai request-----------')
        str_encode = request.img
        img = utils.img_decode(str_encode)
        str_encode = request.img_compose
        img_compose = utils.img_decode(str_encode)
        img_out = compose.start(img, img_compose)
        str_encode = utils.img_encode(img_out, '.png')
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

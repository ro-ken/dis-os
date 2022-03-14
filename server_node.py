
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
from tools.utils import ROOT
from proto import task_pb2_grpc, task_pb2

# model
from model.api import *


# 实现服务
class TaskService(task_pb2_grpc.TaskServiceServicer):

    def __init__(self, node):
        self.node = node

    def task_test(self, request, context):
        utils.server_task_start("task_test")

        # print("收到请求：", request)
        reply = task_pb2.CommonReply(success=True)

        utils.server_task_end("task_test")
        return reply

    def task_transfer_file(self, request, context):
        utils.server_task_start("task_transfer_file")

        path = ROOT + request.file_name + '.bak'
        # utils.write_file(path, request.file_data)
        reply = task_pb2.CommonReply(success=True)

        utils.server_task_end("task_transfer_file")
        return reply

    def task_get_res(self, request, context):
        utils.server_task_start("task_get_res")

        addr = request.addr
        resource = request.resource
        # 把资源放入节点资源表中
        self.node.node_resources[utils.addr2key(addr)] = resource
        # print(self.node.node_resources)
        reply = task_pb2.CommonReply(success=True)

        utils.server_task_end("task_get_res")
        return reply

    def send_image(self, request, context):
        utils.server_task_start("send_image")

        str_encode = request.img
        img = utils.img_decode(str_encode)
        img_res = yolo_x.start(img)
        cv2.imshow('img', img_res)
        cv2.waitKey()

        utils.server_task_end("send_image")
        return task_pb2.CommonReply(success=True)

    def task_yolox_image(self, request, context):
        utils.server_task_start("task_yolox_image")

        str_encode = request.img
        img = utils.img_decode(str_encode)
        img_res = yolo_x.start(img)
        str_encode = utils.img_encode(img_res, '.jpg')
        reply = task_pb2.Image(img=str_encode)

        utils.server_task_end("task_yolox_image")
        return reply

    def task_yolox_vedio(self, request_iterator, context):
        utils.server_task_start("task_yolox_vedio")

        for image in request_iterator:
            str_encode = image.img
            img = utils.img_decode(str_encode)
            img_res = yolo_x.start(img)
            # cv2.imshow('img', img_res)
            # cv2.waitKey(1)
            str_encode = utils.img_encode(img_res, '.jpg')
            reply = task_pb2.Image(img=str_encode)
            yield reply

        utils.server_task_end("task_yolox_vedio")

    def task_yolo5(self, request, context):
        utils.server_task_start("task_yolo5")

        in_path = ROOT + 'model/yolo_5/input/' + request.file_name
        utils.write_file(in_path, request.file_data)
        # detect.start(in_path)     # 非windows错误
        yolo_5.start(None)
        out_path = ROOT + 'model/yolo_5/output/' + request.file_name
        img_req = utils.get_image_req(out_path)

        utils.server_task_end("task_yolo5")
        return img_req

    def task_style_transfer(self, request, context):
        utils.server_task_start("task_style_transfer")

        content_path = ROOT + 'model/style_transfer/input/' + request.content.file_name
        utils.write_file(content_path, request.content.file_data)
        style_path = ROOT + 'model/style_transfer/input/' + request.style.file_name
        utils.write_file(style_path, request.style.file_data)
        style_transfer.start(content_path, style_path)
        out_path = ROOT + 'model/style_transfer/output/' + 'out.jpg'
        img_req = utils.get_image_req(out_path)

        utils.server_task_end("task_style_transfer")
        return img_req

    def task_ai(self, request, context):
        utils.server_task_start("task_ai")

        linear_regression.run()

        utils.server_task_end("task_ai")
        return task_pb2.CommonReply(success=True)

    def task_num_detect(self, request, context):
        utils.server_task_start("task_num_detect")

        num_detect.predict_number()

        utils.server_task_end("task_num_detect")
        return task_pb2.CommonReply(success=True)

    def task_lic_detect(self, request, context):
        utils.server_task_start("task_lic_detect")

        str_encode = request.img
        img = utils.img_decode(str_encode)
        img_res = lic_detect.start(img)
        str_encode = utils.img_encode(img_res, '.jpg')
        reply = task_pb2.Image(img=str_encode)

        utils.server_task_end("task_lic_detect")
        return reply

    def task_face_ai(self, request, context):
        utils.server_task_start("task_face_ai")

        str_encode = request.img
        img = utils.img_decode(str_encode)
        str_encode = request.img_compose
        img_compose = utils.img_decode(str_encode)
        img_out = compose.start(img, img_compose)
        str_encode = utils.img_encode(img_out, '.png')
        reply = task_pb2.Image(img=str_encode)

        utils.server_task_end("task_face_ai")
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

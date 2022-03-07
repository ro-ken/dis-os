import os
import threading
import time
import grpc
import numpy as np
import psutil
from cv2 import cv2
from tools import utils
from tools.utils import ROOT

from proto import task_pb2, task_pb2_grpc


# client线程
class ClientThread(threading.Thread):
    stub = None

    def __init__(self, name, host, port, addr):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.port = port
        self.addr = addr  # 节点地址

    # 启动client发送任务
    def run(self) -> None:
        with grpc.insecure_channel(self.host + ":" + str(self.port)) as channel:
            stub = task_pb2_grpc.TaskServiceStub(channel)
            self.stub = stub
            # self.task_test()
            # self.task_ai()
            self.task_get_res()
            self.task_transfer_file()
            self.task_yolox_image()
            self.task_yolo5()
            self.task_face_ai()
            self.task_lic_detect()
            self.task_style_transfer()
            # self.task_yolox_vedio()

    def task_test(self):
        req = task_pb2.TaskRequest(task_id=1, task_name='task01')
        reply = self.stub.task_test(req)
        print(reply)

    def task_transfer_file(self):
        file_name = ROOT + 'README.md'
        req = utils.get_file_req(file_name)
        reply = self.stub.task_transfer_file(req)
        print(reply)

    def task_get_res(self):
        cpu = task_pb2.CPU(use_ratio=psutil.cpu_percent(0),
                           real_num=psutil.cpu_count(logical=False),
                           logic_num=psutil.cpu_count())
        mem = task_pb2.Memory(total=psutil.virtual_memory().total,
                              used=psutil.virtual_memory().used,
                              available=psutil.virtual_memory().available)
        disc = task_pb2.Disc(total=psutil.disk_usage('/').total,
                             used=psutil.disk_usage('/').used,
                             available=psutil.disk_usage('/').free)

        resource = task_pb2.Resource(cpu=cpu, mem=mem, disc=disc)
        request = task_pb2.ResourceRequest(addr=self.addr, resource=resource)
        reply = self.stub.task_get_res(request)

        print("send_resource.reply:", reply)

    def send_image(self, img_path):
        img_req = utils.get_image_req(img_path)
        reply = self.stub.send_image(img_req)
        print("send_img.reply:", reply)

    def task_yolox_image(self):
        img_path = ROOT + '/dataset/001.jpg'
        img_req = utils.get_image_req(img_path)
        reply = self.stub.task_yolox_image(img_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)
        cv2.imshow('img', img_res)
        cv2.waitKey()

    def task_ai(self):
        ai_req = task_pb2.AIRequesst()
        reply = self.stub.task_ai(ai_req)
        return reply

    def task_yolo5(self):
        file_name = ROOT + 'dataset/001.jpg'
        req = utils.get_file_req(file_name)
        reply = self.stub.task_yolo5(req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)
        cv2.imshow('img', img_res)
        cv2.waitKey(0)

    def task_style_transfer(self):
        # content_path = ROOT + 'dataset/style-transfer/content.jpg'
        content_path = ROOT + 'dataset/style-transfer/content.jpg'
        style_path = ROOT + 'dataset/style-transfer/style.jpg'
        content_img = utils.get_file_req(content_path)
        style_img = utils.get_file_req(style_path)
        file_req = task_pb2.File_x2(content=content_img, style=style_img)
        reply = self.stub.task_style_transfer(file_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)
        cv2.imshow('img', img_res)
        cv2.waitKey()


    def get_img_iter(self, vedio):
        cap = cv2.VideoCapture(vedio)
        img_width = 360
        img_height = 640
        # 1280.0 720.0
        # print(cap.set(3,640.0))
        # print(cap.set(4,360.0))
        # cap.set(10, 130)
        while True:
            ret, frame = self.read_times(cap, 5)
            if ret:
                frame = cv2.resize(frame, (img_height, img_width))
                str_encode = utils.img_encode(frame, '.jpg')
                request = task_pb2.Image(img=str_encode)
                yield request
            else:
                break
        cap.release()

    def task_yolox_vedio(self):
        vedio_name = ROOT + '/dataset/test2.mp4'
        req_iter = self.get_img_iter(vedio_name)
        reply = self.stub.task_yolox_vedio(req_iter)
        for image in reply:
            str_encode = image.img
            img_res = utils.img_decode(str_encode)
            cv2.imshow('img', img_res)
            cv2.waitKey(1)
        print("vedio play finished")
        cv2.destroyAllWindows()

    def read_times(self, cap, times):
        for _ in range(times):
            cap.read()
        return cap.read()

    def task_face_ai(self):
        img_path = ROOT + 'dataset/face_ai/ag-3.png'
        img_compose_path = ROOT + 'dataset/face_ai/compose/maozi-1.png'
        img = utils.get_image_req(img_path, '.png').img
        img_compose = utils.get_image_req(img_compose_path, '.png').img
        img_2_req = task_pb2.Image_x2(img=img, img_compose=img_compose)
        reply = self.stub.task_face_ai(img_2_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)
        cv2.imshow('img', img_res)
        cv2.waitKey()

    def task_lic_detect(self):
        img_path = ROOT + 'dataset/lic/02.jpg'
        img_req = utils.get_image_req(img_path)
        reply = self.stub.task_lic_detect(img_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)
        cv2.imshow('img', img_res)
        cv2.waitKey()


def start(host, port):
    client = ClientThread("client", host, port, None)
    client.start()
    client.join()


if __name__ == '__main__':
    # start('localhost','50051')
    start('localhost', 50051)

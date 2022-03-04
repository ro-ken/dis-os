import os
import threading
import time
import grpc
import numpy as np
import psutil
from cv2 import cv2
import my_tools
from my_tools import ROOT

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
            # self.send_task()
            # self.send_ai('data.csv')
            # self.send_resource()
            # self.send_file(ROOT + 'README.md')
            # self.send_image(ROOT + 'dataset/01.jpg')
            self.send_image_2(ROOT + '/dataset/001.jpg')
            # self.send_vedio(ROOT + '/dataset/test2.mp4')
            # self.send_yolo5(ROOT + 'dataset/001.jpg')
            # self.send_face_ai()
            # self.send_lic_detect(ROOT + 'dataset/lic/02.jpg')
            # self.send_style_transfer()

    def send_task(self):
        req = task_pb2.TaskRequest(task_id=1, task_name='task01')
        reply = self.stub.task_service_1(req)
        print(reply)

    def send_file(self, file_name):
        req = my_tools.get_file_req(file_name)
        reply = self.stub.send_file(req)
        print(reply)

    def send_resource(self):
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
        reply = self.stub.send_resource(request)

        print("send_resource.reply:", reply)

    def send_image(self, img_path):
        img_req = my_tools.get_image_req(img_path)
        reply = self.stub.send_image(img_req)
        print("send_img.reply:", reply)

    def send_image_2(self, img_path):
        img_req = my_tools.get_image_req(img_path)
        reply = self.stub.send_image_2(img_req)
        str_encode = reply.img
        img_res = my_tools.img_decode(str_encode)
        cv2.imshow('img', img_res)
        cv2.waitKey()

    def send_ai(self, data):
        ai_req = task_pb2.AIRequesst()
        reply = self.stub.send_ai(ai_req)
        return reply

    def send_yolo5(self, file_name):
        req = my_tools.get_file_req(file_name)
        reply = self.stub.send_yolo5(req)
        str_encode = reply.img
        img_res = my_tools.img_decode(str_encode)
        cv2.imshow('img', img_res)
        cv2.waitKey()

    def send_style_transfer(self):
        # content_path = ROOT + 'dataset/style-transfer/content.jpg'
        content_path = ROOT + 'dataset/style-transfer/content.jpg'
        style_path = ROOT + 'dataset/style-transfer/style.jpg'
        content_img = my_tools.get_file_req(content_path)
        style_img = my_tools.get_file_req(style_path)
        file_req = task_pb2.File_x2(content=content_img, style=style_img)
        reply = self.stub.send_style_transfer(file_req)
        str_encode = reply.img
        img_res = my_tools.img_decode(str_encode)
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
                str_encode = my_tools.img_encode(frame, '.jpg')
                request = task_pb2.Image(img=str_encode)
                yield request
            else:
                break
        cap.release()

    def send_vedio(self, vedio_name):
        req_iter = self.get_img_iter(vedio_name)
        reply = self.stub.send_vedio(req_iter)
        for image in reply:
            str_encode = image.img
            img_res = my_tools.img_decode(str_encode)
            cv2.imshow('img', img_res)
            cv2.waitKey(1)
        print("vedio play finished")
        cv2.destroyAllWindows()

    def read_times(self, cap, times):
        for _ in range(times):
            cap.read()
        return cap.read()

    def send_face_ai(self):
        img_path = ROOT + 'dataset/face_ai/ag-3.png'
        img_compose_path = ROOT + 'dataset/face_ai/compose/maozi-1.png'
        img = my_tools.get_image_req(img_path, '.png').img
        img_compose = my_tools.get_image_req(img_compose_path, '.png').img
        img_2_req = task_pb2.Image_x2(img=img, img_compose=img_compose)
        reply = self.stub.send_face_ai(img_2_req)
        str_encode = reply.img
        img_res = my_tools.img_decode(str_encode)
        cv2.imshow('img', img_res)
        cv2.waitKey()

    def send_lic_detect(self, img_path):
        img_req = my_tools.get_image_req(img_path)
        reply = self.stub.send_lic_detect(img_req)
        str_encode = reply.img
        img_res = my_tools.img_decode(str_encode)
        cv2.imshow('img', img_res)
        cv2.waitKey()


def start(host, port):
    client = ClientThread("client", host, port, None)
    client.start()
    client.join()


if __name__ == '__main__':
    # start('localhost','50051')
    start('localhost', 50051)

import os
import threading
import time
import grpc
import numpy as np
import psutil
from cv2 import cv2
from tools import utils
from tools.utils import ROOT
from tools.settings import *

from proto import task_pb2, task_pb2_grpc


class ClientThread(threading.Thread):
    stub = None

    def __init__(self, name, host, port, addr):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.port = port
        self.addr = addr  # 节点地址
        #   taskid               0               1                   2               3                   4                       5                      6
        self.task_list = [self.task_ai, self.task_yolox_image, self.task_yolo5, self.task_face_ai, self.task_lic_detect, self.task_num_detect,self.task_style_transfer]

    def task(self):
        self.task_ai()
        self.task_yolox_image()
        self.task_yolo5()
        self.task_face_ai()
        self.task_lic_detect()
        self.task_num_detect()
        self.task_style_transfer()

    # 启动client发送任务
    def run(self) -> None:
        with grpc.insecure_channel(self.host + ":" + str(self.port)) as channel:
            stub = task_pb2_grpc.TaskServiceStub(channel)
            self.stub = stub
            self.task()
            #self.five_solution()

    def task_test(self):
        utils.client_task_start("task_test")

        req = task_pb2.TaskRequest(task_id=1, task_name='task01')
        reply = self.stub.task_test(req)

        if show_result:
            print(reply)

        utils.client_task_end("task_test")

    def task_transfer_file(self):
        utils.client_task_start("task_transfer_file")

        file_name = ROOT + 'README.md'
        req = utils.get_file_req(file_name)
        reply = self.stub.task_transfer_file(req)
        if show_result:
            print(reply)

        utils.client_task_end("task_transfer_file")

    def task_get_res(self):
        utils.client_task_start("task_get_res")

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
        if show_result:
            print("send_resource.reply:", reply)

        utils.client_task_end("task_get_res")

    # def send_image(self, img_path):
    #     utils.client_task_start("task_test")
    #
    #     img_req = utils.get_image_req(img_path)
    #     reply = self.stub.send_image(img_req)
    #     print("send_img.reply:", reply)
    #
    #     utils.client_task_end("task_test")

    def task_yolox_image(self):
        utils.client_task_start("task_yolox_image")

        img_path = ROOT + '/dataset/001.jpg'
        img_req = utils.get_image_req(img_path)
        reply = self.stub.task_yolox_image(img_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)

        utils.client_task_end("task_yolox_image")

        if show_result:
            utils.imshow("task_yolox_image", img_res)

    def task_ai(self):
        utils.client_task_start("task_ai")

        ai_req = task_pb2.AIRequesst()
        reply = self.stub.task_ai(ai_req)

        utils.client_task_end("task_ai")
        return reply

    def task_num_detect(self):
        utils.client_task_start("task_num_detect")

        ai_req = task_pb2.AIRequesst()
        reply = self.stub.task_num_detect(ai_req)

        utils.client_task_end("task_num_detect")
        return reply


    def task_yolo5(self):
        utils.client_task_start("task_yolo5")

        file_name = ROOT + 'dataset/001.jpg'
        req = utils.get_file_req(file_name)
        reply = self.stub.task_yolo5(req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)

        utils.client_task_end("task_yolo5")

        if show_result:
            utils.imshow("task_yolo5", img_res)

    def task_style_transfer(self):
        utils.client_task_start("task_style_transfer")

        content_path = ROOT + 'dataset/style-transfer/content.jpg'
        style_path = ROOT + 'dataset/style-transfer/style.jpg'
        content_img = utils.get_file_req(content_path)
        style_img = utils.get_file_req(style_path)
        file_req = task_pb2.File_x2(content=content_img, style=style_img)
        reply = self.stub.task_style_transfer(file_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)

        utils.client_task_end("task_style_transfer")

        if show_result:
            utils.imshow("task_style_transfer", img_res)

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
        utils.client_task_start("task_yolox_vedio")

        vedio_name = ROOT + '/dataset/test2.mp4'
        req_iter = self.get_img_iter(vedio_name)
        reply = self.stub.task_yolox_vedio(req_iter)
        for image in reply:
            str_encode = image.img
            img_res = utils.img_decode(str_encode)
            cv2.imshow('img', img_res)
            cv2.waitKey(1)
        cv2.destroyAllWindows()

        utils.client_task_end("task_yolox_vedio")

    def read_times(self, cap, times):

        for _ in range(times):
            cap.read()
        return cap.read()

    def task_face_ai(self):
        utils.client_task_start("task_face_ai")

        img_path = ROOT + 'dataset/face_ai/ag-3.png'
        img_compose_path = ROOT + 'dataset/face_ai/compose/maozi-1.png'
        img = utils.get_image_req(img_path, '.png').img
        img_compose = utils.get_image_req(img_compose_path, '.png').img
        img_2_req = task_pb2.Image_x2(img=img, img_compose=img_compose)
        reply = self.stub.task_face_ai(img_2_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)

        utils.client_task_end("task_face_ai")

        if show_result:
            utils.imshow("task_face_ai", img_res)

    def task_lic_detect(self):
        utils.client_task_start("task_lic_detect")

        img_path = ROOT + 'dataset/lic/02.jpg'
        img_req = utils.get_image_req(img_path)
        reply = self.stub.task_lic_detect(img_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)

        utils.client_task_end("task_lic_detect")

        if show_result:
            utils.imshow("task_lic_detect", img_res)

    def five_solution(self):
        path = ROOT + 'output/out_time.txt'
        utils.write_time_start(path, arch + ' solution_1', time.time(),'w')
        self.solution(win=[0, 1, 5], mac=[1, 0, 5], smp=[2, 3, 4], hwj=[2, 3], ywd=[4])
        utils.write_time_end(path, arch + ' solution_1', time.time())

        utils.write_time_start(path, arch + ' solution_2', time.time())
        self.solution(win=[2, 3], mac=[], smp=[], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_2', time.time())

        utils.write_time_start(path, arch + ' solution_3', time.time())
        self.solution(win=[1], mac=[], smp=[], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_3', time.time())

        utils.write_time_start(path, arch + ' solution_4', time.time())
        self.solution(win=[0], mac=[], smp=[], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_4', time.time())

        utils.write_time_start(path, arch + ' solution_5', time.time())
        self.solution(win=[4], mac=[], smp=[], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_5', time.time())

    def solution(self, win, mac, smp, hwj, ywd):
        if arch == "win":
            self.do_task(win)
        elif arch == "mac":
            self.do_task(mac)
        elif arch == "smp":
            self.do_task(smp)
        elif arch == "hwj":
            self.do_task(hwj)
        elif arch == "ywd":
            self.do_task(ywd)

    def do_task(self, task_ids):
        for i in task_ids:
            self.task_list[i]()


def start(host, port):
    client = ClientThread("client", host, port, None)
    client.start()
    client.join()


if __name__ == '__main__':
    # start('localhost','50051')
    start('localhost', 50051)

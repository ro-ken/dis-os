from cv2 import cv2

from tools import utils
from tools.utils import ROOT
from tools.settings import *
from tools.proto import task_pb2, task_pb2_grpc


def read_times(cap, times):

    for _ in range(times):
        cap.read()
    return cap.read()


class TaskHandler():

    def __init__(self,stub,client):
        self.stub = stub
        self.client = client

        self.task_list = [self.task_linear_regression,                 # 0
                          self.task_yolox_image,        # 1
                          self.task_yolo5,              # 2
                          self.task_compose,            # 3
                          self.task_lic_detect,         # 4
                          self.task_num_detect,         # 5
                          self.task_monet_transfer,     # 6
                          self.task_style_transfer]     # 7

    def do_task(self, task_ids):
        for i in task_ids:
            self.task_list[i]()

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

        resource = utils.get_resources()
        request = task_pb2.ResourceRequest(addr=self.client.addr, resource=resource)
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

    def task_linear_regression(self):
        utils.client_task_start("task_linear_regression")

        null = task_pb2.Null()
        reply = self.stub.task_linear_regression(null)

        utils.client_task_end("task_linear_regression")
        return reply

    def task_num_detect(self):
        utils.client_task_start("task_num_detect")

        null = task_pb2.Null()
        reply = self.stub.task_num_detect(null)

        utils.client_task_end("task_num_detect")
        return reply


    def task_monet_transfer(self):
        utils.client_task_start("task_monet_transfer")

        null = task_pb2.Null()
        reply = self.stub.task_monet_transfer(null)

        utils.client_task_end("task_monet_transfer")
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
            ret, frame = read_times(cap, 5)
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

    def task_compose(self):
        utils.client_task_start("task_compose")

        img_path = ROOT + 'dataset/face_ai/ag-3.png'
        img_compose_path = ROOT + 'dataset/face_ai/compose/maozi-1.png'
        img = utils.get_image_req(img_path, '.png').img
        img_compose = utils.get_image_req(img_compose_path, '.png').img
        img_2_req = task_pb2.Image_x2(img=img, img_compose=img_compose)
        reply = self.stub.task_compose(img_2_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)

        utils.client_task_end("task_compose")

        if show_result:
            utils.imshow("task_compose", img_res)

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
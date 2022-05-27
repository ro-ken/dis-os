import time

from cv2 import cv2

import settings
from module.proto import task_pb2
from settings import *
from tools import utils
from tools.utils import ROOT
from tools.utils import mytime


# 负责封装任务，并向grpc server请求服务

class TaskHandler:

    def __init__(self, master, stub):
        self.master = master  # client节点
        self.stub = stub  # 代理

        # 任务编号
        self.task_list = [self.task_linear_regression,  # 0
                          self.task_compose,  # 1
                          self.task_num_detect,  # 2
                          self.task_monet_transfer,  # 3
                          self.task_yolox_image,  # 4
                          self.task_yolo5,  # 5
                          self.task_style_transfer]  # 6
        #                 task_face_recognition     # 7

    def do_task_by_ids(self, task_ids):
        for id in task_ids:
            self.do_task_by_id(id)

    def do_task_by_id(self, task_id):
        self.task_list[task_id]()

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

    def task_yolox_image(self, img=None):
        utils.client_task_start("task_yolox_image")

        img_path = ROOT + '/dataset/gather.png'
        img_req = utils.get_image_req(img_path, img=img)
        reply = self.stub.task_yolox_image(img_req)
        str_encode = reply.img
        img_res = utils.img_decode(str_encode)

        utils.client_task_end("task_yolox_image")

        if show_result:
            utils.imshow("task_yolox_image", img_res)
        return img_res

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

    def task_yolox_vedio(self):
        utils.client_task_start("task_yolox_vedio")

        vedio_name = ROOT + '/dataset/test2.mp4'
        req_iter = utils.get_img_iter(vedio_name)
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

    def task_face_recognition(self, frame_tuple, target_list):
        utils.client_task_start("task_face_recognition")

        img, seq = frame_tuple
        str_img = utils.img_encode(img, '.jpg')
        str_names = str(target_list)
        node_name = self.master.node.name
        face_req = task_pb2.FaceRecoRequest(img=str_img, names=str_names, frame_cnt=seq, node_name=node_name)
        reply = self.stub.task_face_recognition(face_req)
        success = reply.success
        img_res = utils.img_decode(reply.img)

        utils.client_task_end("task_face_recognition")

        if show_result:
            utils.imshow("task_face_recognition", img_res)
        return success, img_res

    # 发送心跳包
    def keep_alive(self):
        addr = self.get_node_addr()
        res = utils.get_res()
        name = self.master.node.name
        task_time_list = self.list_add_time(self.master.node.allocated_task_queue)
        tasks = str(task_time_list)
        package = task_pb2.HeartBeat(name=name, addr=addr, res=res, tasks=tasks)
        reply = self.stub.keep_alive(package, timeout=settings.keep_alive_time_out)
        return reply

    # 更新对应节点的任务
    def update_tasks(self, add_task, tasks):
        addr = self.get_node_addr()
        tasks = str(tasks)
        package = task_pb2.TaskPackage(add_task=add_task, tasks=tasks, addr=addr)
        reply = self.stub.update_tasks(package)
        return reply

    def get_node_addr(self):
        ip = self.master.node.server_t.ip
        port = self.master.node.server_t.port
        addr = task_pb2.Address(ip=ip, port=port)
        return addr

    # 给每个任务加上实际运行时间
    def list_add_time(self, queue):
        res = []
        for task in queue:
            res.append([task, 0])  # 初始化

        for node in self.master.node.conn_node_list.values():
            if len(node.run_tasks) != 0 and node.task_start_time != 0:
                task = node.run_tasks[0]  # 正在执行的任务
                cost = mytime() - node.task_start_time  # 获取运行了多久
                cost = round(cost, 2)
                for item in res:
                    if item[0] == task and item[1] == 0:
                        item[1] = cost
                        break

        return res

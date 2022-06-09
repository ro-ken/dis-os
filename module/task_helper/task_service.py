# packge
import time

# app
import settings
from app.app_api import *
from module.proto import task_pb2
from module.proto import task_pb2_grpc

# tool
from tools import utils

# image handle
from cv2 import cv2

# grpc server端实现proto定义的服务
class TaskService(task_pb2_grpc.TaskServiceServicer):
    """ grpc server能够支持的远程服务调用

    主要目的是实现节点间任务数据传输和节点状态同步, 每一类任务都需要不同类型和组合的数据, 
    因此对于每一个特定的任务都要定义不同的远程服务来支持对任务数据的接收和解组

    Attributes:
        node: class Node, 一个节点的抽象, 同时也是grpc server在其上运行的节点
        face_recognizer: 人脸识别器, 目前还不知到用来干啥


    """


    def __init__(self, node):
        """initial class with class Node"""
        self.node = node  
        self.face_recognizer = face_recognition.Face_Recognizer()  


    def task_test(self, request, context):
        """测试grpc server服务是否成功运行"""
        utils.server_task_start("task_test")

        # print("收到请求：", request)
        reply = task_pb2.CommonReply(success=True)

        utils.server_task_end("task_test")
        return reply


    def task_transfer_file(self, request, context):
        """风格迁移文件传输远程服务调用函数"""
        utils.server_task_start("task_transfer_file")

        path = ROOT + request.file_name + '.bak'
        # utils.write_file(path, request.file_data)
        reply = task_pb2.CommonReply(success=True)

        utils.server_task_end("task_transfer_file")
        return reply


    def send_image(self, request, context):
        """yolox图像处理任务远程服务调用函数【早期用来传递图片给yolox, 该函数已不用】"""
        # 任务开始运行提示
        utils.server_task_start("send_image")

        # 图片从字节流解码为能够被应用进行处理的图像数据
        str_encode = request.img
        img = utils.img_decode(str_encode)

        # 调用yolox进行处理图像, 处理完毕后显示图像, 等待用户确认后结束
        img_res = yolo_x.start(img)
        cv2.imshow('img', img_res)
        cv2.waitKey()

        # 任务结束提示
        utils.server_task_end("send_image")
        return task_pb2.CommonReply(success=True)


    def task_yolox_image(self, request, context):
        """yolox图像处理任务远程函数调用服务"""
        utils.server_task_start("task_yolox_image")

        str_encode = request.img
        img = utils.img_decode(str_encode)
        img_res = yolo_x.start(img)
        str_encode = utils.img_encode(img_res, '.jpg')
        reply = task_pb2.Image(img=str_encode)

        utils.server_task_end("task_yolox_image")
        return reply


    def task_yolox_vedio(self, request_iterator, context):
        """yolox视频处理任务远程函数调用服务"""
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
        """yolo5任务远程函数调用服务"""
        utils.server_task_start("task_yolo5")

        in_path = ROOT + 'app/yolo_5/input/' + request.file_name
        utils.write_file(in_path, request.file_data)
        # detect.start(in_path)     # 非windows错误
        yolo_5.start(None)
        out_path = ROOT + 'app/yolo_5/output/' + request.file_name
        img_req = utils.get_image_req(out_path)

        utils.server_task_end("task_yolo5")
        return img_req


    def task_style_transfer(self, request, context):
        """风格迁移任务远程函数调用服务"""
        utils.server_task_start("task_style_transfer")

        content_path = ROOT + 'app/style_transfer/input/' + request.content.file_name
        utils.write_file(content_path, request.content.file_data)
        style_path = ROOT + 'app/style_transfer/input/' + request.style.file_name
        utils.write_file(style_path, request.style.file_data)
        style_transfer.start(content_path, style_path)
        out_path = ROOT + 'app/style_transfer/output/' + 'out.jpg'
        img_req = utils.get_image_req(out_path)

        utils.server_task_end("task_style_transfer")
        return img_req


    def task_linear_regression(self, request, context):
        """线性回归任务远程函数调用服务"""
        utils.server_task_start("task_linear_regression")

        linear_regression.run()

        utils.server_task_end("task_linear_regression")
        return task_pb2.CommonReply(success=True)


    def task_num_detect(self, request, context):
        """数字预测任务远程函数调用服务"""
        utils.server_task_start("task_num_detect")

        num_detect.predict_number()

        utils.server_task_end("task_num_detect")
        return task_pb2.CommonReply(success=True)


    def task_lic_detect(self, request, context):
        """lic-detect任务远程函数调用服务"""
        utils.server_task_start("task_lic_detect")

        str_encode = request.img
        img = utils.img_decode(str_encode)
        img_res = lic_detect.start(img)
        str_encode = utils.img_encode(img_res, '.jpg')
        reply = task_pb2.Image(img=str_encode)

        utils.server_task_end("task_lic_detect")
        return reply


    def task_compose(self, request, context):
        """图像合成任务远程函数调用服务"""
        utils.server_task_start("task_compose")

        str_encode = request.img
        img = utils.img_decode(str_encode)
        str_encode = request.img_compose
        img_compose = utils.img_decode(str_encode)
        img_out = compose.start(img, img_compose)
        str_encode = utils.img_encode(img_out, '.png')
        reply = task_pb2.Image(img=str_encode)

        utils.server_task_end("task_compose")
        return reply


    def task_monet_transfer(self, request, context):
        """"""
        utils.server_task_start("task_monet_transfer")

        monet_transfer.start()

        utils.server_task_end("task_monet_transfer")
        return task_pb2.CommonReply(success=True)


    def task_face_recognition(self, request, context):
        """人脸识别任务远程函数调用服务"""
        utils.server_task_start("task_face_recognition")

        str_encode = request.img
        img = utils.img_decode(str_encode)
        names = eval(request.names)
        frame_cnt = request.frame_cnt
        node_name = request.node_name

        start_time = utils.mytime(point_len=3)

        success, img_out = self.face_recognizer.face_recognition(img, names, frame_cnt)

        end_time = utils.mytime(point_len=3)
        time_slot = end_time - start_time
        path = utils.ROOT + 'output/server_frame_time_{}.txt'.format(node_name)
        # utils.write_time_start(path, 'frame seq = {}'.format(frame_cnt), utils.mytime(point_len=3))     # 记录时间
        # utils.write_time_end(path, 'frame seq = {}'.format(frame_cnt), utils.mytime(point_len=3))       # 记录时间

        utils.write_now_res(path, time_slot, frame_cnt)

        str_encode = utils.img_encode(img_out, '.jpg')
        reply = task_pb2.FaceRecoReply(img=str_encode, success=success)

        utils.server_task_end("task_face_recognition")
        return reply


    def keep_alive(self, request, context):
        """心跳函数, 检测节点是否活跃

        根据心跳频率settings.heart_rate发送心跳包, 检测节点活跃状态并发送节点负载信息

        Attributes:
            request: message HeartBeat{
                        string name = 1;    # 节点名
                        Address addr = 2;   # 节点地址
                        Resource res = 3;   # 节点负载信息
                        string tasks = 4;   # 当前节点待处理任务队列
                    }
        
        Returns:
            CommonReply: message CommonReply{
                            bool success = 1;   # 是否收到心跳包
                        }
        """


        name = request.name
        addr = request.addr
        res = request.res
        tasks = eval(request.tasks)
        key = utils.addr_key(addr)

        # 没有则创建，有则更新
        if key not in self.node.conn_node_list.keys():
            node = self.node.handler.new_node_join(addr.ip, addr.port, name)
        else:
            node = self.node.conn_node_list.get(key)
        node.name, node.res, node.tasks = name, res, tasks
        if settings.show_server_heart_res:
            print("server :get {} heartbeat time={}".format(name, int(time.time()) % 100))

        return task_pb2.CommonReply(success=True)


    def update_tasks(self, request, context):
        """更新节点任务列表

        添加或删除节点上的任务队列中的任务

        Attributes:
            request: message TaskPackage{
                        bool add_task = 1;  # 添加任务为True,删减任务为False
                        string tasks = 2;   # 任务编号, 用','隔开, 例 '1,3,4'
                        Address addr = 3;   # 发送更新请求的节点地址
                    }
        Returns:
            CommonReply: message CommonReply{
                            bool success = 1;   # 是否收到任务更新请求
                        }
        """

        
        addr = request.addr
        key = utils.addr_key(addr)
        node = self.node.conn_node_list.get(key)
        add_task = request.add_task
        tasks = eval(request.tasks)
        if add_task:  # 添加任务
            self.node.allocated_task_queue.extend(tasks)  # 在对应的待执行表添加
            node.run_tasks.extend(tasks)  # 任务发送节点也添加
            node.task_start_time = utils.mytime()  # 开始运行，记录时间
            print("server :add tasks {}".format(tasks))

        else:  # 删除任务
            for task in tasks:
                self.node.allocated_task_queue.remove(task)  # 在对应的待执行表移出
                node.run_tasks.remove(task)  # 任务发送节点也移出
                node.task_start_time = utils.mytime()  # 运行结束，重置时间
                print("server :rm tasks {}".format(task))

        return task_pb2.CommonReply(success=True)

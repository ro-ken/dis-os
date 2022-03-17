

# packge
from cv2 import cv2

# tool
from tools import utils
from tools.settings import arch
from tools.utils import ROOT
from tools.proto import task_pb2, task_pb2_grpc

# model
from model.api import *

# 实现服务
class TaskService(task_pb2_grpc.TaskServiceServicer):

    def __init__(self, node):
        self.node = node

    # 测试grpc server服务是否成功运行
    def task_test(self, request, context):
        utils.server_task_start("task_test")

        # print("收到请求：", request)
        reply = task_pb2.CommonReply(success=True)

        utils.server_task_end("task_test")
        return reply

    '''
    function:   task_transfer_file
    describe:   request方向response方发送request节点上风格迁移应用所需的.bak文件?【该函数已被废弃?】
    input:      
                request         - protobuf 的 message File 类
                    attribute:
                    - string file_name  - 文件名
                    - bytes file_data   - 文件数据
    output:
                protobuf 的 message CommonReply类
    '''
    def task_transfer_file(self, request, context):
        utils.server_task_start("task_transfer_file")

        path = ROOT + request.file_name + '.bak'
        # utils.write_file(path, request.file_data)
        reply = task_pb2.CommonReply(success=True)

        utils.server_task_end("task_transfer_file")
        return reply

    '''
    function:   task_get_res
    describe:   request方向response方发送request节点上的节点资源使用情况(CPU, 内存, 硬盘IO)
    input:      
                request         - protobuf 的 message ResourceRequest 类
                    attribute:
                    - Addr addr             - 节点地址
                    - Resource resource     - 节点资源数据结构
    output:
                protobuf 的 message CommonReply类
    '''
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

    '''
    function:   send_image【yolox应用专用】【兼容性不强啊庆庆】【该函数早期版本没删?】
    describe:   request方向response方发送图片给yolox应用进行处理, 处理完毕后在response方显示处理后的图像
    input:      
                request         - protobuf 的 message Image 类
                    attribute:
                    - bytes img - 图片的字节流
    output:
                protobuf 的 message CommonReply类
    '''
    def send_image(self, request, context):
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

    '''
    function:   task_yolox_image【yolox应用专用】
    describe:   request方向response方发送图片给yolox应用进行处理, 返回处理完毕后的图像给request方
    input:      
                request         - protobuf 的 message Image 类
                    attribute:
                    - bytes img - 图片的字节流
    output:
                protobuf 的 message Image
    '''
    def task_yolox_image(self, request, context):
        utils.server_task_start("task_yolox_image")

        str_encode = request.img
        img = utils.img_decode(str_encode)
        img_res = yolo_x.start(img)
        str_encode = utils.img_encode(img_res, '.jpg')
        reply = task_pb2.Image(img=str_encode)

        utils.server_task_end("task_yolox_image")
        return reply

    '''
    function:   task_yolox_video【yolox应用专用】【处理视频】
    describe:   双向stream, request方向解析视频为image stream, 向response方请求yolox处理, 处理完毕后返回image stream
    input:      
                request_iterator    - protobuf 的 message Image 类的yield迭代器, yield单次迭代返回request
                    attribute:
                     - bytes img - 图片的字节流
    output:
                protobuf 的 message Image steam
    '''
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

    def task_linear_regression(self, request, context):
        utils.server_task_start("task_linear_regression")

        linear_regression.run()

        utils.server_task_end("task_linear_regression")
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

    def task_compose(self, request, context):
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
        utils.server_task_start("task_monet_transfer")

        monet_transfer.start()

        utils.server_task_end("task_monet_transfer")
        return task_pb2.CommonReply(success=True)

    def keep_alive(self, request, context):
        print("server reserve keepalive")
        return task_pb2.CommonReply(success=True)

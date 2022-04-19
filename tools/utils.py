import os
import random
import socket
import time

import numpy as np
from cv2 import cv2
from .io_utils import *
from .random_num import *
from module.proto import task_pb2

ROOT = os.path.split(os.path.realpath(__file__))[0] + '/../'


# 输出提示，表明任务开始调用
def server_task_start(task_name):
    print('--------------{} server start'.format(task_name))



# 输出提示，表明任务结束调用
def server_task_end(task_name):
    print('--------------{} server end'.format(task_name))



def client_task_start(task_name):
    print('--------{} client start'.format(task_name))



def client_task_end(task_name):
    print('--------{} client end'.format(task_name))


def calc_weight(resource):
    cpu = resource.cpu
    mem = resource.mem
    cpu_weight = cpu.logic_num * cpu.use_ratio
    mem_weight = mem.available
    weight = cpu_weight * 0.8 + mem_weight * 0.2
    return weight


def select_max_weight(weights):
    key = None
    max_weight = 0
    for item in weights:
        if weights[item] > max_weight:
            key = item
    return key


def select_by_resource(node_resources):
    weights = {}
    for item in node_resources:
        weight = calc_weight(node_resources[item])
        weights[item] = weight

    key = select_max_weight(weights)
    ip = key.split(':')[0]
    port = key.split(':')[1]

    addr = task_pb2.Address(ip=ip, port=port)
    return addr


def addr_key(addr):
    ip = addr.ip
    port = addr.port
    return gen_node_key(ip, port)


def gen_node_key(ip, port):
    return ip + ":" + str(port)


def img_encode(img, img_type):
    encode = cv2.imencode(img_type, img)[1].tobytes()
    data_encode = np.array(encode)
    str_encode = data_encode.tobytes()
    return str_encode


def img_decode(str_encode):
    nparr = np.frombuffer(str_encode, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def get_image_req(img_path, type='.jpg'):
    img = cv2.imread(img_path)
    str_encode = img_encode(img, type)
    img_req = task_pb2.Image(img=str_encode)
    return img_req


def imshow(title, image):
    cv2.imshow(title, image)
    cv2.waitKey()


def list_to_str(list):
    res = ""

    for i in list:
        res = res + str(i) + ","

    res = res[:-1]  # 删去最后的 ‘,’
    return res


def str_to_list(str):
    str_list = str.split(",")
    res = []
    if str == "":
        return res
    for i in str_list:
        res.append(int(i))
    return res


def get_allocated_tasks(node_list):
    res = {}
    for node in node_list.values():
        res[node.name] = node.tasks

    return res

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

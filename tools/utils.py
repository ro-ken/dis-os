import socket

import numpy as np
from cv2 import cv2
from .io_utils import *
from .random_num import random_list
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


# addr 转 key
def addr_key(addr):
    ip = addr.ip
    port = addr.port
    return gen_node_key(ip, port)


# ip,port 转 key
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


def get_image_req(img_path=None, type='.jpg', img=None):
    if img is None:
        img = cv2.imread(img_path)
    str_encode = img_encode(img, type)
    img_req = task_pb2.Image(img=str_encode)
    return img_req


# 显示图片
def imshow(title, image):
    cv2.imshow(title, image)
    cv2.waitKey()


# 显示视频
def imshow_vedio(title, img_res):
    cv2.imshow(title, img_res)
    cv2.waitKey(1)


def get_img_iter(vedio):
    cap = cv2.VideoCapture(vedio)
    img_width = 360
    img_height = 640
    while True:
        ret, frame = read_times(cap, 5)
        if ret:
            frame = cv2.resize(frame, (img_height, img_width))
            str_encode = img_encode(frame, '.jpg')
            request = task_pb2.Image(img=str_encode)
            yield request
        else:
            break
    cap.release()


def read_times(cap, times):
    for _ in range(times):
        cap.read()
    return cap.read()


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
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


# 把{key:[]}换成{name:[]}
def key_list_name(node_list, res_list):
    name_list = {}
    for key in res_list:
        node = node_list[key]
        name_list[node.name] = res_list[key]

    return name_list

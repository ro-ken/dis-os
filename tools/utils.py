import os

import numpy as np
from cv2 import cv2

from proto import task_pb2, task_pb2_grpc

ROOT = os.path.split(os.path.realpath(__file__))[0] + '/../'


def server_task_start(task_name):
    print('--------------{} server start'.format(task_name))


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

    addr = task_pb2.Addr(ip=ip, port=port)
    return addr


def addr2key(addr):
    return addr.ip + ":" + str(addr.port)


def img_encode(img, img_type):
    encode = cv2.imencode(img_type, img)[1].tobytes()
    data_encode = np.array(encode)
    str_encode = data_encode.tobytes()
    return str_encode


def img_decode(str_encode):
    nparr = np.frombuffer(str_encode, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def get_file_req(file_path) -> object:
    f = open(file_path, 'rb')
    file_data = f.read()
    file_req = task_pb2.File(file_name=get_file_name(file_path), file_data=file_data)
    return file_req


def get_image_req(img_path, type='.jpg'):
    img = cv2.imread(img_path)
    str_encode = img_encode(img, type)
    img_req = task_pb2.Image(img=str_encode)
    return img_req


def get_file_name(path):
    return os.path.split(os.path.realpath(path))[1]


def write_file(path, data):
    f = open(path, 'wb')
    f.write(data)
    f.close()


def imshow(title, image):
    cv2.imshow(title, image)
    cv2.waitKey()

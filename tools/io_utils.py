import os
import time

import psutil

from module.proto import task_pb2


def get_file_name(path):
    return os.path.split(os.path.realpath(path))[1]


def write_file(path, data, type='wb'):
    f = open(path, type)
    f.write(data)
    f.close()


def write_time_start(path, title, time=time.time(),type='a+'):
    data = title + " start time :" + str(time) + '\n'
    write_file(path, data, type)


def write_time_end(path, title, time):
    data = title + " end time :" + str(time) + '\n'
    write_file(path, data, 'a+')

def get_file_req(file_path) -> object:
    f = open(file_path, 'rb')
    file_data = f.read()
    file_req = task_pb2.File(file_name=get_file_name(file_path), file_data=file_data)
    return file_req


def get_resources():
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
    return resource


def save_resource(path,type='a+'):
    resource = get_resources()
    data = str(resource) + '\n'
    write_file(path, data, type)
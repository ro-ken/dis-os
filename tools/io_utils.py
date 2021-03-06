import os
import time
import psutil

from module.proto import task_pb2


def get_file_name(path):
    return os.path.split(os.path.realpath(path))[1]


def write_file(path, data, type='wb'):
    path_dir = os.path.split(path)[0]
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    f = open(path, type)
    f.write(data)
    f.close()


def mytime(int_len=100000, point_len=2):
    return round(time.time() % int_len, point_len)


def write_task_seq(path, seq, task_list, info, type='a+', new_line=False):
    data = "the {} times, {} , {} , time={}\n".format(seq, task_list, info, mytime())
    if new_line:
        data = '\n' + data
    write_file(path, data, type)


def write_time_start(path, title, now, type='a+'):
    data = title + " start time :" + str(now) + '\n'
    write_file(path, data, type)


def write_time_end(path, title, now):
    data = title + " end time :" + str(now) + '\n'
    write_file(path, data, 'a+')


# 写入当前资源
def write_now_res(path, time_slot, seq):
    resource = get_res()
    # cpu = "logic_num = {} ; use_ratio = {}".format(resource.cpu.logic_num, resource.cpu.use_ratio)
    # mem = "total = {} ; available = {}".format(resource.mem.total, resource.mem.available)
    # disc = "total = {} ; available = {}".format(resource.disc.total, resource.disc.available)
    cpu = resource.cpu.use_ratio
    mem = resource.mem.available / resource.mem.total
    disc = resource.disc.available / resource.disc.total
    # data = "cpu :: {} \n mem :: {} \n disc :: {} \n".format(cpu, mem, disc)
    data = "seq:{},cpu:{},mem:{},time:{}\n".format(seq, cpu, mem, time_slot)

    write_file(path, data, 'a+')


def get_file_req(file_path) -> object:
    f = open(file_path, 'rb')
    file_data = f.read()
    file_req = task_pb2.File(file_name=get_file_name(file_path), file_data=file_data)
    return file_req


# 获取本机资源
def get_res():
    cpu = task_pb2.CPU(use_ratio=psutil.cpu_percent(0.1),
                       real_num=psutil.cpu_count(logical=False),
                       logic_num=psutil.cpu_count())
    mem = task_pb2.Memory(total=psutil.virtual_memory().total,
                          available=psutil.virtual_memory().available)
    disc = task_pb2.Disc(total=psutil.disk_usage('/').total,
                         available=psutil.disk_usage('/').free)

    resource = task_pb2.Resource(cpu=cpu, mem=mem, disc=disc)
    return resource


def save_resource(path, type='a+'):
    resource = get_res()
    data = str(resource) + '\n'
    write_file(path, data, type)

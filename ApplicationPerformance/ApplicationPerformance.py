import os
import numpy as np
import cv2
import json

from tools import  task_handler
from tools import task_service
from tools import settings
from tools import utils
from tools.proto import task_pb2
from tools.proto import task_pb2_grpc

import psutil

# 测试结果集
ApplicationPerformanceList = []

# 获取节点资源
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

# 对应不同节点, 使用不同的测试方法
def UnifyPerformance():
    if settings.arch == 'win':
        pass
    if settings.arch == 'mac':
        pass
    if settings.arch == 'raspberry4b':
        pass
    if settings.arch == 'nanob02':
        pass
    if settings.arch == 'mlu220':
        pass
    else:
        print("Error: Please check you tools.settings.arch!")

# 节点 raspberry4b 上的各个应用性能测试
def Raspberry4b():
    # 建立测试结果列表, 存放101次测试结果

    # while循环进行101次测试, 每次传入图像加10(第一次除外, 第一次处理一张图片, 第二次处理10张图片, 第三次处理20张图片, 此后推类)


    # 计算应用平均性能(应用/节点/性能指标)
    pass

# 节点 nanob02 上的各个应用的性能测试
def Nanob02():
    # 建立测试结果列表, 存放101次测试结果

    # while循环进行101次测试, 每次传入图像加10(第一次除外, 第一次处理一张图片, 第二次处理10张图片, 第三次处理20张图片, 此后推类)


    # 计算应用平均性能(应用/节点/性能指标)
    pass

#节点 mlu220 上的各个应用的性能测试
def Mul220():
    # 建立测试结果列表, 存放101次测试结果

    # while循环进行101次测试, 每次传入图像加10(第一次除外, 第一次处理一张图片, 第二次处理10张图片, 第三次处理20张图片, 此后推类)


    # 计算应用平均性能(应用/节点/性能指标)
    pass

# 应用平台检测
def ApplicationIsRun(arch):
    pass

# 性能测试
def PerformanceTest():
    pass

# 计算平均值
def CacAveragePerformance():
    pass
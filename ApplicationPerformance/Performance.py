import os
import numpy as np
import cv2
import json
import time

from model.api import api_yolo_x
from model.api import api_linear_regression
import GetResources

from tools import  task_handler
from tools import task_service
from tools import settings
from tools import utils
from tools.proto import task_pb2
from tools.proto import task_pb2_grpc
import Const

import psutil

class Performance():
    def __init__(self):
        self.task_list = [
            self.task_linear_regression,
            self.task_yolox_image,
            self.task_yolo5,
            self.task_compose,
            self.task_lic_detect,
        ]
    
    # 应用性能测试对外接口
    #   接收任务标号, 执行标号对应的测试函数
    def do_task(self, task_label):
        self.task_list[task_label]()

    # 计算平均资源使用情况
    # 内存以KB为单位
    # 先获取最开始的资源使用情况, 用每一次的测试值减去最开始的值，则为该应用所应用的值, 对这些减数做平均值
    #   内存三元组为(total, free, avilable)
    #    free: LowFree与HighFree的总和，被系统留着未使用的内存,MemFree是说的系统层面
    #    avilavle:应用程序可用内存数。系统中有些内存虽然已被使用但是可以回收的，比如cache/buffer、slab都有一部分可以回收，所以MemFree不能代表全部可用的内存，这部分可回收的内存加上MemFree才是系统可用的内存，即：MemAvailable≈MemFree+Buffers+Cached，它是内核使用特定的算法计算出来的，是一个估计,MemAvailable是说的应用程序层面
    def cac_resource(cpuinfo_list, meminfo_list):
        cpu_start = cpuinfo_list[0]  # 应用开始前的CPU使用率
        cpu_sum = 0
        for cpu_key in cpuinfo_list:
            cpu_sum += cpu_key - cpu_start
        cpu_ave = cpu_sum / len(cpuinfo_list)

        mem_sum = 0
        # 先获取最开始的内存使用情况
        mem_start = meminfo_list[0][0] - meminfo_list[0][1] - meminfo_list[0][2]
        for mem_key in meminfo_list:
            mem_sum += mem_key[0] - mem_key[1]- mem_key[2] - mem_start
        mem_ave = mem_sum / len(meminfo_list)

        return cpu_ave, mem_ave
    
    # 线性回归性能测试
    def task_linear_regression(self):
        cpuinfo_list = []
        meminfo_list = []
        # 开启资源监控线程
        system_info_thread = GetResources.GetSystemInfoThread()
        system_info_thread.start()

        # 监控应用开始运行时间
        start_time = time.time()

        api_linear_regression()

        # 监控应用结束运行时间
        end_time = time.time()

        # 结束资源监控线程
        system_info_thread.stop()

        # 计算应用运行时间
        run_time = end_time - start_time

        # 计算资源平均占用率
        cpuinfo_list = system_info_thread.cpuinfo_list
        meminfo_list = system_info_thread.meminfo_list
        cpu_ave, mem_ave = self.cac_resource(cpuinfo_list, meminfo_list)

        return run_time, cpu_ave, mem_ave


    # yolox性能测试
    #   load为待处理的图片字节流集合
    def task_yolox_image(self, loads):
        # 获取当前资源
        resource_start = self.GetResources()
        results = []

        for img in loads:
            results.append(api_yolo_x(img))
        
        # 获取运行结束后资源
        resource_end = self.GetResources()

        # 返回两次获取的资源
        return resource_start, resource_end
        

    # yolo5性能测试
    def task_yolo5():
        pass

    # 图像合成性能测试
    def task_compose():
        pass

    # 车牌识别性能测试
    def task_lic_detect():
        pass

    # 手写数据集识别性能测试
    def task_num_detect():
        pass

    # 风格迁移性能测试
    def task_monet_transfer():
        pass

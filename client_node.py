import asyncio
import os
import threading
import time
import grpc
import numpy as np
import psutil
from cv2 import cv2
from tools import utils
from tools.utils import ROOT
from tools.settings import *
from tools.proto import task_pb2, task_pb2_grpc
from tools import task_handler

'''
    Class:      ClientThread
    功能：      线程, 封装了客户端调用grpc和应用的函数, 继承threading模块的Thread类
    function:
                __init__    - 初始化线程类的属性
                run         - 封装测试代码, 模拟client调用grpc server方法
                task_test   - 封装应用接口, 调用全部的应用
                five_solution   - 应用性能测试, 测试应用的运行时间, 消耗资源(CPU, 内存)[特定于指定的五种分配方案]
                solution        - 节点环境检测, 根据不同的节点调用不同的应用接口
    attribute: 
                stub            - grpc客户端, 通过这个调用grpc server方法
                task_handler    - 未知
                self.name       - 
                self.port       - grpc server的端口号
                self.addr       - grpc server的ip地址
                self.node       - 当前节点硬件资源特征抽象
'''
class ClientThread(threading.Thread):
    stub = None
    task_handler = None
    # 待处理队列
    task_queue = []

    def __init__(self, name, host, port, addr):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.port = port
        self.addr = addr  # 节点地址


    # 启动client发送任务
    def run(self) -> None:
        with grpc.insecure_channel(self.host + ":" + str(self.port)) as channel:
            stub = task_pb2_grpc.TaskServiceStub(channel)
            self.stub = stub
            self.task_handler = task_handler.TaskHandler(stub,self)
            
            # 依次调用七个应用
            # self.task_test()
            # self.five_solution()
            asyncio.run(self.async_task())

    # 异步协同执行
    async def async_task(self):
        await asyncio.gather(
            self.keep_alive(),
            self.do_task(),
        )

    # 保持连接
    async def keep_alive(self):

        while True:
            request = task_pb2.HeartBeat()
            reply = self.stub.keep_alive(request)
            print(reply)
            # 每秒发送一次
            await asyncio.sleep(1)

    # 应用调用接口封装, 调用全部的7个应用
    async def task_test(self):
        self.task_handler.task_linear_regression()
        self.task_handler.task_yolox_image()
        self.task_handler.task_yolo5()
        self.task_handler.task_compose()
        self.task_handler.task_lic_detect()
        self.task_handler.task_num_detect()
        self.task_handler.task_monet_transfer()
        self.task_handler.task_style_transfer()

    # 应用测试, 测试应用调用时间、消耗资源(CPU、内存), 结果保存在 ./oputput/out_time.txt文件下
    def five_solution(self):
        path = ROOT + 'output/out_time.txt'
        utils.write_time_start(path, arch + ' solution_1', time.time(),'w')
        self.solution(win=[2], mac=[1, 0, 5], smp=[2], hwj=[2, 3], ywd=[4])
        utils.write_time_end(path, arch + ' solution_1', time.time())

        utils.write_time_start(path, arch + ' solution_2', time.time())
        self.solution(win=[2,2], mac=[], smp=[2,2], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_2', time.time())

        utils.write_time_start(path, arch + ' solution_3', time.time())
        self.solution(win=[1,1,2,2,4,4], mac=[], smp=[1,1,2,2,4,4], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_3', time.time())

        utils.write_time_start(path, arch + ' solution_4', time.time())
        self.solution(win=[3,3,4,4], mac=[], smp=[3,3,4,4], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_4', time.time())

        utils.write_time_start(path, arch + ' solution_5', time.time())
        self.solution(win=[2,4,4], mac=[], smp=[2,4,4], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_5', time.time())

    # 节点环境检测, 根据不同的节点调用不同的应用接口
    def solution(self, win, mac, smp, hwj, ywd):
        if arch == "win":
            self.task_handler.do_task_by_ids(win)
        elif arch == "mac":
            self.task_handler.do_task_by_ids(mac)
        elif arch == "smp":
            self.task_handler.do_task_by_ids(smp)
        elif arch == "hwj":
            self.task_handler.do_task_by_ids(hwj)
        elif arch == "ywd":
            self.task_handler.do_task_by_ids(ywd)

    # 处理任务队列里的任务
    async def do_task(self):
        while True:
            if len(self.task_queue) == 0:
                await asyncio.sleep(1)
            else:
                self.task_handler.do_task_by_id(self.task_queue.pop())
            await asyncio.sleep(0.1)

    # 给client添加任务
    def add_tasks(self,task_list):
        self.task_queue.extend(task_list)

# 启动测试代码
def start(host, port):
    client = ClientThread("client", host, port, None)
    client.start()
    client.add_tasks(range(7))
    client.join()
    # client.test()


if __name__ == '__main__':
    # start('localhost','50051')
    start('localhost', 50051)

import asyncio
import time

from module.proto import task_pb2
from module.task_helper import task_handler
from settings import *
from tools import utils
from tools.utils import ROOT


class ClientHandler:

    def __init__(self, master, stub):
        self.master = master  # client节点
        self.stub = stub
        self.task_handler = task_handler.TaskHandler(stub)

    # 异步协同执行
    async def async_task(self):
        await asyncio.gather(
            # self.keep_alive(),
            self.do_task()
        )

    # 保持连接
    async def keep_alive(self):

        while True:
            request = task_pb2.HeartBeat()
            reply = self.stub.keep_alive(request)
            # print(reply)
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

    # 处理任务队列里的任务
    async def do_task(self):
        addr = str(self.master.host) + "_" + str(self.master.port)
        path = ROOT + 'output/' + addr + '_out_time.txt'
        utils.write_time_start(path, arch, addr, 'w')
        while True:
            if len(self.master.task_queue) == 0:
                await asyncio.sleep(1)
            else:
                # print(self.task_queue)
                task_id = self.master.task_queue.pop()
                utils.write_time_start(path, arch + " task id :" + str(task_id), time.time())
                try:
                    self.task_handler.do_task_by_id(task_id)
                except:
                    print("server:{}发生异常!!!".format(addr))
                    self.master.task_queue.append(task_id)
                    self.master.disconnect = True
                    break
                utils.write_time_end(path, arch + " task id :" + str(task_id), time.time())
            await asyncio.sleep(0.1)

    # 给client添加任务
    def add_tasks(self, task_list):
        self.master.task_queue.extend(task_list)

import asyncio
import time

import settings
from module.proto import task_pb2
from module.task_helper import task_handler
from tools.node_settings import *
from tools import utils
from tools.utils import ROOT


class ClientHandler:

    def __init__(self, master, stub):
        self.master = master  # client节点
        self.task_handler = task_handler.TaskHandler(master, stub)

    # 异步协同执行
    async def async_task(self):
        await asyncio.gather(
            self.keep_alive(),
            self.do_task()
        )

    # 保持连接
    async def keep_alive(self):
        await asyncio.sleep(1)  # 等node把表项先创建好
        while not self.master.stop:
            try:
                reply = self.task_handler.keep_alive()
                if settings.show_client_heart_res:
                    print("client heartbeat:send {}:{} time={} ".format(self.master.ip, self.master.port,
                                                                        int(time.time()) % 100))
                # 每秒发送一次
            except:
                print("keep_alive 异常")
                self.disconnection()
                break
            await asyncio.sleep(settings.heart_rate)

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
        name = ip_name[self.master.ip]  # ip到名字的映射
        if settings.env == "lo_exp":
            name = port_name[self.master.port]
        addr = str(self.master.ip) + "_" + str(self.master.port)
        path = ROOT + 'output/' + name + "_" + str(self.master.node.task_seq) + '_task_time.txt'
        utils.write_time_start(path, name, addr, 'w')
        while not self.master.stop:
            if len(self.master.task_queue) == 0:
                await asyncio.sleep(1)
            else:
                # print(self.task_queue)
                task_id = self.master.task_queue.pop(0)
                utils.write_time_start(path, name + " task id :" + str(task_id), time.time())
                try:
                    self.task_handler.do_task_by_id(task_id)
                    self.task_handler.update_tasks(False, [task_id])    # 通知节点删除该任务
                except:
                    self.master.task_queue.append(task_id)
                    self.disconnection()
                    break
                utils.write_time_end(path, name + " task id :" + str(task_id), time.time())
                if len(self.master.task_queue) == 0:
                    utils.write_file(path, 'the task seq {} finish!\n\n'.format(self.master.node.task_seq), 'a+')

            await asyncio.sleep(0.1)    # take a break

    # 给client添加任务
    def add_tasks(self, task_list):
        self.master.task_queue.extend(task_list)

    # 断开连接
    def disconnection(self):
        key = utils.gen_node_key(self.master.ip, self.master.port)
        print("server:{} 连接失败!!!".format(key))
        self.master.node.fail_task_queue.extend(self.master.task_queue)  # 把剩余的任务加入失败任务队列
        self.master.node.conn_node_list.pop(key)  # 从表中移出该节点
        self.master.stop = True
        print("{} client stop".format(key))
        print("当前剩余连接节点：{}".format(list(self.master.node.conn_node_list.keys())))

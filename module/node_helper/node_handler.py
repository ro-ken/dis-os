import asyncio
import time

import server_node
import client_node
from tools import node_settings as settings
from tools.utils import ROOT
from .node_struct import NodeInfo
from tools import utils


class NodeHandler:

    def __init__(self, master):
        self.master = master  # 主节点
        self.queue = master.task_queue  # 节点任务队列

    # 对每个node建立一个client与之连接
    def create_node_table(self):
        time.sleep(0.5)
        for item in self.master.node_list:
            ip, port = item[0], item[1]
            self.create_node_to_table(ip, port)

    # 异步协同执行
    async def async_task(self):
        await asyncio.gather(
            self.gen_task(),  # 生成任务
            self.do_task(),  # 执行任务
            self.do_fail_task()  # 执行失败的任务
        )

    # 通过调度模块方法获取节点地址, 开始进行测试
    async def do_task(self):

        while True:
            if len(self.queue) > 0 and len(self.master.conn_node_list) > 0:  # 有任务，有资源则执行
                print(self.master.conn_node_list.keys(), self.queue)
                self.assign_tasks(self.queue)
            await asyncio.sleep(1)

    async def do_fail_task(self):
        while True:
            await asyncio.sleep(1)
            if len(self.master.fail_task_queue) > 0 and len(self.master.conn_node_list) > 0:
                self.assign_tasks(self.master.fail_task_queue)

    def create_client(self, ip, port):
        client_t = client_node.ClientThread(ip, port, self.master)
        client_t.start()
        time.sleep(0.5)
        return client_t

    def create_node_to_table(self, ip, port):
        key = utils.gen_node_key(ip, port)
        client_t = self.create_client(ip, port)
        # 生成一个表项添加到节点列表
        node = NodeInfo(key, client_t)
        self.master.conn_node_list[key] = node
        return node

    # 动态生成任务
    async def gen_task(self):
        if settings.gen_task is False:
            return  # 不生成任务返回

        await asyncio.sleep(settings.wait_conn_time)  # 等待连接完成

        task_num = 1 if settings.single_task else settings.dynamic_gen_task_num

        while True:
            print("==========times = {} ==========".format(self.master.task_seq))
            self.create_tasks(task_num)
            await asyncio.sleep(settings.dynamic_gen_task_rate)

    # 随机生成任务并添加到队列
    def create_tasks(self, task_num):
        path = ROOT + 'output/task_seq.txt'
        self.master.task_seq += 1
        task_list = utils.random_list(task_num, 0, 5, 3)
        self.queue.extend(task_list)

        if self.master.task_seq == 1:  # 第一次写刷新文件
            utils.write_task_seq(path, self.master.task_seq, task_list, 'w')
        else:
            utils.write_task_seq(path, self.master.task_seq, task_list)

    # 分配任务
    def assign_tasks(self, queue):
        task_res = self.master.scheduler.sched(queue, self.master.conn_node_list)  # 划分任务
        queue.clear()  # 清空队列
        path = ROOT + 'output/task_seq.txt'
        allocated_tasks = utils.get_allocated_tasks(self.master.conn_node_list)
        utils.write_task_seq(path, self.master.task_queue, allocated_tasks)

        for key in task_res.keys():  # 添加到各自的处理队列
            self.master.conn_node_list[key].client.handler.task_handler.update_tasks(True, task_res[key])  # 先通知节点更新任务
            self.master.conn_node_list[key].client.handler.add_tasks(task_res[key])

        utils.write_task_seq(path, self.master.task_seq, task_res)

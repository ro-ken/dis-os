import asyncio
import time

import server_node
import client_node
from tools import node_settings as settings
from .node_struct import NodeInfo
from tools import utils


class NodeHandler:

    def __init__(self, master):
        self.master = master

    # 对每个node建立一个client与之连接
    def create_node_table(self):
        for item in settings.node_list:
            ip, port = item[0], item[1]
            self.create_node_to_table(ip, port)


    # 通过调度模块方法获取节点地址, 开始进行测试
    async def do_task(self):
        # 本机测试
        if settings.env == "dev":
            for node in self.master.conn_node_list.values():
                # 给每个client添加任务
                node.client.handler.add_tasks(range(7))
        else:
            # 联机测试
            # task_list = utils.get_random(15)
            task_list = range(7)
            print(task_list)
            res = self.master.scheduler.divide_tasks(task_list, self.master.node_resources)
            print(res)
            for i in range(3):
                self.master.client_list[i].add_tasks(res[i])


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


    # 异步协同执行
    async def async_task(self):
        await asyncio.gather(
            self.keep_alive(),  # 保持连接
            self.gen_task(),    # 生成任务
            self.do_task()  # 执行任务
        )

    # 检测是否有节点已经断开
    async def keep_alive(self):
        while True:
            for node in self.master.conn_node_list.values():
                client = node.client
                if client.disconnect:
                    res_task = client.task_queue.copy()         # 获取没处理完的任务
                    self.master.conn_node_list.pop(node.key)    # 从表中移出该节点
                    self.master.task_queue.extend(res_task)     # 把剩余的任务加入任务队列

            await asyncio.sleep(1)

    # 动态生成任务
    async def gen_task(self):
        while True:

            await asyncio.sleep(1)



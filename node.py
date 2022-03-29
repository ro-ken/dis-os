import asyncio
import time

import server_node
from module.node_helper import node_handler
from module.sched import sched_api
from tools import node_settings as settings


class Node:

    def __init__(self, port):
        self.server_t = server_node.ServerThread(self, settings.server_ip, port)  # 节点的 server 线程
        self.conn_node_list = {}  # 连接的节点列表
        self.task_queue = []  # 本节点待处理的任务队列
        self.scheduler = sched_api.Scheduler(self)  # 初始化调度器
        self.handler = node_handler.NodeHandler(self)  # 节点的辅助类，一些业务函数在里面

    def start(self):
        self.server_t.start()  # 启动服务器
        self.handler.create_node_table()  # 初始化可连接的节点表
        asyncio.run(self.handler.async_task())  # 执行异步任务

if __name__ == '__main__':
    node = Node(50051)
    node.start()

    time.sleep(60 * 60 * 24)

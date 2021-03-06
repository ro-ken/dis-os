import asyncio
import time

import server_node
from module.node_helper import node_handler
from module.sched import sched_api
from tools import node_settings as settings
from module.node_discovery.dyn_node_server import DynNodeServer
from module.node_helper import vedio_handler

# 分布式系统主启动类
class Node:

    def __init__(self, port):

        # 基础属性
        self.conn_node_list = {}  # 连接的节点列表
        self.task_queue = []  # 本节点待处理的任务队列
        self.frame_queue = []  # 本节点待处理的帧任务队列
        self.fail_task_queue = []  # 执行失败的任务队列
        self.fail_frame_queue = []  # 执行失败的frame队列
        self.allocated_task_queue = []  # 分配给本节点处理的任务队列
        self.name = settings.arch  # 给每个节点起个名字
        self.node_list = settings.node_list  # 所有已知节点集合
        self.task_seq = 0  # 表示第几波任务



        # 视频流
        self.target_list = settings.target_list  # 攻击目标
        self.find_target = False  # 是否发现目标 （视频流处理任务）
        self.target_frame = -1  # 目标帧的序号
        self.recv_queue = []       # 接受到的任务帧序列
        self.next_frame = 0     # 下一帧入队的序号，防止乱序

        # 对象属性
        self.server_t = server_node.ServerThread(self, settings.server_ip, port)  # 节点的 server 线程
        self.dyn_server = DynNodeServer(self,settings.sub_net)  # 节点动态发现的udp server
        self.scheduler = sched_api.Scheduler(self)  # 初始化调度器
        self.handler = node_handler.NodeHandler(self)  # 节点的辅助类，一些业务函数在里面


    # 各个线程启动
    def start(self):
        self.server_t.start()  # 启动服务器
        if settings.node_discovery == "auto" or settings.recv_udp:
            self.dyn_server.StartSocketServer()  # 启动设备发现服务器，监听有无节点加入
        self.handler.join_cluster()  # 将本节点加入集群
        if settings.env == "show":
            vedio_handler.VedioHandlerThread(self).start()  # 开启实时视频显示线程
        self.handler.task_running()     # 执行任务




if __name__ == '__main__':
    node = Node(50051)
    node.start()

    time.sleep(60 * 60 * 24)

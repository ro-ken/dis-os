import asyncio
import time

import cv2

import server_node
import client_node
from tools import node_settings as settings
from tools.utils import ROOT
from .node_struct import NodeInfo
from tools import utils
from ..proto import task_pb2

# 处理节点业务的辅助函数
class NodeHandler:

    def __init__(self, master):
        self.master = master  # 主节点
        self.queue = master.task_queue  # 节点任务队列
        utils.init_output()

    # 任务开始执行
    def task_running(self):
        if settings.task_type == "tasks":
            asyncio.run(self.async_task())  # 执行异步所有任务
        else:
            if settings.sched_type == 'share':
                self.gen_frame_to_queue()
            else:
                asyncio.run(self.async_stream_video())  # 执行异步视频流任务

    # 异步协同执行
    async def async_task(self):
        await asyncio.gather(
            self.gen_task(),  # 生成任务
            self.do_task(),  # 处理任务
            self.do_fail_task()  # 处理失败的任务
        )

    # 异步协同执行处理视频流
    async def async_stream_video(self):
        await asyncio.gather(
            self.gen_frame_task(),  # 生成视频帧并处理
            self.do_fail_stream_task()  # 处理失败帧的任务
        )

    # 通过调度模块方法获取节点地址, 开始进行测试
    async def do_task(self):

        while True:
            if len(self.queue) > 0 and len(self.master.conn_node_list) > 0:  # 有任务，有资源则执行
                print(list(self.master.conn_node_list.keys()), self.queue)
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

    # 新节点加入集群
    def new_node_join(self, ip, port, name):
        node = self.create_node_to_table(ip, port, name)
        key = utils.gen_node_key(ip, port)
        print("新节点接入 addr={},name={}".format(key, name))
        print("当前连接节点：{}".format(self.master.conn_node_list.keys()))
        return node

    # 创建一个节点对象并添加到表里
    def create_node_to_table(self, ip, port, name=''):
        key = utils.gen_node_key(ip, port)
        client_t = self.create_client(ip, port)
        # 生成一个表项添加到节点列表
        node = NodeInfo(key, client_t, name)
        self.master.conn_node_list[key] = node
        return node

    # 动态生成任务
    async def gen_task(self):

        await asyncio.sleep(3)  # 等待连接完成
        # 只生成一批任务
        if settings.gen_task_one_turn:
            self.create_tasks(-1)
            return  # 执行结束返回
        if settings.gen_task is False:
            return  # 不生成任务返回


        task_num = 1 if settings.single_task else settings.dynamic_gen_task_num

        while True:
            print("==========times = {} ==========".format(self.master.task_seq))
            self.create_tasks(task_num)
            await asyncio.sleep(settings.dynamic_gen_task_rate)

    # 随机生成任务并添加到队列
    def create_tasks(self, task_num):
        path = ROOT + 'output/task_seq.txt'
        self.master.task_seq += 1
        if task_num == -1:
            task_list = settings.one_turn_list  # 只生成一次任务
        else:
            task_list = utils.random_list(task_num, 0, 5, 3)
        self.queue.extend(task_list)

        if self.master.task_seq == 1:  # 第一次写刷新文件
            utils.write_task_seq(path, self.master.task_seq, 'new tasks', task_list, type='w')
        else:
            utils.write_task_seq(path, self.master.task_seq, 'new tasks', task_list, new_line=True)

    # 分配任务
    def assign_tasks(self, queue):
        path = ROOT + 'output/task_seq.txt'
        self.write_rest_tasks(path)
        task_res = self.master.scheduler.sched(queue, self.master.conn_node_list)  # 划分任务
        queue.clear()  # 清空队列

        for key in task_res.keys():  # 添加到各自的处理队列
            self.master.conn_node_list[key].client.handler.task_handler.update_tasks(True, task_res[key])  # 先通知节点更新任务
            self.master.conn_node_list[key].client.handler.add_tasks(task_res[key])

        task_res_by_name = utils.key_list_name(self.master.conn_node_list, task_res)  # 结果用name呈现
        utils.write_task_seq(path, self.master.task_seq, 'assign result', task_res_by_name)

    def write_rest_tasks(self, path):
        rest_tasks = utils.get_allocated_tasks(self.master.conn_node_list)
        utils.write_task_seq(path, self.master.task_seq, 'rest tasks', rest_tasks)

    def get_cap(self,src = 1):
        path = ROOT + '/dataset/vedio_30.mp4'
        if src == 0:
            path = 0
        cap = cv2.VideoCapture(path)  # 从摄像头获取视频流
        cap.set(3, 480)  # 640x480
        return cap

    # 处理视频流
    def process_vedio_stream(self,queue):
        while len(queue) > 0 and len(self.master.conn_node_list) > 0:
            node = self.master.scheduler.get_node()     # 获取调度节点
            node.client.frame_queue.append(queue.pop(0))  # 把任务队列的任务分发给对应节点client执行

    # 只产生关键帧到公共队列
    def gen_frame_to_queue(self):
        time.sleep(3)  # 等待连接完成
        cap = self.get_cap()
        total = settings.total_frame_num  # 总共待处理帧的数量
        for i in range(total):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i * 30)    # 每30帧取一帧
            ret, frame = cap.read()
            time.sleep(settings.frame_interval)     # 控制速度
            print(utils.mytime())
            if ret:
                frame_start_time = utils.mytime()     # 获取帧产生的时间
                self.master.frame_queue.append((frame, i, frame_start_time))  # 把帧添加到任务队列里去
                # self.process_vedio_stream(self.master.frame_queue)
            else:
                break
            if self.master.find_target:     # 发现目标，退出
                break
        cap.release()

    # 生成任务帧
    async def gen_frame_task(self):
        await asyncio.sleep(3)  # 等待连接完成
        cap = self.get_cap()
        total = settings.total_frame_num  # 总共待处理帧的数量
        for i in range(total):

            #ret, frame = utils.read_times(cap, settings.key_frame_rate)

            cap.set(cv2.CAP_PROP_POS_FRAMES, i * 30)    # 每30帧取一帧
            ret, frame = cap.read()
            time.sleep(settings.frame_interval)  # 控制速度


            if ret:
                frame_start_time = utils.mytime()     # 获取帧产生的时间
                self.master.frame_queue.append((frame, i, frame_start_time))  # 把帧添加到任务队列里去
                self.process_vedio_stream(self.master.frame_queue)      # 分发下去
            else:
                break
            await asyncio.sleep(0.01)
            if self.master.find_target:     # 发现目标，退出
                break
        cap.release()

    # 把剩余的任务处理掉
    async def do_fail_stream_task(self):
        while True:
            await asyncio.sleep(1)
            self.process_vedio_stream(self.master.frame_queue)
            self.process_vedio_stream(self.master.fail_frame_queue)

    # 将本节点加入集群
    def join_cluster(self):
        if settings.node_discovery == "auto":
            self.master.dyn_server.join_broadcast(self.master.name,settings.sub_net)
        else:
            self.create_node_table()  # 根据配置表连接

    # 对每个node建立一个client与之连接
    def create_node_table(self):
        time.sleep(0.5)
        for item in self.master.node_list:
            ip, port = item[0], item[1]
            name = settings.ip_name[ip]
            self.create_node_to_table(ip, port,name)
            # self.create_node_to_table(ip, port)


    # 自身一个节点处理视频流并实时显示
    def process_vedio_stream_by_self(self):
        time.sleep(1)  # 等待连接完成
        cap = self.get_cap(0)
        while True:
            ret, frame = utils.read_times(cap, 1)
            if ret:
                # frame = cv2.resize(frame, (img_height, img_width))
                str_encode = utils.img_encode(frame, '.jpg')
                request = task_pb2.Image(img=str_encode)
                node = self.master.scheduler.get_node()
                reply = node.client.stub.task_yolox_image(request)
                str_encode = reply.img
                img_res = utils.img_decode(str_encode)
                # 实时显示
                utils.imshow_vedio("vedio_stream", img_res)

            else:
                break
        cap.release()




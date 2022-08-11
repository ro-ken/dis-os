import asyncio
import os
import time

import cv2

from module.task_helper import task_handler
from tools import utils
from tools.utils import mytime
from tools import node_settings as settings
from tools.utils import ROOT
from module.task_helper.task_testy import TaskTesty


# client 线程的辅助类，处理一些业务
class ClientHandler:

    def __init__(self, master, stub):
        self.master = master  # client节点
        self.recv_queue = []
        self.task_handler = task_handler.TaskHandler(master, stub)  # 通过grpc发送任务的辅助类

    def task_running(self):
        time.sleep(5)  # 等node把表项先创建好,多进程情况下等待子进程创建

        if settings.task_type == "tasks":
            asyncio.run(self.async_tasks())
        else:
            asyncio.run(self.async_stream_video())

    # 异步协同执行
    async def async_tasks(self):
        await asyncio.gather(
            self.keep_alive(),
            self.do_task()
        )

    # 异步协同执行
    async def async_stream_video(self):
        await asyncio.gather(
            self.keep_alive(),
            self.process_frame_task(),
            self.frame_to_queue()
        )

    # 做任务测试
    def task_test(self):
        testy = TaskTesty(self.task_handler)
        # testy.do_all_task()
        # self.task_handler.task_yolox_image()
        testy.test_yolox_time()
        # testy.per_task_time()

    # 保持连接
    async def keep_alive(self):

        while not self.master.stop:
            try:
                reply = self.task_handler.keep_alive()
                # print("client heartbeat:send {}:{} time={} ".format(self.master.ip, self.master.port,
                #                                                         int(time.time()) % 100))
            except:
                print("keep_alive 异常")
                self.disconnection()
                break
            await asyncio.sleep(settings.heart_rate)  # 发送频率

    # 处理任务队列里的任务
    async def do_task(self):
        key = utils.gen_node_key(self.master.ip, self.master.port)
        name = self.master.node.conn_node_list[key].name
        addr = str(self.master.ip) + "_" + str(self.master.port)
        path = ROOT + 'output/' + name + "_" + str(self.master.node.task_seq) + '_task_time.txt'
        utils.write_time_start(path, name, addr, 'w')
        while not self.master.stop:
            if len(self.master.task_queue) == 0:
                await asyncio.sleep(1)
            else:
                # print(self.task_queue)
                task_id = self.master.task_queue.pop(0)
                utils.write_time_start(path, name + " task id :" + str(task_id), mytime())
                try:
                    self.task_handler.do_task_by_id(task_id)
                    self.task_handler.update_tasks(False, [task_id])  # 通知节点删除该任务
                except:
                    self.master.task_queue.append(task_id)
                    self.disconnection()
                    break
                utils.write_time_end(path, name + " task id :" + str(task_id), mytime())
                if len(self.master.task_queue) == 0:
                    utils.write_file(path, 'the task seq {} finish!\n\n'.format(self.master.node.task_seq), 'a+')

            await asyncio.sleep(0.1)  # take a break

    # 给client添加任务
    def add_tasks(self, task_list):
        self.master.task_queue.extend(task_list)

    # 断开连接
    def disconnection(self):
        key = utils.gen_node_key(self.master.ip, self.master.port)
        print("server:{} 连接失败!!!".format(key))
        self.master.node.fail_task_queue.extend(self.master.task_queue)  # 把剩余的任务加入失败任务队列
        self.master.node.fail_frame_queue.extend(self.master.frame_queue)  # 把剩余的帧任务加入帧失败任务队列
        self.master.node.conn_node_list.pop(key)  # 从表中移出该节点
        self.master.stop = True
        print("{} client stop".format(key))
        print("当前剩余连接节点：{}".format(list(self.master.node.conn_node_list.keys())))

    # 处理视频帧
    async def process_frame_task(self):
        key = utils.gen_node_key(self.master.ip, self.master.port)
        name = self.master.node.conn_node_list[key].name
        addr = str(self.master.ip) + "_" + str(self.master.port)
        path = ROOT + 'output/' + name + '_frame_task_time.txt'
        frame_res_path = ROOT + 'output/frame_res/'
        utils.write_time_start(path, name, addr, 'w')

        work_queue = self.master.frame_queue        # 调度模式下用client自己的队列作为工作队列
        if settings.sched_type == 'share':          # 共享模式下用node的队列作为工作队列
            work_queue = self.master.node.frame_queue

        while not self.master.stop :

            if len(work_queue) == 0:
                self.master.frame_fin = True
                await asyncio.sleep(0.5)
            else:
                # print(self.task_queue)
                # frame_tuple = work_queue[0]

                frame_tuple = work_queue.popleft()   # 弹出一帧
                self.master.frame_fin = False
                frame, seq, frame_start_time = frame_tuple
                if settings.sched_type == 'share' and settings.real_time:
                    self.master.node.lock.acquire()         # 加一把互斥锁，防止乱序
                    seq = self.master.node.frame_process_seq
                    self.master.node.frame_process_seq += 1
                    self.master.node.lock.release()
                if settings.conn_uav:
                    data = {"seq":seq,"find":False}
                    self.master.node.pipe.send(data)
                print("==========frames seq = {} ==========".format(seq))
                utils.write_time_start(path, name + " before sched frame seq :" + str(seq), frame_start_time)
                utils.write_time_start(path, name + " before send  frame seq :" + str(seq), mytime())
                try:
                    # res = self.task_handler.task_yolox_image(frame)
                    success, res = self.task_handler.task_face_recognition(frame_tuple, self.master.node.target_list)
                    if settings.env == "show":
                        self.recv_queue.append((res,seq))

                    if success:  # 找到目标
                        self.master.node.find_target = True
                        if self.master.node.target_frame == -1:
                            self.master.node.target_frame = seq
                            if settings.conn_uav:
                                data = {"seq": seq, "find": True}
                                self.master.node.pipe.send(data)
                            print("find target!")
                    if self.master.node.find_target:
                        if seq > self.master.node.target_frame:
                            break       # 别的节点发现了目标，直接退出，让最后一张为目标图
                    cv2.imwrite(frame_res_path + str(seq) + '.jpg', res)
                except:
                    work_queue.insert(0,frame_tuple)
                    self.disconnection()
                    break
                utils.write_time_end(path, name + " after send   frame seq :" + str(seq), mytime())
                # work_queue.pop(0)

                if seq == settings.total_frame_num - 1:
                    self.master.frame_fin = True
                    if settings.env == 'exp':       # 做实验过程中，若数据处理完毕，结束进程
                        nodes = self.master.node.conn_node_list.values()
                        while True:
                            is_fin = True       # 是否结束
                            for node in nodes:
                                if not node.client.frame_fin:
                                    is_fin = False
                            if is_fin:          # 处理完毕
                                print('{} 张图片处理完毕'.format(seq + 1))
                                os._exit(0)       # 测完一组数据就自动结束
                            else:
                                await asyncio.sleep(0.5)

            await asyncio.sleep(0.1)  # take a break

    # 把视频帧放入公共队列显示
    async def frame_to_queue(self):
        if settings.env != "show":
            return
        while not self.master.stop or len(self.recv_queue) != 0:
            if len(self.recv_queue) == 0:
                await asyncio.sleep(0.5)
            else:
                item=self.recv_queue.pop(0)
                seq = item[1]
                while seq != self.master.node.next_frame:       # 不是下一帧序号，等待
                    await asyncio.sleep(0.3)

                self.master.node.recv_queue.append(item)
                self.master.node.next_frame += 1






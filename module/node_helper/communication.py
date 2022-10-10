'''
    节点的通信模块，负责连接此系统和小车
'''
import threading
import time

import settings
from tools.node_settings import vehicle_client_port, vehicle_server_port, vehicle_main_ip, vehicle_coop_ip, \
    vehicle_local_ip, frame_size
import socket


class StatusControlBlock:

    def __init__(self, deque):
        self.deque = deque
        self.stage = 0  # 发送的不同阶段
        self.door_pos = None
        self.target_pos = None


class StatusControlBlock2:

    def __init__(self, deque):
        self.deque = deque
        self.mid_x = frame_size[0] / 2  # 图像中心x
        self.mid_y = frame_size[1] / 2  # 图像中心y
        self.last_x = self.mid_x  # 上一次目标的中心x
        self.last_y = self.mid_y  # 上一次目标的中心y
        self.server = UDPServer(vehicle_local_ip, vehicle_server_port)  # 负责接受的服务器
        self.client = UDPClient(self.server, vehicle_main_ip, vehicle_client_port)  # 连接主车客户端

        self.x = 0  # 前后
        self.th = 0  # 转向
        self.speed = 0.2  # 移动速度
        self.turn = 0.5  # 转向速度 rad/s

    # 根据框框的位置判定该往哪儿走
    def follow_target(self, rects):
        target = []
        num = len(rects)
        if num == 0:
            pass  # 没有框处信息
            return
        elif num == 1:
            target = rects[0]
        else:
            target = self.find_target_rect(rects)
        self.last_x = (target[1][0] + target[0][0]) / 2

        # 转向判断
        if self.last_x < self.mid_x * 0.8:
            self.th = 1
            # print("turn left!")
        elif self.last_x > self.mid_x * 1.2:
            self.th = -1
            # print("turn right!")
        else:
            self.th = 0
            # pass
            # print("direction keep!")

        # 前后判断
        span = target[1][0] - target[0][0]
        if span < self.mid_x * 0.5:
            self.x = 1
            # print("go ahead !")
        elif span > self.mid_x:
            self.x = -1
            # print("go back")
        else:
            self.x = 0
            # print("distance keep !!!")
            pass
        print("小车运动，前后:{},左右{}".format(self.x, self.th))

        control_speed = self.x * self.speed
        control_turn = self.th * self.turn

        data = str({"code": 200, "speed": control_speed,"turn": control_turn})
        self.client.send(data)


    # 目标
    def find_target_rect(self, rects):
        assert len(rects) > 1
        gap = self.mid_x * 2  # 寻找和上一个点差值最小的点
        cur_rect = []
        for rect in rects:
            cur_x = (rect[1][0] + rect[0][0]) / 2
            cur_gap = abs(cur_x - self.last_x)
            if cur_gap < gap:
                cur_rect = rect
        self.last_x = (cur_rect[1][0] + cur_rect[0][0]) / 2
        return cur_rect


class UDPClient:
    def __init__(self, server, ip, port):
        self.server = server  # 负责接受的server
        self.ip_port = (ip, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    # 发送消息
    def send(self, msg):
        print("send data", msg)
        self.client.sendto(msg.encode(), self.ip_port)

    # 发送并接受
    def send_recv(self, msg):
        self.send(msg)
        data = self.server.recv()
        return data


class UDPServer:
    def __init__(self, ip, port):
        self.ip_port = (ip, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.server.bind(self.ip_port)

    def recv(self):
        data = self.server.recv(1024).strip().decode()
        print("recv data:", data)
        return data


# 连接小车主程序
def conn_vehicle(node):
    if settings.task_type == "vedio":
        task_target_find(node)
    else:
        task_follow_target(node)


# 目标跟随任务
def task_follow_target(node):
    rect_queue = node.vehicle_deque
    scb = StatusControlBlock2(rect_queue)
    node.start_vedio_process = True  # 通知人脸识别程序启动
    while True:
        cur_len = len(rect_queue)
        if cur_len == 0:
            time.sleep(0.5)
            continue
        elif cur_len == 1:  # 有1张图片信息，识别位置
            data = rect_queue.popleft()
            rects = data["rects"]

        else:  # 有多张图片信息，选择最新的图片获取位置信息
            max = 0
            rects = []
            while len(rect_queue) > 0:
                data = rect_queue.popleft()
                if data["seq"] > max:
                    max = data["seq"]
                    rects = data["rects"]
        # print(data["seq"])
        scb.follow_target(rects)


# 发现打击目标任务
def task_target_find(node):
    scb = StatusControlBlock(node.vehicle_deque)
    server = UDPServer(vehicle_local_ip, vehicle_server_port)  # 负责接受的服务器
    main = UDPClient(server, vehicle_main_ip, vehicle_client_port)  # 连接主车客户端
    coops = []
    for coop_ip in vehicle_coop_ip:
        coop = UDPClient(server, coop_ip, vehicle_client_port)  # 连接从车客户端
        coops.append(coop)

    while True:
        if scb.stage == 0:
            print("stage {}".format(scb.stage))
            data = str({"code": 100, "ip_port": server.ip_port})
            main.send_recv(data)
            for coop in coops:
                coop.send_recv(data)

            scb.stage += 1
            print("client and server init finished! ")
            print("stage {}".format(scb.stage))

        if scb.stage == 1:
            node.start_vedio_process = True  # 通知人脸识别程序启动
            data = str({"code": 0})
            reply = main.send_recv(data)
            data = eval(reply)
            scb.door_pos = data["pos"]  # 获取小车的出口位置

            scb.stage += 1
            print("main vehicle started !")
            print("stage {}".format(scb.stage))


        elif scb.stage == 2:
            if len(scb.deque) > 0:
                data = scb.deque.popleft()
            else:
                time.sleep(0.3)
                continue
            print("scb recv num", data)
            seq = data["seq"]
            if data["find"]:
                data = str({"code": 2, "num": seq})
                reply = main.send_recv(data)  # 告诉小车当前获取图片的序号
                data = eval(reply)
                scb.target_pos = data["pos"]  # 获取小车的出口位置

                scb.stage += 1
                print("target position got!")
                print("stage {}".format(scb.stage))
            else:
                data = str({"code": 1, "num": seq})
                main.send(data)  # 告诉小车当前获取图片的序号

        elif scb.stage == 3:
            data = str({"code": 3, "pos": scb.target_pos})
            for coop in coops:
                coop.send(data)  # 告诉从车目标人物的位置
            for _ in coops:
                server.recv()
            print("coop vehicle already in target position!")
            time.sleep(3)  # 模拟攻击目标等待时间
            scb.stage += 1
            print("stage {}".format(scb.stage))

        elif scb.stage == 4:
            data = str({"code": 5, "pos": scb.door_pos})

            main.send(data)  # 告诉小车当前获取图片的序号
            for coop in coops:
                coop.send(data)  # 告诉小车当前获取图片的序号
            print("发送出入口位置完毕！")
            server.recv()  # 两个车回到初始位置会发送达到消息
            for _ in coops:
                server.recv()  # 依次接受即可
            scb.stage += 1  # 结束了

        else:
            print("所有节点回到出口位置！")
            break

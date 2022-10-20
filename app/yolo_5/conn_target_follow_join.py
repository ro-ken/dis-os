import os
import threading
import time

import cv2
import socket
import yolo_5

'''
要单独运行 目标跟随程序 执行 conn_target_follow

这个文件是打击任务协作的文件，需要和主项目配合使用

'''

vehicle_server_port = 1245  # 此程序的服务器端口
vehicle_client_port = 1240  # 小车server端口
vehicle_main_ip = "192.168.31.148"
vehicle_local_ip = "192.168.31.148"

frame_size = (1920, 1080)


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


class StatusControlBlock:

    def __init__(self):
        self.stop = True       # 线程停止

        self.mid_x = frame_size[0] / 2  # 图像中心x
        self.last_x = self.mid_x  # 上一次目标的中心x
        self.last_w = 0  # 上一次目标的宽度
        self.server = UDPServer(vehicle_local_ip, vehicle_server_port)  # 负责接受的服务器
        self.client = UDPClient(self.server, vehicle_main_ip, vehicle_client_port)  # 连接主车客户端

        self.speed = 0.2  # 移动速度 (m/s)
        self.speed_max = 0.3  # 太快容易撞
        self.back_speed = -0.15  # 后退速度
        self.turn = 0.3  # 转向速度 (rad/s)
        self.t = 0.7  # 两张图片的时间间隔 (s)
        self.half_rad = 0.7  # 半角弧度
        self.base_w = self.mid_x * 0.6  # 基准框宽度 (像素)
        self.bash_y = 1  # 基准距离 (m )

        self.x_l_min = self.mid_x * 0.8  # 向左转向阈值
        self.x_r_min = self.mid_x * 1.2  # 向右转向阈值
        self.x_l_max = self.mid_x * 0.2  # 向左转向阈值
        self.x_r_max = self.mid_x * 1.8  # 向右转向阈值
        self.w_b_min = self.mid_x * 0.8  # 小车后退阈值
        self.w_f_min = self.mid_x * 0.5  # 小车前进阈值

        self.control_speed = 0  # 控制前后速度
        self.control_turn = 0  # 控制转向速度

    # 根据框框的位置判定该往哪儿走
    def follow_target(self, rects):
        target = []
        num = len(rects)

        if num == 0:  # 无框
            self.last_x = self.mid_x  # 上一次目标的中心x
            self.last_w = 0
            self.control_turn = 0
            self.control_speed = 0
        elif num == 1:
            target = rects[0]
        else:
            target = self.find_target_rect(rects)

        if target:
            self.last_x = (target[1][0] + target[0][0]) / 2  # 中心x
            self.last_w = target[1][0] - target[0][0]  # 宽度
            self.tran_turn()
            self.tran_speed()

            print("小车运动，前后:{} m/s,左右{} rad/s".format(self.control_speed, self.control_turn))
        data = str({"code": 200, "speed": self.control_speed, "turn": self.control_turn})
        self.client.send(data)

    # 计算小车转向
    def tran_turn(self):
        if self.x_l_min <= self.last_x <= self.x_r_min:
            # 不转向
            self.control_turn = 0

        elif self.last_x < self.x_l_min:
            # 左转
            turn_rad = self.half_rad * (self.x_l_min - self.last_x) / self.mid_x  # 该转动的弧度
            self.control_turn = turn_rad / self.t
        else:
            # 右转
            turn_rad = self.half_rad * (self.x_r_min - self.last_x) / self.mid_x
            self.control_turn = turn_rad / self.t
        self.control_turn /= 2

    # 计算小车速度
    def tran_speed(self):

        if self.w_f_min <= self.last_w <= self.w_b_min:
            # 不运动
            self.control_speed = 0

        elif self.last_w > self.w_b_min:
            # 小车后退
            self.control_speed = self.back_speed
        else:
            if self.control_speed <= 0.2:
                self.control_speed = 0.2
            # 小车前进
            if self.last_x <= self.x_l_min or self.last_x >= self.x_r_max:
                # 人在边上，可能只识别半个人，速度不能太快
                # self.control_speed = 0.2
                pass
            else:
                distance = self.bash_y * (self.base_w / self.last_w) - self.bash_y  # 该移动的距离
                speed = distance / self.t  # 理应速度
                if speed > self.control_speed:
                    if self.control_speed < self.speed_max:
                        self.control_speed += 0.05  # 匀变速

                else:
                    self.control_speed = speed
                print("--- caculate distance = {} , speed = {}".format(distance, speed))

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


# 目标跟随任务
def task_follow_target(node):
    rect_queue = node.vehicle_deque
    scb = StatusControlBlock()
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
        scb.follow_target(rects)


def write_file(path, data, type='wb'):
    path_dir = os.path.split(path)[0]
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
    f = open(path, type)
    f.write(data)
    f.close()

# 接受状态线程
def recv_status(scb):
    while scb.stop:
        time.sleep(3)
    scb.server.recv()  # 等待主程序发结束信号
    scb.stop = True

if __name__ == '__main__':
    scb = StatusControlBlock()
    threading.Thread(target=recv_status, args=(scb,)).start()  # 控制状态线程
    scb.server.recv()       # 等待主程序发开始信号
    scb.stop = False        # 程序状态变为开始
    cap = cv2.VideoCapture(0)  # 从摄像头获取视频流
    s = time.time()
    while not scb.stop:
        ret, frame = cap.read()
        e = time.time()
        print("delta = {}--------".format(e - s))
        s = e
        in_path = './input/work.jpg'
        cv2.imwrite(in_path, frame)
        rects = yolo_5.start(in_path)
        scb.follow_target(rects)

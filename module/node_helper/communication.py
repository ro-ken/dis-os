'''
    节点的通信模块，负责连接此系统和小车
'''
import threading
import time

from tools.node_settings import vehicle_port, vehicle_main_ip, vehicle_coop_ip, vehicle_local_ip
import socket


class StatusControlBlock:

    def __init__(self, deque):
        self.deque = deque
        self.stage = 0  # 发送的不同阶段
        self.door_pos = None
        self.target_pos = None


class UDPClient:
    def __init__(self,server, ip, port):
        self.server = server    # 负责接受的server
        self.ip_port = (ip, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    # 发送消息
    def send(self, msg):
        print("send data", msg)
        self.client.sendto(msg.encode(), self.ip_port)

    # 发送并接受
    def send_recv(self,msg):
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
    scb = StatusControlBlock(node.vehicle_deque)


    server = UDPServer(vehicle_local_ip, vehicle_port)  # 负责接受的服务器
    main = UDPClient(server,vehicle_main_ip, vehicle_port)  # 连接主车客户端
    coops = []
    for coop_ip in vehicle_coop_ip:
        coop = UDPClient(server,coop_ip, vehicle_port)  # 连接从车客户端
        coops.append(coop)

    while True:
        if scb.stage == 0:
            print("stage {}".format(scb.stage))
            data = str({"code": 100,"ip_port":server.ip_port})
            main.send_recv(data)
            for coop in coops:
                coop.send_recv(data)

            scb.stage += 1
            print("client and server init finished! ")
            print("stage {}".format(scb.stage))


        if scb.stage == 1:
            node.start_vedio_process = True     # 通知人脸识别程序启动
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

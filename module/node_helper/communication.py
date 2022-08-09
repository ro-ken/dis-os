'''
    节点的通信模块，负责连接此系统和小车
'''
import threading
import time

from tools.node_settings import vehicle_port, vehicle_main_ip, vehicle_coop_ip
import socket

class StatusControlBlock:

    def __init__(self,pipe):
        self.pipe = pipe
        self.stage = 0  # 发送的不同阶段
        self.main_ready = False
        self.coop_ready = False
        self.door_pos = None
        self.target_pos = None


# 连接小车主程序
def conn_vehicle(pipe):
    scb = StatusControlBlock(pipe)

    # t1 = threading.Thread(target=main_vehicle_fun, args=(scb,))  # target是要执行的函数名（不是函数），args是函数对应的参数，以元组的形式存在
    # t2 = threading.Thread(target=coop_vehicle_fun, args=(scb,))
    # t1.start()
    # t2.start()

    print("stage {}".format(scb.stage))
    main = socket.socket()  # 创建套接字
    main.connect((vehicle_main_ip,vehicle_port))  # 连接服务器
    coop = socket.socket()  # 创建套接字
    # coop.connect((vehicle_coop_ip,vehicle_port))  # 连接服务器
    scb.stage +=1
    print("stage {}".format(scb.stage))
    while True:
        time.sleep(2)
        if scb.stage == 1 :
            data = {"code":1}
            scb.pipe.send(data)                # 告诉人脸识别该启动了
            data = str({"code":0})
            main.sendall(data.encode())        # 告诉小车该启动了

            reply = main.recv(1024).decode()
            print(reply)
            data = eval(reply)
            scb.door_pos = data["pos"]           # 获取小车的出口位置
            scb.stage += 1

        elif scb.stage == 2:
            data = scb.pipe.recv()
            seq = data["seq"]
            print(data)
            if data["find"]:
                data = str({"code": 2, "num": seq})
                main.sendall(data.encode())  # 告诉小车当前获取图片的序号

                reply = main.recv(1024).decode()
                data = eval(reply)
                print(data)
                scb.target_pos = data["pos"]  # 获取小车的出口位置
                scb.stage += 1

            else:

                data = str({"code":1,"num":seq})
                main.sendall(data.encode())  # 告诉小车当前获取图片的序号

                # reply = main.recv(1024).decode()
                # print(reply)

        elif scb.stage == 3:
            data = str({"code": 3, "pos": scb.target_pos})
            coop.sendall(data.encode())  # 告诉从车目标人物的位置

            reply = coop.recv(1024).decode()
            data = eval(reply)
            # if data["code"] == 3:      # 收到从车到达目标的消息
            scb.stage += 1

        elif scb.stage == 4:
            data = str({"code":5,"pos":scb.door_pos})
            main.sendall(data.encode())  # 告诉小车当前获取图片的序号
            coop.sendall(data.encode())  # 告诉小车当前获取图片的序号

            reply = main.recv(1024).decode()
            reply = coop.recv(1024).decode()
            data = eval(reply)
            scb.stage += 1              # 结束了

        else:
            break

# 主车代码
def main_vehicle_fun(scb):
    ip_port = (vehicle_main_ip, vehicle_port)
    s = socket.socket()  # 创建套接字
    s.connect(ip_port)  # 连接服务器
    scb.main_ready = True

    while True:  # 通过一个死循环不断接收用户输入，并发送给服务器
        if scb.stage == 0 or scb.stage == 3:
            time.sleep(1)

        elif scb.stage == 1:
            data = {"code":1}
            scb.pipe.send(data)    # 告诉无人机该启动了
            data = str({"code":0})
            s.sendall(data.encode())        # 告诉小车该启动了

            reply = s.recv(1024).decode()
            print(reply)
            data = eval(reply)
            scb.door_pos = data["pos"]           # 获取小车的出口位置
            scb.main_ready = True

        elif scb.stage == 2:
            data = scb.pipe.recv()
            seq = data["seq"]
            if data["find"]:
                data = str({"code": 2, "num": seq})
                s.sendall(data.encode())  # 告诉小车当前获取图片的序号

                reply = s.recv(1024).decode()
                data = eval(reply)
                scb.target_pos = data["pos"]  # 获取小车的出口位置
                scb.main_ready = True
            else:
                data = str({"code":1,"num":seq})
                s.sendall(data.encode())  # 告诉小车当前获取图片的序号

        elif scb.stage == 4:
            data = str({"code":5,"pos":scb.door_pos})
            s.sendall(data.encode())  # 告诉小车当前获取图片的序号

            reply = s.recv(1024).decode()
            data = eval(reply)
            scb.main_ready = True

        else:
            break

    s.close()  # 关闭连接


# 从车代码
def coop_vehicle_fun(scb):
    ip_port = (vehicle_coop_ip, vehicle_port)
    s = socket.socket()  # 创建套接字
    s.connect(ip_port)  # 连接服务器
    scb.coop_ready = True

    while True:  # 通过一个死循环不断接收用户输入，并发送给服务器
        if scb.stage == 0 or scb.stage == 1 or scb.stage == 2:
            time.sleep(1)

        elif scb.stage == 3:
            data = str({"code": 3, "pos": scb.target_pos})
            s.sendall(data.encode())  # 告诉小车当前获取图片的序号

            reply = s.recv(1024).decode()
            data = eval(reply)
            # if data["code"] == 3:
            scb.coop_ready = True

        elif scb.stage == 4:
            data = str({"code": 5, "pos": scb.door_pos})
            s.sendall(data.encode())  # 告诉小车当前获取图片的序号

            reply = s.recv(1024).decode()
            data = eval(reply)
            scb.coop_ready = True

        else:
            break
    s.close()  # 关闭连接

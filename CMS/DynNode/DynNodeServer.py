import Const
import socket
import time
import threading

class DynNode():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.encoding = 'utf-8'
        self.server = None
        self.client = None
    
    # 启动socket server
    def StartSocketServer(self):
        pass

    # 修改ip, port
    def ModServerRoute(self):
        pass

    # 发送广播
    def Broadcast(self):
        pass
    
    # 结束socket server
    def KillSocketServer(self):
        pass

# # -*- coding:utf-8 -*-




# from socket import *
# from time import ctime, sleep
# import threading
# class ChatRoomPlus:
#     def __init__(self):
#         # 全局参数配置
#         self.encoding = "utf-8"  # 使用的编码方式
#         self.broadcastPort = 7788   # 广播端口
 
#          # 创建广播接收器
#         self.recvSocket = socket(AF_INET, SOCK_DGRAM)
#         self.recvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#         self.recvSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
#         self.recvSocket.bind(('', self.broadcastPort))
 
#          # 创建广播发送器
#         self.sendSocket = socket(AF_INET, SOCK_DGRAM)
#         self.sendSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
 
#          # 其他
#         self.threads = []
 
#     def send(self):
#         """发送广播"""
 
#         print("UDP发送器启动成功...")
#         self.sendSocket.sendto("***加入了聊天室".encode(self.encoding), ('255.255.255.255', self.broadcastPort))
#         while True:
#             sendData = input("请输入需要发送的消息:")
 
#             self.sendSocket.sendto(sendData.encode(self.encoding), ('255.255.255.255', self.broadcastPort))
#              # print("【%s】%s:%s" % (ctime(), "我", sendData))
 
#             sleep(1)
 
#     def recv(self):
#         """接收广播"""
 
#         print("UDP接收器启动成功...")
#         while True:
#             # 接收数据格式：(data, (ip, port))
#             recvData = self.recvSocket.recvfrom(1024)

#             print("【%s】[%s : %s] : %s" % (ctime(), recvData[1][0], recvData[1][1], recvData[0].decode(self.encoding)))
 
#             sleep(1)
 
#     def start(self):
#         """启动线程"""
#         t1 = threading.Thread(target=self.recv)
#         t2 = threading.Thread(target=self.send)
#         self.threads.append(t1)
#         self.threads.append(t2)
 
#         for t in self.threads:
#             t.setDaemon(True)
#             t.start()
 
#         while True:
#             pass
 

# if __name__ == "__main__":
#      demo = ChatRoomPlus()
#      demo.start()
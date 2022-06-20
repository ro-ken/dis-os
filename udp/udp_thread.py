import socket
import time
import threading

# import other path's pack
import sys
sys.path.append("..")

# type change
from tools.type_change import DictToBytes
from tools.type_change import BytesToDict

class UdpServerThread(threading.Thread):
    def __init__(self, ip, port)
        super(UdpServerThread, self).__init__()
        self.ip = ip
        self.port = port
        self.server = None
        self.encoding = "utf-8"
    
    def create_udp_server(self):
        """建立并初始化一个socket udp服务"""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # 获取socket对象
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # 设置端口重用
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   # 设置socket对象是广播模式
        self.server.bind(('', self.port))                                   # 绑定端口和ip
    
    def message_handle(self, message, addr):
        pass
    
    def message_join(self):
        pass
    
    def message_quit(self):
        pass
    
    def message_heart(slef):
        pass

    def run(self) -> None:
        create_udp_server()
        while True:
            receive_data = self.server.recvfrom(1024)
            message = BytesToDict(receive_data[0])
            addr = receive_data[1]
            self.message_handle(message, addr)

class UdpClientHeartThread(threading.Thread):
    def __init__(self, ip, port)
        super(UdpClientHeartThread, self).__init__()
        self.encoding = "utf-8"
        self.client = None
    
    def get_resource(self):
        pass

    def create_udp_client(self):
        """建立并初始化一个socket udp客户端"""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    def run(self) -> None:
        pass

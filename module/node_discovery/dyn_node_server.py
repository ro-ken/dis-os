from . import Const
import socket
import time
import threading
import json


# socket server线程
# 该线程控制socket UDP server 的启动和结束
class socketserver(threading.Thread):
    """socket udp server 线程

    用来运行 socket udp server 的线程类, 主要用来控制 udp server的启动和终止
    
    Attributes:
        _stop_event: threading.Event(). 线程标志, 为 True 时关闭线程, 终止 UDP server
        server: socket() 创建的 udp server
        master: DynNodeServer. 节点动态管理类
    """

    
    def __init__(self, master, server):
        super(socketserver, self).__init__()
        self._stop_event = threading.Event()
        self.server = server
        self.master = master

    # 字节流转为字典
    def BytesToDict(self, bytesmessage):
        return json.loads(bytesmessage)

    # 设置 _stop_event flag 为 True
    def stop(self):
        self._stop_event.set()

    # 关闭线程, 终止socket UDP server
    def stopped(self):
        return self._stop_event.is_set()

    # 运行 socket UDP server
    def run(self):
        while self.stopped != True:
            ReceiveData = self.server.recvfrom(1024)
            message = self.BytesToDict(ReceiveData[0])
            addr = ReceiveData[1]
            sucess = self.master.InteractionServer(message, addr)


# 动态节点服务类
class DynNodeServer():
    """节点动态管理类
    
    使用socket udp server进行节点的动态加入、退出管理.
    当外部节点想要加入集群时, 发送 UDP 广播请求加入, 退出时同理

    Attributes:
        node: class Node. 专门用于管理节点动态管理而设置的节点类【庆庆你怎么照抄啊, 弄出两个class Node, 之后改改】【@continue】
        ip: string, 节点ip
        port: int, 节点 udp server 端口号
        encoding: 广播消息编码
        server: socket()创建的 udp server
        client: socket()创建的 udp client
    """


    def __init__(self, node):
        self.node = node
        self.ip = Const.SOCKET_UDP_SERVER_IP
        self.port = Const.SOCKET_UDP_SERVER_PORT
        self.encoding = 'utf-8'
        self.server = None
        self.client = None


    def DictToBytes(self, dictmessage):
        """将字典转化为字节流"""
        return json.dumps(dictmessage).encode(self.encoding)


    def BytesToDict(self, bytesmessage):
        """字节流转为字典"""
        return json.loads(bytesmessage)


    # 启动socket server
    def StartSocketServer(self):
        """创建、初始化、启动udp server"""
        # 设置广播模式socket server
        runserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        runserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        runserver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        runserver.bind(('', self.port))

        self.server = socketserver(self, runserver)
        # self.server.setDaemon(True)
        self.server.start()
        # print("Successful: The socket server starting...")


    def StartSocketClient(self):
        """创建、初始化、启动udp client"""
        # 设置广播模式的socket client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


    def Broadcast(self, message, targetport):
        """发送广播消息"""
        if self.client is None:
            self.StartSocketClient()
        bytesmessage = self.DictToBytes(message)
        self.client.sendto(bytesmessage, ('255.255.255.255', targetport))
        return True


    def join_broadcast(self,name):
        """广播节点申请加入集群消息"""
        message = {'type': 'JOIN', 'node_server_ip': self.node.server_t.ip,
                   'node_server_port': self.node.server_t.port, 'name': name}
        self.Broadcast(message,self.port)

    
    def KillSocketServer(self):
        """结束udp server"""
        self.server.stop()
        self.client.close()
        self.server = None
        self.client = None


    def NodeJoinEvent(self, message, addr):
        """节点加入集群处理逻辑"""
        node_ip = message['node_server_ip']
        node_port = message['node_server_port']
        name = message['name']
        self.node.handler.new_node_join(node_ip, node_port, name) # 添加到表里
        return True

    
    def NodeRemoveEvent(self, message, addr):
        """节点退出集群处理逻辑"""
        pass
        return True

    
    def InteractionServer(self, message, addr):
        """udp server处理广播消息"""
        message_type = message['type']
        if message_type == 'JOIN':
            success = self.NodeJoinEvent(message, addr)
            return True
        if message_type == 'REMOVE':
            success = self.NodeRemoveEvent(message, addr)
            return success
        print('【%s】[%s]  Error: unknown message type!' % (time.ctime(), addr[0]))
        return False


    def GenerateMessage(self, type, udp_server_ip, udp_server_port, data):
        """格式化标准消息格式"""
        # 检查传入的数据可靠性
        if isinstance(type, str) != True or isinstance(data, str) != True:
            return None
        if type not in Const.MESSAGE_TYPE:
            return None
        if isinstance(udp_server_ip, str) != True or isinstance(udp_server_port, int) != True:
            return None

        # 构建消息
        message = {}
        message['type'] = type
        message['udp_server_ip'] = udp_server_ip
        message['udp_server_port'] = udp_server_port
        message['data'] = data
        return message

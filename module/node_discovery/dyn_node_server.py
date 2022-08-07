from tools import node_settings as settings
from . import Const
import socket
import time
import threading
import json



# socket server线程
# 该线程控制socket UDP server 的启动和结束
class socketserver(threading.Thread):
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
    def __init__(self, node,sub_net):
        self.node = node
        self.sub_net = sub_net
        self.ip = Const.SOCKET_UDP_SERVER_IP
        self.port = Const.SOCKET_UDP_SERVER_PORT
        self.encoding = 'utf-8'
        self.server = None
        self.client = None

    # 字典转为字节流
    def DictToBytes(self, dictmessage):
        return json.dumps(dictmessage).encode(self.encoding)

    # 字节流转为字典
    def BytesToDict(self, bytesmessage):
        return json.loads(bytesmessage)

    # 启动socket server
    def StartSocketServer(self):
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
        # 设置广播模式的socket client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # 发送广播
    def Broadcast(self, message, targetport):
        if self.client is None:
            self.StartSocketClient()
        bytesmessage = self.DictToBytes(message)
        self.client.sendto(bytesmessage, ('255.255.255.255', targetport))
        return True

    # 广播节点加入
    def join_broadcast(self, name, sub_net):
        message = {'type': 'JOIN', 'node_server_ip': settings.server_ip, 'sub_net': sub_net,
                   'node_server_port': settings.server_port, 'name': name}
        self.Broadcast(message, self.port)

    # 结束socket server
    def KillSocketServer(self):
        self.server.stop()
        self.client.close()
        self.server = None
        self.client = None

    # 节点加入集群处理逻辑
    def NodeJoinEvent(self, message, addr):
        node_ip = message['node_server_ip']
        node_port = message['node_server_port']
        name = message['name']
        sub_net = message['sub_net']
        if self.sub_net == sub_net:     # 网段相同，同意加入
            self.node.handler.new_node_join(node_ip, node_port, name)  # 添加到表里
        # return True

    # 节点退出集群处理逻辑
    def NodeRemoveEvent(self, message, addr):
        pass
        return True

    # socket server处理逻辑
    def InteractionServer(self, message, addr):
        message_type = message['type']
        if message_type == 'JOIN':
            success = self.NodeJoinEvent(message, addr)
            return True
        if message_type == 'REMOVE':
            success = self.NodeRemoveEvent(message, addr)
            return success
        print('【%s】[%s]  Error: unknown message type!' % (time.ctime(), addr[0]))
        return False

    # 传入要传递的内容, 格式化为标准消息格式
    def GenerateMessage(self, type, udp_server_ip, udp_server_port, data):
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

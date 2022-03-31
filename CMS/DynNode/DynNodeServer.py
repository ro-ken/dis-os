from Const import NodeTable
import socket
import time
import threading
import json

# 格式化消息
def GenerateMessage(type, data):
    if  isinstance(type, str) != True or isinstance(data, str) != True:
        return None
    message = {}
    message['type'] = type
    message['data'] = data
    return message

# 节点加入集群
def NodeJoinEvent(data, addr):
    ip = addr[0]
    port = addr[1]
    success, label = NodeTable.NodeJoin(ip, port)
    if success == False:
        print('【%s】[%s]  Error: Reject this node join system, please check your apply!', time.ctime(), ip)
    print('【%s】[%s]  OK: This Node success join system!', time.ctime(), ip)

# 节点退出集群
def NodeRemoveEvent(data, addr):
    ip = addr[0]
    port = addr[1]
    success, label = NodeTable.NodeRemove(ip, port)
    if success == False:
        print('【%s】[%s]  Error: Reject system remove this node, please check your apply!', time.ctime(), ip)
    print('【%s】[%s]  OK: System success remove this node!', time.ctime(), ip)


# socket server处理逻辑
def InteractionServer(message, addr):
    message_type = message['type']
    if message_type == 'JOIN':
        NodeJoinEvent(message['data'],addr)
    if message_type == 'REMOVE':
        NodeRemoveEvent(message['data'],addr)
    print('【%s】[%s]  Error: unknown message type!', time.ctime(), addr[0])
    return False


# socket server线程
class socketserver(threading.Thread):
    def __init__(self, server):
        super(socketserver, self).__init__()
        self._stop_event = threading.Event()
        self.server = server

    # 字节流转为字典
    def BytesToDict(self, bytesmessage):
        return json.loads(bytesmessage)
    
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while self.stopped != True:
            ReceiveData = self.server.recvfrom(1024)
            message = self.BytesToDict(ReceiveData[0])
            addr = ReceiveData[1]
            InteractionServer(message, addr)

# 动态节点服务类
class DynNodeServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
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

        self.server = socketserver(runserver)
        self.server.start()
        print("Successful: The socket server starting...")

    
    def StartSocketClient(self):
        # 设置广播模式的socket client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # 发送广播
    def Broadcast(self, message,targetport):
        if self.client == None:
            print("Error: not run client!")
            return False
        bytesmessage = self.DictToBytes(message)
        self.client.sendto(bytesmessage, ('255.255.255.255', targetport))
        return True

        
    # 结束socket server
    def KillSocketServer(self):
        self.server.stop()
        self.client.close()
        self.server = None
        self.client = None
import Const
import socket
import time
import threading
import json

# 传入要传递的内容, 格式化为标准消息格式
def GenerateMessage(type, data):
    # 检查传入的数据可靠性
    if isinstance(type, str) != True or isinstance(data, str) != True:
        return None
    if type not in Const.MESSAGE_TYPE:
        return None
    
    # 构建消息
    message = {}
    message['type'] = type
    message['data'] = data
    return message

# 节点加入集群处理逻辑
def NodeJoinEvent(data, addr):
    node_ip = addr[0]
    node_port = addr[1]
    success, node_label = Const.NodeTable.NodeJoin(node_ip, node_port)
    if success == False:
        print('【%s】[%s]  Error: Reject this node join system, please check your apply!' % time.ctime(), node_ip)
        return False
    print('【%s】[%s]  OK: This Node success join system, the node label is %d' % time.ctime(), node_ip, node_label)
    print('【%s】[%s]  OK: This new node want to speak : %s' % time.ctime(), node_ip, data)
    return True

# 节点退出集群处理逻辑
def NodeRemoveEvent(data, addr):
    node_ip = addr[0]
    node_port = addr[1]
    success, node_label = Const.NodeTable.NodeRemove(node_ip, node_port)
    if success == False:
        print('【%s】[%s]  Error: Reject system remove this node, please check your apply!' % time.ctime(), node_ip)
        return False
    print('【%s】[%s]  OK: System success remove this node, the node label is %d' % time.ctime(), node_ip, node_label)
    return True


# socket server处理逻辑
def InteractionServer(message, addr):
    message_type = message['type']
    if message_type == 'JOIN':
        success = NodeJoinEvent(message['data'],addr)
        return True
    if message_type == 'REMOVE':
        success = NodeRemoveEvent(message['data'],addr)
        return success
    print('【%s】[%s]  Error: unknown message type!' % time.ctime(), addr[0])
    return False


# socket server线程
# 该线程控制socket UDP server 的启动和结束
class socketserver(threading.Thread):
    def __init__(self, server):
        super(socketserver, self).__init__()
        self._stop_event = threading.Event()
        self.server = server

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
            sucess = InteractionServer(message, addr)

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
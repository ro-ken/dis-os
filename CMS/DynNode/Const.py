import json
import time
import socket

SOCKET_UDP_SERVER_PORT = 10034
__SOCKET_UDP_GET_IP_PORT = 80

MESSAGE_TYPE = ['JOIN', 'REMOVE']

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', __SOCKET_UDP_GET_IP_PORT))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

class Node:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        # 节点列表
        self.NodeTable = {}
        self.NodeTable[0] = str(ip) + ':' + str(port)
        
        # 节点资源抽象表
        self.NodeSourceTable = {}
        self.NodeSourceTable[0] = {}
        print("【%s】[%s:%d] Tip: NodeTable has been created!" % (time.ctime(), self.ip, self.port))

    # 给新加入的节点分配标号
    def __AllocationLabel(self):
        # 获取节点列表
        NodeLabels = self.NodeTable.keys()
        # 集群中无任何节点, 分配标号 0 
        if len(NodeLabels) == 0:
            return 0
        # 集群中存在一个节点且该节点为第一个节点, 分配标号 1
        if len(NodeLabels) == 1 and 0 in NodeLabels:
            return 1
        # 如果不存在退出节点, 即节点表中节点标号皆是递增的, 则分配最大标号+1
        # 如果存在退出节点, 即节点表中节点标号不连续, 则分配最小可分配标号
        maxlabel = max(NodeLabels)
        for label in range(maxlabel + 2):
            if label not in NodeLabels:
                return label

    # 节点加入集群
    def NodeJoin(self, ip, port):
        socketinfo = str(ip) + ':' + str(port)
        if socketinfo not in self.NodeTable.values():
            print('【%s】[%s:%d] OK: The is a new node, then it will join this system!' % (time.ctime(), self.ip, self.port))
            label = self.__AllocationLabel()
            self.NodeTable[label] = socketinfo
            self.NodeSourceTable[label] = {}
            return True, label
        print("【%s】[%s:%d] Error: the node already exist in node table!" % (time.ctime(), self.ip, self.port))
        return False, -1
    
    # 节点退出集群
    def NodeRemove(self, label):
        if label not in self.NodeTable.keys():
            print('【%s】[%s:%d] Error: the node is not in NodeTable' % (time.ctime(), self.ip, self.port))
            return False
        self.NodeTable.pop(label)
        self.NodeSourceTable.pop(label)
        print('【%s】[%s:%d] OK: The node successfully removed %d' % (time.ctime(), self.ip, self.port, label))
        return True, label
    
    # 修改节点资源抽象表
    def NodeModSource(self):
        pass

SOCKET_UDP_SERVER_IP = get_host_ip()

NodeTable = Node(SOCKET_UDP_SERVER_IP, SOCKET_UDP_SERVER_PORT)
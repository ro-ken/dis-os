class Node:
    def __init__(self, ip, port):
        print("Tip: your nodes manager has been created!")
        self.SelfNode = (ip, port)
    
    # 节点列表
    self.NodeTable = {}
    # 节点资源抽象表
    self.NodeSourceTable = {}
    # 节点路由表
    self.NodeRouteTable = {}

    # 增加节点
    def AddNode(self):
        pass
    
    # 删除节点
    def RemoveNode(self):
        pass
    
    # 修改节点路由信息
    def ModNodeRoute(self):
        pass
    
    # 修改节点资源抽象表
    def ModNodeSource(self):
        pass

NodeTalbe = Node()
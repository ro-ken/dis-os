# packge
import threading
from concurrent import futures
import grpc

from tools.node_settings import *
from module.proto import task_pb2_grpc, task_pb2
# tool
from module.task_helper.task_service import TaskService

# model

'''
    Class:      ServerThread
    功能：      线程, 封装grpc的服务器启动代码, 继承threading模块的Thread类, 重写了run方法,
    function:
                __init__    - 初始化线程类的属性
                run         - 封装grpc的服务器启动代码
    attribute: 
                self.name - 
                self.port - grpc server的端口号
                self.addr - grpc server的ip地址
                self.node - 当前节点硬件资源特征抽象
'''


class ServerThread(threading.Thread):
    def __init__(self, node, ip, port):
        threading.Thread.__init__(self)
        self.port = port
        self.ip = ip
        self.node = node
        # self.addr = task_pb2.Addr(ip=self.ip, port=self.port)

    # 开启服务器
    def run(self) -> None:
        # 初始化 grpc server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    # 10个线程池，每个线程池为一个client服务
        service = TaskService(self.node)
        task_pb2_grpc.add_TaskServiceServicer_to_server(service, server)

        # 配置端口
        while True:
            try:
                server.add_insecure_port("[::]:" + str(self.port))
                break
            except:
                # print(str(self.port) + "端口已被占用！")
                self.port += 1
                self.node.name = port_name[self.port]
                self.node.node_list = [[server_ip, 50051]]

        # 运行grpc server
        server.start()
        print("server start... ip = {} , port = {}\n".format(self.ip, str(self.port)))
        server.wait_for_termination()
        print("server 线程结束！！！")


def start(port):
    server_t = ServerThread(None, "localhost", port)
    server_t.start()
    return server_t


if __name__ == '__main__':
    server = start(50051)
    server.join()

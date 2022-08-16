# packge
import threading
from concurrent import futures
import grpc

from tools.node_settings import *
from module.proto import task_pb2_grpc, task_pb2
# tool
from module.task_helper.task_service import TaskService
from module.task_helper.task_service2 import TaskService2

# model

'''
    Class:      ServerThread
    功能：      线程, 封装grpc的服务器启动代码, 继承threading模块的Thread类, 重写了run方法,
'''

def server_process(pipe):
    # 初始化 grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # 10个线程池，每个线程池为一个client服务
    service = TaskService2(pipe)  # grpc实现的服务
    task_pb2_grpc.add_TaskServiceServicer_to_server(service, server)  # 注册进去

    server.add_insecure_port("[::]:50051")

    # 运行grpc server
    server.start()
    pipe.send("ok")     # server启动完毕发送一条消息，client可以发送心跳了
    print("server start... ip = {} , port = 50051\n".format(server_ip))
    server.wait_for_termination()
    print("server 进程结束！！！")



class ServerThread(threading.Thread):
    def __init__(self, node, ip, port):
        threading.Thread.__init__(self)
        self.node = node  # server依附的node
        self.ip = ip  # grpc server的ip
        self.port = port  # grpc server的port

    # 开启服务器
    def run(self) -> None:
        # 初始化 grpc server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # 10个线程池，每个线程池为一个client服务
        service = TaskService(self.node)  # grpc实现的服务
        task_pb2_grpc.add_TaskServiceServicer_to_server(service, server)  # 注册进去

        # 配置端口
        while True:
            try:
                server.add_insecure_port("[::]:" + str(self.port))
                break
            except:
                self.port += 1  # 端口被占用，只有dev模式下才会被占用
                self.node.name = settings.arch + str(self.port % 10)    # 名字依次往下取 win2,win3...
                # self.node.node_list = [[server_ip, 50051]]

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

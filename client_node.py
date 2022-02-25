import os
import threading
import time
import grpc
import numpy as np
import psutil
from cv2 import cv2

from proto import task_pb2,task_pb2_grpc

# client线程
class ClientThread(threading.Thread):
    stub = None

    def __init__(self,name,host,port,addr):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.port = port
        self.addr = addr    # 节点地址

    def send_task(self):
        req = task_pb2.TaskRequest(task_id=1, task_name='task01')
        reply = self.stub.task_service_1(req)
        print(reply)

    def send_file(self,file_name):
        f = open(file_name,'rb')
        file_data = f.read()
        req = task_pb2.FileRequest(file_name = file_name,file_data = file_data)
        reply = self.stub.send_file(req)
        print(reply)

    def send_resource(self):
        cpu = task_pb2.CPU(use_ratio = psutil.cpu_percent(0),
                           real_num = psutil.cpu_count(logical=False),
                           logic_num = psutil.cpu_count())
        mem = task_pb2.Memory(total = psutil.virtual_memory().total,
                              used = psutil.virtual_memory().used,
                              available = psutil.virtual_memory().available)
        disc = task_pb2.Disc(total = psutil.disk_usage('/').total,
                              used = psutil.disk_usage('/').used,
                              available = psutil.disk_usage('/').free)

        resource = task_pb2.Resource(cpu = cpu,mem = mem,disc = disc)
        request = task_pb2.ResourceRequest(addr = self.addr,resource=resource)
        reply = self.stub.send_resource(request)

        print("send_resource.reply:",reply)

    def send_image(self,img_name):
        img = cv2.imread(img_name)
        img_encode = cv2.imencode('.jpg', img)[1]
        data_encode = np.array(img_encode)
        str_encode = data_encode.tobytes()
        request = task_pb2.ImageRequest(img=str_encode)
        reply = self.stub.send_image(request)
        print("send_img.reply:", reply)

    def send_ai(self,data):
        ai_req = task_pb2.AIRequesst()
        reply = self.stub.send_ai(ai_req)
        # ai.run()
        return reply

    # 启动client发送任务
    def run(self) -> None:
        with grpc.insecure_channel(self.host+":"+str(self.port)) as channel:
            stub = task_pb2_grpc.TaskServiceStub(channel)
            self.stub = stub
            # self.send_task()
            # self.send_resource()
            # self.send_file('abc.txt')
            # self.send_image(os.path.split(os.path.realpath(__file__))[0] + '/01.jpg')
            self.send_ai('data.csv')

def start(host,port):
    client = ClientThread("client",host,port,None)
    client.start()
    client.join()

if __name__ == '__main__':
    # start('localhost','50051')
    start('localhost',50051)
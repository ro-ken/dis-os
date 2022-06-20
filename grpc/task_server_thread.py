# grpc
import task_pb2
import task_pb2_grpc
import task_server

# other
import time
import threading


class TaskServerThread(threading.Thread):
    def __init__(self, ip, port):
        super(TaskServerThread, self).__init__()
        self.ip = ip
        self.port = port
    
    def run(self) -> None
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service = task_server.TaskServer()
        task_pb2_grpc.add_TaskServiceServicer_to_server(server, service)
        server.add_insecure_port("[::]:" + str(self.port))

        server.start()
        print("grpc服务已启动, ip: {}, port: {}".format(self.ip, self.port))
        server.wait_for_termination()
        print("grpc服务结束!")


    
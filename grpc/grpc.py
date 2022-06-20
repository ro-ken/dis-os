import task_pb2
import task_pb2_grpc
from task_server_thread improt TaskServerThread

def CreateGrpcClientStub(ip, port):
    """创建并返回grpc客户端
    
    Args:
        ip: grpc服务运行的地址ip
        port: grpc服务运行的地址port

    Returns:
        stub: grpc服务的客户端
    """
    channel = grpc.insecure_channel(ip + ":" + str(port))
    stub = task_pb2_grpc.TaskServiceStub(channel)

    return stub

def CreateGrpcServerStub(ip, port):
    """启动线程运行grpc服务
    
    Args:
        ip: grpc服务运行的地址ip
        port: grpc服务运行的地址port

    Returns: 没有返回, 线程一直运行grpc服务直到程序结束
    """
    grpc_thread = TaskServerThread(ip, port)
    grpc_thread.start()
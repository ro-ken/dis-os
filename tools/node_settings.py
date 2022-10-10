from settings import *
from tools.utils import get_host_ip

node_list = []
server_ip = get_host_ip()
server_port = 50051 # grpc 端口
udp_server_port = 10000  # udp监听端口
vehicle_server_port = 1235       # 小车server端口
vehicle_client_port = 1234       # 小车server端口
vehicle_main_ip = "192.168.0.100"
vehicle_local_ip = "192.168.0.241"
vehicle_coop_ip = ["192.168.0.170","192.168.0.141"]     # 从车ip列表
# vehicle_coop_ip = ["192.168.0.170"]     # 从车ip列表


print_heartbeat = False   # 打印输出实时心跳
heart_rate = 5  # 设置心跳频率（单位/s）
keep_alive_time_out = 6  # 心跳超时时间（单位/s）
frame_size = (640 , 480)


# 以下是手动配置的ip
if node_discovery == "man":
    name_ip = {}
    if nets == "ro_mi":
        name_ip = {
            "win": '192.168.31.204',
            "smp": '192.168.31.117',
            "smp2": '192.168.31.190',
            "smp3": '192.168.31.187',
            "hwj": '192.168.31.112',
            "ywd": '192.168.31.237',
            "vma": "192.168.31.130",
            "rpa": "192.168.31.94",
            "rpb": "192.168.31.25",
            "rpc": "192.168.31.243",
            "rpd": "192.168.31.136"
        }
    elif nets == "tx1":
        name_ip = {
            "win": '192.168.0.241',
            "tx1": '192.168.0.100'
        }

    name_ip["local"] = "127.0.0.1"
    # 想要连接哪个节点就配置哪个节点

    for name in node_names:
        node_list.append([name_ip[name], 50051])

    server_ip = name_ip[arch]

    ip_name = {}    # ip 到name 的映射

    for name in name_ip:
        ip_name[name_ip[name]] = name

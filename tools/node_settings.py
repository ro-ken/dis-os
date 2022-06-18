from settings import *
from tools.utils import get_host_ip

node_list = []
server_ip = get_host_ip()

udp_server_port = 10000  # udp监听端口

# 以下是手动配置的ip
if node_discovery == "man":


    name_ip = {
        "win": '192.168.31.236',
        "smp": '192.168.31.117',
        "ywd": '192.168.31.237',
        "hwj": '192.168.31.112'
    }

    # 想要连接哪个节点就配置哪个节点

    node_list = [
        [name_ip["win"], 50051],
        [name_ip["smp"], 50051]
    ]

    server_ip = name_ip[arch]


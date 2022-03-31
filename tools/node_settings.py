from settings import *

node_list = []
server_ip = "localhost"

name_ip = {
    "win": '192.168.31.236',
    "smp": '192.168.31.117',
    "ywd": '192.168.31.237',
    "hwj": '192.168.31.112'
}

ip_name = {
    "localhost": "local",
    name_ip["win"]: "win",
    name_ip["smp"]: "smp",
    name_ip["ywd"]: "ywd",
    name_ip["hwj"]: "hwj"
}

# 只在开发时用到，不同端口模拟不同节点
name_port = {
    "win": 50051,
    "smp": 50052,
    "ywd": 50053,
    "hwj": 50054
}

port_name = {
    name_port["win"]: "win",
    name_port["smp"]: "smp",
    name_port["ywd"]: "ywd",
    name_port["hwj"]: "hwj"
}


# 配置每个节点所要连接的其他节点列表
if env == "dev":
    node_list = [
        ['localhost', 50051]
    ]
elif env == "exp":
    if arch == "win":       # windows和其他节点连接
        node_list = [
            [name_ip["smp"], 50051]
            , [name_ip["ywd"], 50051]
            , [name_ip["hwj"], 50051]
        ]
    else:
        node_list = [
            [name_ip["win"], 50051]     # 暂时其他节点只和windows连接
        ]
    server_ip = name_ip[arch]
else:
    if arch == "win":
        node_list = [
            [server_ip, 50052]
            , [server_ip, 50053]
            , [server_ip, 50054]
        ]
    else:
        node_list = [
            [server_ip, 50051]  # 暂时其他节点只和windows连接
        ]

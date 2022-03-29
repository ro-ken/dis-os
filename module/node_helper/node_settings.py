from settings import *

node_list = []
server_ip = "localhost"

name_ip = {
    "win": '192.168.31.15',
    "smp": '192.168.31.117',
    "ywd": '192.168.31.236',
    "hwj": '192.168.31.112'
}

if env == "dev":
    node_list = [
        ['localhost', 50051]
    ]
elif env == "exp":
    node_list = [
        [name_ip["smp"], 50051]
        , [name_ip["ywd"], 50051]
        , [name_ip["hwj"], 50051]
    ]
    server_ip = name_ip[arch]
else:
    node_list = [
        [server_ip, 50051]
        , [server_ip, 50052]
        , [server_ip, 50053]
    ]

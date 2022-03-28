from settings import *

node_list = []

if env == "dev":
    node_list = [
        ['localhost', 50051]
    ]
elif env == "exp":
    node_list = [
        ['192.168.31.117', 50051]       # smp
        , ['192.168.31.236', 50051]     # ywd
        , ['192.168.31.112', 50051]     # hwj
        ]
else:
    node_list = [
        ['localhost', 50051]
        , ['localhost', 50052]
        , ['localhost', 50053]
    ]
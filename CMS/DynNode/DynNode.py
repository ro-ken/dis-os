import Const
import DynNodeServer
import time
import threading




# if __name__ == '__main__':
#     server = DynNodeServer.DynNodeServer(Const.SOCKET_UDP_SERVER_IP, Const.SOCKET_UDP_SERVER_PORT)
#     server.StartSocketServer()
#     print("test")
#     server.StartSocketClient()
#     while True:
#         time.sleep(1)
#         print(Const.NodeTable.NodeTable)
#         message = {'type':'JOIN', 'udp_server_ip':Const.SOCKET_UDP_SERVER_IP,'udp_server_port':Const.SOCKET_UDP_SERVER_PORT,'data':'test udp communication'}
#         server.Broadcast(message,7789)
#     server.KillSocketServer()

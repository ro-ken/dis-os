import Const
import DynNodeServer
import threading
ip = '127.0.0.1'
port = 7788

if __name__ == '__main__':
    server = DynNodeServer.DynNodeServer(ip, port)
    server.StartSocketServer()
    print("test")
    # server.StartSocketClient()
    # message = {'type':'commond', 'data':'test udp communication'}
    # server.Broadcast(message,7789)
    # server.KillSocketServer()

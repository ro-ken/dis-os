import os
from time import sleep
import threading
sleep_time = 0.01


# 获取一次cpu的使用情况
def get_cpuinfo():
    raw_cpuinfo = os.popen('cat /proc/stat | grep cpu').readline().split(' ')
    user = int(raw_cpuinfo[2])
    nice = int(raw_cpuinfo[3])
    system = int(raw_cpuinfo[4])
    idle = int(raw_cpuinfo[5])
    cpu = 100 * (user + nice +  system) / (user + nice +  system + idle)
    return cpu

# 获取磁盘使用情况
def get_meminfo():
    raw_meminfo = os.popen('cat /proc/meminfo | grep Mem').readlines()
    total = raw_meminfo[0].split(' ')[8]
    free = raw_meminfo[1].split(' ')[10]
    avilable = raw_meminfo[2].split(' ')[4]
    return (int(total), int(free), int(avilable))

# 获取系统资源使用情况(CPU占用率、内存使用情况)
class GetSystemInfoThread(threading.Thread):
    def __init__(self):
        super(GetSystemInfoThread, self).__init__()
        self._stop_event = threading.Event()
        self.cpuinfo_list = []
        self.meminfo_list = []

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while self.stopped() !=True:
            self.cpuinfo_list.append(get_cpuinfo())
            self.meminfo_list.append(get_meminfo())
            sleep(sleep_time)
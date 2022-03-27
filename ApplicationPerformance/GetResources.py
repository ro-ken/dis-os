import os
import re
from time import sleep
import threading
sleep_time = 0.01

# 正则表达式匹配字符串种的全部数字, 返回一个列表, 列表元素为字符串类型
def num_match(target):
    num_pattern = re.compile(r'\d+')
    return num_pattern.findall(target)


# 获取一次cpu的使用情况
def get_cpuinfo():
    raw_cpuinfo = os.popen('cat /proc/stat | grep cpu').readline()
    cpuinfo_list =  num_match(raw_cpuinfo)
    user = int(cpuinfo_list[0])
    nice = int(cpuinfo_list[1])
    system = int(cpuinfo_list[2])
    idle = int(cpuinfo_list[3])
    cpu = 100 * (user + nice +  system) / (user + nice +  system + idle)
    return cpu

# 获取磁盘使用情况
def get_meminfo():
    raw_meminfo = os.popen('cat /proc/meminfo | grep Mem').readlines()
    total =  num_match(raw_meminfo[0])[0]
    free = num_match(raw_meminfo[1])[0]
    avilable = num_match(raw_meminfo[2])[0]
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

if __name__ == '__main__':
    system_thread = GetSystemInfoThread()
    system_thread.start()
    sleep(1)
    system_thread.stop()
    print(system_thread.cpuinfo_list)
    print(system_thread.meminfo_list)

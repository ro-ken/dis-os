import re
import os


# 正则表达式匹配字符串中的全部数值, 输入为待匹配的字符串(只接受字符串作为输入), 匹配结果以列表形式返回
def num_match_all(target_str):
    if not isinstance(target_str, str):
        return []
    num_pattern = re.compile(r'\d+')
    return num_pattern.findall(target_str)


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

'''
# 通过proc获取CPU使用情况
# 通过proc获取的CPU使用情况每一列参数含义如下: 
    # 1. CPU标识, 用来标识是哪一个CPU, 第一行为所有CPU的总使用情况 
    # 2. user: 从系统启动开始累计到当前时刻, 用户态的CPU时间(单位:jiffies) , 不包含 nice值为负进程。1jiffies=0.01秒
    # 3. nice: 从系统启动开始累计到当前时刻, nice值为负的进程所占用的CPU时间(单位:jiffies)
    # 4. system: 从系统启动开始累计到当前时刻, 核心时间(单位:jiffies)
    # 5. idle: 从系统启动开始累计到当前时刻, 除硬盘IO等待时间以外其它等待时间(单位:jiffies)
    # 6. iowait: 从系统启动开始累计到当前时刻, 硬盘IO等待时间(单位:jiffies) , 
    # 7. irq: 从系统启动开始累计到当前时刻, 硬中断时间(单位:jiffies)
    # 8. softirq: 从系统启动开始累计到当前时刻, 软中断时间(单位:jiffies
# 可以通过简单的计算公式来计算CPU的当前使用率
#       cpu_usage = 100 * (user + nice + system) / (user + nice + system + idle)
'''
def GetCPUUsage():
    # 获取总的CPU使用情况, 而不特别区分每个核的CPU使用情况
    raw_cpuinfo = os.popen('cat /proc/stat | grep cpu').readline()
    match_result = num_match_all(raw_cpuinfo)
    user = int(match_result[0])
    nice = int(match_result[1])
    system = int(match_result[2])
    idle = int(match_result[3])
    cpu = 100 * (user + nice +  system) / (user + nice +  system + idle)
    return cpu


# 获取内存使用情况
def GetMEMUsage():
    pass

# 获取磁盘使用情况
def GetDISKUsage():
    pass

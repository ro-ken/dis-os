from module.sched.sched import IScheduler
from tools import utils
from tools.utils import ROOT
from .utils import *


# 全局贪心 + CPU调度
# 和全局贪心差不多，就是把任务的静态运行时间从静态表改为用拟合后的一次函数计算
class Scheduler(IScheduler):

    # 多任务调度
    def __init__(self, node):
        super().__init__(node)
        self.name_key_dict = {}

    def multi_task_sched(self, task_list, node_list):
        self.name_key_dict = get_node_names(node_list)
        name_time_dict = get_init_time(node_list)
        name_res = self.global_greed(task_list, name_time_dict)
        key_res = name_to_key(name_res, self.name_key_dict)  # 返回字典用地址作为key
        return key_res

    # 全局贪心算法
    def global_greed(self, task_list, name_time_dict):
        res = {}  # 返回结果值
        node_task_time = {}  # 统计花费的时间
        for name in name_time_dict.keys():
            node_task_time[name] = name_time_dict[name]
            res[name] = []

        for task in task_list:
            node = self.select_min_time_node(node_task_time, task)
            res[node].append(task)
            node_task_time[node] += self.get_node_task_time(node, task)  # task_time_table[node][task]
            node_task_time[node] = round(node_task_time[node], 2)  # 保留小数
        print(node_task_time)
        path = ROOT + 'output/task_seq.txt'
        utils.write_task_seq(path, self.node.task_seq, 'node_task_time', node_task_time)
        return res

    # 根据节点CPU换算任务应该运行多久
    def get_node_task_time(self, node_name, task):
        a, b = task_coef_table[node_name][task]  # 取出系数
        node = self.nodes[self.name_key_dict[node_name]]  # 获取节点
        cpu = node.res.cpu.use_ratio  # cpu的利用率   可能超过100%
        x = cpu / node.res.cpu.logic_num  # 归一化处理 ，压缩到（0-100%）
        y = linear_func(a, b, x)  # 任务应该运行的时间
        # print("node={},task={},a={},b={},cpu={},num={},x={},y={}".format(node_name,task,a,b,cpu,node.res.cpu.logic_num,x,y))
        return y

    # 获取当前最小时间的节点 返回最小时间节点的name
    def select_min_time_node(self, node_task_time, task) -> str:
        tmp = node_task_time.copy()
        min_time = 10000000
        min_name = None
        for name in tmp:
            tmp[name] += self.get_node_task_time(name, task)
            if tmp[name] < min_time:
                min_time = tmp[name]
                min_name = name

        return min_name

from module.sched.sched import IScheduler
from tools import utils
from tools.utils import ROOT
from .utils import *

class Scheduler(IScheduler):

    def multi_task_sched(self, task_list, node_list):

        name_key_dict = get_node_names(node_list)
        name_res = self.simple_greed(task_list, name_key_dict.keys())
        key_res = name_to_key(name_res, name_key_dict)  # 返回字典用地址作为key
        return key_res

    # 简单贪心算法
    def simple_greed(self, task_list, name_list):
        res = {}  # 返回结果值
        use_time = {}  # 统计花费的时间
        for name in name_list:
            use_time[name] = 0
            res[name] = []

        for task in task_list:
            node = select_min_time_node(use_time, task)
            res[node].append(task)
            use_time[node] += task_node_table[node][task].time
        print(use_time)
        path = ROOT + 'output/task_seq.txt'
        utils.write_task_seq(path, self.node.task_seq, use_time)
        return res


from module.sched.sched import IScheduler
from tools import utils
from tools.utils import ROOT
from .utils import *


# 全局贪心调度器

class Scheduler(IScheduler):

    # 多任务调度
    def multi_task_sched(self, task_list, node_list):

        name_key_dict = get_node_names(node_list)
        name_time_dict = get_init_time(node_list)
        name_res = self.global_greed(task_list, name_time_dict)
        key_res = name_to_key(name_res, name_key_dict)  # 返回字典用地址作为key
        return key_res

    # 全局贪心算法
    def global_greed(self, task_list, name_time_dict):
        res = {}  # 返回结果值
        node_task_time = {}  # 统计花费的时间
        for name in name_time_dict.keys():
            node_task_time[name] = name_time_dict[name]
            res[name] = []

        for task in task_list:
            node = select_min_time_node(node_task_time, task)
            res[node].append(task)
            node_task_time[node] += task_time_table_fun(node)[task]
            node_task_time[node] = round(node_task_time[node], 2)  # 保留小数
        print(node_task_time)
        path = ROOT + 'output/task_seq.txt'
        utils.write_task_seq(path, self.node.task_seq, 'node_task_time', node_task_time)
        return res

from module.sched.sched import IScheduler
from tools import utils
from tools.utils import ROOT
from .utils import *


# 简单贪心调度器
class Scheduler(IScheduler):

    def get_node(self):
        task = 8   # 8号任务为人脸识别
        name_key_dict = get_node_names(self.nodes)   # 先知道有哪些结点，把名字取出来
        node_task_time = get_node_task_time(self.nodes,task)        # 获取当前节点运行任务所需时间
        print(node_task_time)
        node_name = select_min_time_node(node_task_time, task)         # 选择一个节点，

        return self.nodes[name_key_dict[node_name]]     # 返回node对象

    def multi_task_sched(self, task_list, node_list):

        name_key_dict = get_node_names(node_list)       # 先知道有哪些结点，把名字取出来
        name_res = self.simple_greed(task_list, name_key_dict.keys())
        key_res = name_to_key(name_res, name_key_dict)  # 返回字典用地址作为key
        return key_res

    # 简单贪心算法
    def simple_greed(self, task_list, name_list):
        res = {}  # 返回结果值
        node_task_time = {}  # 统计花费的时间
        for name in name_list:
            node_task_time[name] = 0
            res[name] = []

        for task in task_list:
            node = select_min_time_node(node_task_time, task)
            res[node].append(task)
            node_task_time[node] += task_time_table_fun(node)[task]
        print(node_task_time)
        path = ROOT + 'output/task_seq.txt'
        utils.write_task_seq(path, self.node.task_seq, 'node_task_time', node_task_time)
        return res

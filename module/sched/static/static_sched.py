from module.sched.sched import IScheduler
from .static_tbl import task_node_table
from tools import node_settings


def select_min_time_node(use_time, task) -> str:

    tmp = use_time.copy()
    min_time = 10000000
    min_name = None
    for name in tmp:
        tmp[name] += task_node_table[name][task].time
        if tmp[name] < min_time:
            min_time = tmp[name]
            min_name = name

    return min_name


def get_node_names(node_list):
    name_key_dict = {}
    for key in node_list:
        name = node_list[key].name
        name_key_dict[name]=key
    return name_key_dict


def name_to_key(name_res, name_key_dict):
    key_res = {}
    for name in name_key_dict:
        key_res[name_key_dict[name]] = name_res[name]
    return key_res


class Scheduler(IScheduler):

    def divide_tasks(self, task_list,node_list):

        name_key_dict = get_node_names(node_list)
        name_res = self.simple_greed(task_list,name_key_dict.keys())
        key_res = name_to_key(name_res,name_key_dict)     # 返回字典用地址作为key
        return key_res

        # 选择最小时间的节点

    # 简单贪心算法
    def simple_greed(self, task_list,name_list):
        res = {}  # 返回结果值
        use_time = {}       # 统计花费的时间
        for name in name_list:
            use_time[name] = 0
            res[name]=[]

        for task in task_list:
            node = select_min_time_node(use_time, task)
            res[node].append(task)
            use_time[node] += task_node_table[node][task].time
        print(use_time)
        return res

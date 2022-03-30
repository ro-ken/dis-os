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
    name_list = []
    for key in node_list:
        # ip = key.split(":")[0]
        # name = node_settings.ip_name[ip]
        name = node_list[key].name
        name_list.append(name)
    return name_list


class Scheduler(IScheduler):

    def divide_tasks(self, task_list,node_list):

        name_list = get_node_names(node_list)
        res = self.simple_greed(task_list,name_list)
        return res

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

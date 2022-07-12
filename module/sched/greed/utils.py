from .static_tbl import task_time_table_fun
from .static_tbl import task_coef_table_fun
from .static_tbl import node_trans_delay_table_fun

# 获取当前最小时间的节点 返回最小时间节点的name
def select_min_time_node(node_task_time, task) -> str:
    tmp = node_task_time.copy()
    min_time = 10000000
    min_name = None
    for name in tmp:
        tmp[name] += task_time_table_fun(name)[task]
        if tmp[name] < min_time:
            min_time = tmp[name]
            min_name = name

    return min_name


# 获取节点name到key的dict 返回 {name1:key1,name2:key2...}
def get_node_names(node_list):
    name_key_dict = {}
    for key in node_list:
        name = node_list[key].name
        name_key_dict[name] = key
    return name_key_dict


# 获取节点的任务所需时间，针对 vedio_stream 任务 运行yolox模型 任务编号：1
def get_node_task_time(node_list, task):
    node_task_time = {}  # 统计花费的时间
    for node in node_list.values():
        client = node.client  # 结点待运行的任务存与client的frame_queue中
        task_num = len(client.frame_queue)  # 获取剩余帧数
        single_task_time = task_time_table_fun(node.name)[task]  # 获取单任务运行时间
        node_task_time[node.name] = task_num * single_task_time  # 计算时间
    return node_task_time


# 获取dict的name转为key 返回 {key1：res1,key2：res2...}
def name_to_key(name_res, name_key_dict):
    key_res = {}
    for name in name_key_dict:
        key_res[name_key_dict[name]] = name_res[name]
    return key_res


def get_init_time(node_list):
    name_time_list = {}
    for key in node_list:
        name = node_list[key].name
        task_list = node_list[key].tasks
        t_time = 0
        for item in task_list:
            task, cost = item[0], item[1]  # 取出任务号 和 实际运行时间
            static_time = task_time_table_fun(name)[task]
            cost = min(static_time, cost)  # 如果实际运行实际比预计还长，那么时间算0，不能出现负数
            t_time += static_time - cost  # 贪心时间加上去
        name_time_list[name] = t_time
    return name_time_list

# 一次函数
def regression(coef, x):
    y = -1
    if len(coef) == 2:
        y = coef[0] * x + coef[1]

    elif len(coef) == 3:
        y = coef[0] * x ** 2 + coef[1] * x + coef[2]

    elif len(coef) == 4:
        y = coef[0] * x ** 3 + coef[1] * x ** 2 + coef[2] * x + coef[3]

    elif len(coef) == 5:
        y = coef[0] * x ** 4 + coef[1] * x ** 3 + coef[2] * x ** 2 + coef[3] * x + coef[4]
    return y

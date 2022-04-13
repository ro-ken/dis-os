from .static_tbl import task_node_table


# 获取当前最小时间的节点 返回最小时间节点的name
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


# 获取节点name到key的dict 返回 {name1:key1,name2:key2...}
def get_node_names(node_list):
    name_key_dict = {}
    for key in node_list:
        name = node_list[key].name
        name_key_dict[name] = key
    return name_key_dict


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
        for task in task_list:
            t_time += task_node_table[name][task].time
        name_time_list[name] = t_time
    return name_time_list

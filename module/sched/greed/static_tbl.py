import settings

# 任务序号 0,1,2...

task_time_smp = (2.53, 0.46, 0.01, 41.54, 7.75, 15.63, 1000000)
task_time_ywd = (2.53, 0.43, 0.07, 33.17, 6.65, 1000000, 1000000)
task_time_hwj = (0.95, 0.27, 0.03, 25.47, 4.88, 10.48, 1000000)
task_time_win = (0.33, 0.23, 0.01, 3.45, 1.34, 2.20, 2.95)

# 静态时间表
task_time_table = {"smp": task_time_smp, "ywd": task_time_ywd, "hwj": task_time_hwj, "win": task_time_win,
                   "vma": task_time_smp, "loc": task_time_smp}

# 任务运行时间随CPU负载变化的系数 y=ax+b 系数(a,b)
vedio_coef_hwj = (-1.7288 * 10 ** (-8), 3.3566 * 10 ** (-6), -1.5542 * 10 ** (-4), 0.0069, 0.710699)
vedio_coef_smp = (-5.47786 * 10 ** (-8), 1.39251 * 10 ** (-5), -8.32595 * 10 ** (-4), 0.01802, 1.84984)
vedio_coef_smp2 = (-2.81663 * 10 ** (-8), 7.41518 * 10 ** (-6), -3.76554 * 10 ** (-4), 0.01008, 1.89676)
vedio_coef_smp3 = (-3.69075 * 10 ** (-8), 9.72546 * 10 ** (-6), -5.38190 * 10 ** (-4), 0.01246, 1.88844)

# 0-5 为一般任务，6号为视频流任务
coef_smp = (
    (0.018, 2.147), (0.001, 0.237), (0.003, -0.004), (0.354, 41.186), (0.106, 6.113), (0.275, 13.368), vedio_coef_smp)
# 0-5 为一般任务，6号为视频流任务
coef_smp2 = (
    (0.018, 2.147), (0.001, 0.237), (0.003, -0.004), (0.354, 41.186), (0.106, 6.113), (0.275, 13.368), vedio_coef_smp2)
# 0-5 为一般任务，6号为视频流任务
coef_smp3 = (
    (0.018, 2.147), (0.001, 0.237), (0.003, -0.004), (0.354, 41.186), (0.106, 6.113), (0.275, 13.368), vedio_coef_smp3)
coef_hwj = (
    (0.008, 1.29), (0.001, 0.647), (3.333, 0.535), (0.235, 25.919), (0.042, 5.064), (0.103, 11.544), vedio_coef_hwj)

# 比例系数表
task_coef_table = {"smp": coef_smp, "hwj": coef_hwj, "win": coef_hwj, "smp2": coef_smp2, "smp3": coef_smp3,
                   "vma": coef_smp, "loc": coef_smp, "vma2": coef_smp, "vma3": coef_smp, "vma4": coef_smp,
                   "vma5": coef_smp, "vma6": coef_smp}

'''
    以下为传输时延
'''
# 默认延迟
default_self_delay = 0.5
default_diff_node_delay = 1.0

# 本节点测量延迟
node_self_trans_delay = {"smp": 0, "hwj": 0, "win": 0, "smp2": 0, "smp3": 0,
                         "vma": 0, "local": 0, "vma2": 0, "vma3": 0, "vma4": 0, "vma5": 0, "vma6": 0}

# 未测量延迟
unscanned_delay = {"smp": 0, "hwj": 0, "win": 0, "smp2": 0, "smp3": 0,
                   "vma": 0, "local": 0, "vma2": 0, "vma3": 0, "vma4": 0, "vma5": 0, "vma6": 0, }

diff_node_delay_table = {"smp": unscanned_delay, "hwj": unscanned_delay, "win": unscanned_delay,
                         "smp2": unscanned_delay, "smp3": unscanned_delay,
                         "vma": unscanned_delay, "local": unscanned_delay, "vma2": unscanned_delay,
                         "vma3": unscanned_delay, "vma4": unscanned_delay, "vma5": unscanned_delay,
                         "vma6": unscanned_delay}

'''
    以下为向上层暴露的api函数
'''


# 返回多任务处理时间表
def task_time_table_fun(name):
    arch = name[:3]  # 取前3个作为key：例 name = smp2 ，arch = smp
    return task_time_table[arch]


# 返回任务处理时间系数表
def task_coef_table_fun(name):
    arch = name[:3]  # 取前3个作为key：例 name = smp2 ，arch = smp
    if arch == 'smp':  #
        return task_coef_table[name]
    else:
        return task_coef_table[arch]


# 返回传输时延
def node_trans_delay_table_fun(name):
    # 本节点时延
    if name == settings.arch:
        if settings.self_delay_time > 0:
            return settings.self_delay_time
        elif node_self_trans_delay[name] > 0:
            return node_self_trans_delay[name]
        else:
            return default_self_delay
    # 其他节点时延
    else:
        if settings.diff_node_delay_time > 0:
            return settings.diff_node_delay_time
        elif diff_node_delay_table[settings.arch][name] > 0:
            return diff_node_delay_table[settings.arch][name]
        else:
            return default_diff_node_delay

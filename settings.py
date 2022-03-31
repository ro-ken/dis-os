
arch = "win"   # 本机架构：win , mac , smp , hwj , ywd

env = "lo_exp"  # 环境：”dev“本机开发，”exp“，联机实验，”lo_exp“,本地实验

sched_type = "static"   # 调度类型："static" 根据静态表调度，"dynamic"根据实时获取资源进行动态调度

heart_rate = 2  # 设置心跳频率（单位/s）

show_result = False  # 是否输出结果
show_server_heart_res = True  # 实时显示server心跳结果
show_client_heart_res = True  # 实时显示client心跳结果
if arch == "win":
    show_server_heart_res = False

init_task_num = 10      # 初始任务数量
dynamic_gen_task = True    # 是否动态生成任务
dynamic_gen_task_rate = 8   # 动态生成任务的频率 （单位/s）
dynamic_gen_task_num = 5   # 每次动态生成任务数量

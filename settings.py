arch = "win"  # 本机架构：win , mac , hwj , ywd , smp , smp2 , smp3 , ...

env = "exp"  # 环境：”dev“本机开发，”exp“，联机实验

p2p = True  # 是否是对等模式
sched_type = "loop"  # 调度类型：simple_greed , global_greed , cpu_res , loop

node_discovery = "auto"     # man：手动配置节点ip ， auto：自动发现

heart_rate = 2  # 设置心跳频率（单位/s）
keep_alive_time_out = 2  # 心跳超时时间（单位/s）

show_result = False  # 是否输出结果
show_vedio_stream = True # 显示vedio结果
show_server_heart_res = True  # 实时显示server心跳结果
show_client_heart_res = True  # 实时显示client心跳结果

gen_task = False  # 本节点是否生成任务，若为False，后面配置无效
wait_conn_time = 5  # 第一次任务分配时间
dynamic_gen_task_rate = 15  # 动态生成任务的频率 （单位/s）
single_task = False  # 每次生成单个任务,若为True，后面配置无效
dynamic_gen_task_num = 8  # 每次动态生成任务数量

import sys
arch = "local"  # 本机架构：win , mac , hwj （寒武纪）, ywd （英伟达）, smp （树莓派）, smp2 , smp3 , ...
sub_net = 5   # 子网分区  相同分区的节点可互联

node_discovery = "man"  # 节点获取方式：man：手动配置节点ip ， auto：自动发现
node_names = [arch]    # 若为手动配置，把要连接的节点名写上
recv_udp = True         # 是否接受udp节点发现报文
env = "show"  # 环境：”exp“，做实验测试的环境 ， ”run“ 程序正常运行，"show",验收演示模式
# 调度类型：simple_greed , global_greed , cpu_res , loop,cpu_greed,prop ,prop2 具体去sched_api.py查看  <share>为共享队列模式
sched_type = "prop2"
real_time = True        # 如果sched_type采取<share>公共队列的方式，此标志位有效，True表示没来得及处理的帧会丢弃，只处理最新的帧
conn_uav = False         # 主树莓派要驱动小车，设置此标志为True

task_type = "vedio"  # 任务的类型 tasks （产生所有任务）, vedio（产生视频流任务）
# vedio
vedio_src =  0  # 视频来源 <0>为摄像头 <1>为本地视频
vedio_name = "vedio_5.mp4"    # 如果是视频读取，打开对应的视频
vedio_time_len = 10  # 要处理时间多长的视频帧 单位/min

key_frame_rate = 30  # 每隔多少帧取一个关键帧
frame_rate = 30   # 视频帧速率 30 fps
if len(sys.argv) > 1:
    vedio_time_len = int(sys.argv[1])  # 获取参数

total_frame_num = (frame_rate // key_frame_rate) * 60 * vedio_time_len  # 要产生的帧数量
# total_frame_num = 15   # 要产生的帧数量
target_list = ['wyz']  # 攻击目标
frame_interval = 0    # 帧的生成间隔

# task
gen_task_one_turn = True  # 只生成一次任务
one_turn_list = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]    # 第一次任务的序列
show_result = False  # 是否输出任务处理返回结果
gen_task = False  # 本节点是否生成任务，若为False，后面配置无效
dynamic_gen_task_rate = 15  # 动态生成任务的频率 （单位/s）
single_task = False  # 每次生成单个任务,若为True，后面配置无效
dynamic_gen_task_num = 8  # 每次动态生成任务数量


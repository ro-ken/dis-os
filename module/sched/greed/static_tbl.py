# 任务序号 0,1,2...

task_time_smp = [2.53, 0.46, 0.01, 41.54, 7.75, 15.63, 1000000]
task_time_ywd = [2.53, 0.43, 0.07, 33.17, 6.65, 1000000, 1000000]
task_time_hwj = [0.95, 0.27, 0.03, 25.47, 4.88, 10.48, 1000000]
task_time_win = [0.33, 0.23, 0.01, 3.45, 1.34, 2.20, 2.95]

# 静态时间表
task_time_table = {"smp": task_time_smp, "ywd": task_time_ywd, "hwj": task_time_hwj, "win": task_time_win,
                   "win2": task_time_win, "win3": task_time_win, "smp2": task_time_smp, "smp3": task_time_smp,
                   "smp4": task_time_smp}

# 任务运行时间随CPU负载变化的系数

coef_smp = ((0.21, 1.83), (0.02, 0.20), (0.03, -0.01), (3.34, 38.44), (0.85, 5.9), (2.25, 12.64))
coef_hwj = ((0.085, 0.69), (0.015, 0.123), (0.003, 0.011), (2.506, 21.89), (0.465, 3.86), (1.165, 8.99))

# 比例系数表
task_coef_table = {"smp": coef_smp, "hwj": task_time_hwj, "win": coef_hwj, "win2": coef_hwj, "win3": coef_hwj,
                   "smp2": coef_smp, "smp3": coef_smp, "smp4": coef_smp}

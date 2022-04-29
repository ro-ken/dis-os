from module.sched.sched import TaskCost

smp0 = TaskCost(2.35, 300, 4000, 200)
smp1 = TaskCost(7.75, 300, 4000, 200)
smp2 = TaskCost(15.63, 300, 4000, 200)
smp3 = TaskCost(0.46, 300, 4000, 200)
smp4 = TaskCost(1.00, 300, 4000, 200)
smp5 = TaskCost(0.01, 300, 4000, 200)
smp6 = TaskCost(41.54, 300, 4000, 200)
smp7 = TaskCost(1000000, 300, 4000, 200)

ywd0 = TaskCost(2.53, 300, 4000, 200)
ywd1 = TaskCost(6.65, 300, 4000, 200)
ywd2 = TaskCost(1000000, 300, 4000, 200)
ywd3 = TaskCost(0.43, 300, 4000, 200)
ywd4 = TaskCost(0.88, 300, 4000, 200)
ywd5 = TaskCost(0.07, 300, 4000, 200)
ywd6 = TaskCost(33.17, 300, 4000, 200)
ywd7 = TaskCost(1000000, 300, 4000, 200)

hwj0 = TaskCost(0.95, 300, 4000, 200)
hwj1 = TaskCost(4.88, 300, 4000, 200)
hwj2 = TaskCost(10.48, 300, 4000, 200)
hwj3 = TaskCost(0.27, 300, 4000, 200)
hwj4 = TaskCost(0.36, 300, 4000, 200)
hwj5 = TaskCost(0.03, 300, 4000, 200)
hwj6 = TaskCost(25.47, 300, 4000, 200)
hwj7 = TaskCost(1000000, 300, 4000, 200)

win0 = TaskCost(0.33, 300, 4000, 200)
win1 = TaskCost(1.34, 300, 4000, 200)
win2 = TaskCost(2.20, 300, 4000, 200)
win3 = TaskCost(0.23, 300, 4000, 200)
win4 = TaskCost(0.15, 300, 4000, 200)
win5 = TaskCost(0.01, 300, 4000, 200)
win6 = TaskCost(3.45, 300, 4000, 200)
win7 = TaskCost(2.95, 300, 4000, 200)

smp = [smp0, smp1, smp2, smp3, smp4, smp5, smp6, smp7]
ywd = [ywd0, ywd1, ywd2, ywd3, ywd4, ywd5, ywd6, ywd7]
hwj = [hwj0, hwj1, hwj2, hwj3, hwj4, hwj5, hwj6, hwj7]
win = [win0, win1, win2, win3, win4, win5, win6, win7]

task_node_table = {"smp": smp, "ywd": ywd, "hwj": hwj, "win": win, "win2": win, "win3": win, "smp2": smp, "smp3": smp,
                   "smp4": smp}

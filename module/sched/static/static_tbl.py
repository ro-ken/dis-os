from module.sched.sched  import TaskCost

smp0 = TaskCost(2.35, 300, 4000, 200)
smp1 = TaskCost(7.64, 300, 4000, 200)
smp2 = TaskCost(15.63, 300, 4000, 200)
smp3 = TaskCost(0.46, 300, 4000, 200)
smp4 = TaskCost(1.00, 300, 4000, 200)
smp5 = TaskCost(0.01, 300, 4000, 200)
smp6 = TaskCost(41.54, 300, 4000, 200)

ywd0 = TaskCost(2.53, 300, 4000, 200)
ywd1 = TaskCost(6.65, 300, 4000, 200)
ywd2 = TaskCost(1000000, 300, 4000, 200)
ywd3 = TaskCost(0.43, 300, 4000, 200)
ywd4 = TaskCost(0.88, 300, 4000, 200)
ywd5 = TaskCost(0.07, 300, 4000, 200)
ywd6 = TaskCost(33.17, 300, 4000, 200)

hwj0 = TaskCost(0.95, 300, 4000, 200)
hwj1 = TaskCost(4.71, 300, 4000, 200)
hwj2 = TaskCost(10.48, 300, 4000, 200)
hwj3 = TaskCost(0.27, 300, 4000, 200)
hwj4 = TaskCost(0.36, 300, 4000, 200)
hwj5 = TaskCost(0.03, 300, 4000, 200)
hwj6 = TaskCost(25.47, 300, 4000, 200)

smp = [smp0, smp1, smp2, smp3, smp4, smp5, smp6]
ywd = [ywd0, ywd1, ywd2, ywd3, ywd4, ywd5, ywd6]
hwj = [hwj0, hwj1, hwj2, hwj3, hwj4, hwj5, hwj6]

task_node_table = {"smp": smp, "ywd": ywd, "hwj": hwj}
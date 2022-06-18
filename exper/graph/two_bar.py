import matplotlib.pyplot as plt
import numpy as np

# plt.figure(figsize=(8,6),facecolor="yellow")
plt.rcParams["font.family"] = "kaiTi"

# x = ['smp1', 'smp1+smp2', 'smp1+smp2+hwj','smp1+smp2+smp3+hwj']
y1 = [55.6, 33.0,19.52,15.8]
y2 = [0,55.5,34.34,26.80]

# y1 = [172, 169, 177, 201, 238, 290]
# y2 = [54, 57, 58, 72, 76, 79]
# x_ticks = [2014, 2015, 2016, 2017, 2018, 2019]
x_ticks = ['smp1', 'smp1+smp2', 'smp1+smp2+hwj','smp1+smp2+smp3+hwj']
x = range(0, len(y1))
# 显示x坐标对应位置的内容，就是位置更名函数，plt.xticks()
plt.xticks(x, x_ticks)  # rotation="vertical" 倒转九十度
plt.bar(x, y1, width=0.4, label="5min")
plt.bar([i + 0.4 for i in x], y2, width=0.4, label="10min")

# plt.text(a,b,b)数据显示的横坐标、显示的位置高度、显示的数据值的大小
for y in y1, y2:
    for a, b in zip(x, y):
        if y == y2:
            a += 0.4            # 控制第二个条形数据显示的横坐标
        plt.text(a, b + 1, b, ha='center', va='bottom')


plt.title('5分钟和10分钟处理情况')

# plt.xlabel()
plt.ylabel("运行时间/分钟(min)")
plt.legend()  # 显示标签
plt.show()
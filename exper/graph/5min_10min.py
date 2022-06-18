import matplotlib.pyplot as plt

# 这两行代码解决 plt 中文显示的问题
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

x = ['smp1', 'smp1+smp2', 'smp1+smp2+hwj','smp1+smp2+smp3+hwj']
y1 = [55.6, 33.0,19.52,15.8]
y2 = [0,55.5,34.34,26.80]

# plt.bar(x, Y)
plt.title('5分钟和10分钟处理情况')

# plt.xlabel()
plt.ylabel("运行时间/分钟(min)")

# plt.ylim(0, 25)
# plt.plot(x, y1, "rs--", label="最高气温")
# plt.plot(x, y2, "rd--", label="最低气温")

bar_width = 0.3  # 条形宽度
index_male = np.arange(len(x))  # 男生条形图的横坐标
index_female = index_male + bar_width  # 女生条形图的横坐标

# 使用两次 bar 函数画出两组条形图
plt.bar(index_male, height=y1, width=bar_width, label='5min')
plt.bar(index_female, height=y2, width=bar_width, label='10min')

for y in y1, y2:
    for a, b in zip(x, y):
        if y == y2:
            a += 0.4            # 控制第二个条形数据显示的横坐标
        plt.text(a, b + 2, b, ha='center', va='bottom')


plt.legend()  # 显示图例
plt.xticks(index_male + bar_width/2, x)  # 让横坐标轴刻度显示 waters 里的饮用水， index_male + bar_width/2 为横坐标轴刻度的位置

plt.show()

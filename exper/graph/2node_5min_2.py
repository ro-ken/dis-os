import matplotlib.pyplot as plt

# 这两行代码解决 plt 中文显示的问题
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

X = ('smp1+hwj', 'smp3+hwj')
Y1 = [28.1, 27.33]
Y2 = [17.94,17.1]

# plt.bar(X, Y)
plt.title('双节点组合处理5分钟视频')

# plt.xlabel()
plt.ylabel("运行时间/分钟(min)")


bar_width = 0.2  # 条形宽度
index_male = np.arange(len(X))  # 男生条形图的横坐标
index_female = index_male + bar_width  # 女生条形图的横坐标

# 使用两次 bar 函数画出两组条形图
plt.bar(index_male, height=Y1, width=bar_width, label='树莓派发送')
plt.bar(index_female, height=Y2, width=bar_width, label='寒武纪发送')

# for a,b in zip(X,Y1):   #柱子上的数字显示
#     plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize=13)

# for a,b in zip(X,Y2):   #柱子上的数字显示
#     plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize=13)

plt.legend()  # 显示图例
plt.xticks(index_male + bar_width/2, X)  # 让横坐标轴刻度显示 waters 里的饮用水， index_male + bar_width/2 为横坐标轴刻度的位置

plt.show()

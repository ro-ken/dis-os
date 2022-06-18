import matplotlib.pyplot as plt

# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

X = ('smp1+smp2', 'smp1+smp3', 'smp1+hwj','smp2+hwj','smp3+hwj')
Y = [33, 30.13, 28.1,41.8,17.1]

plt.bar(X, Y)
plt.title('双节点组合处理5分钟视频')

# plt.xlabel()
plt.ylabel("运行时间/分钟(min)")

for a,b in zip(X,Y):   #柱子上的数字显示
    plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize=13)

plt.show()

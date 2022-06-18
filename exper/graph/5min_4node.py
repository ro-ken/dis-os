import matplotlib.pyplot as plt

# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

X = ('smp1', 'smp1+hwj', 'smp1+smp2+hwj','smp1+smp2+smp3+hwj')
Y = [55.6, 28.1, 19.52,15.8]

plt.bar(X, Y)
plt.plot(X, Y, "r", marker='.', ms=10, label="a")
plt.title('节点增加处理时间减少情况')

# plt.xlabel()
plt.ylabel("运行时间/分钟(min)")

for a,b in zip(X,Y):   #柱子上的数字显示
    plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize=13)

plt.show()

import matplotlib.pyplot as plt

# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

X = ('树莓派1', '树莓派2', '树莓派3', '寒武纪')
Y = [15.57, 15.34, 14.99,6.65]

plt.bar(X, Y)
plt.title('单节点处理254帧情况')

# plt.xlabel()
plt.ylabel("运行时间/分钟(min)")

for a,b in zip(X,Y):   #柱子上的数字显示
    plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize=13)

plt.show()

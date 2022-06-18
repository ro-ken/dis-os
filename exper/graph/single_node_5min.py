import matplotlib.pyplot as plt

# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

X = ('树莓派1', '树莓派2', '树莓派3', '寒武纪')
Y = [55.6, 56.0, 14.99,8.4]

plt.bar(X, Y)
plt.title('单节点处理5分钟视频情况')

# plt.xlabel()
plt.ylabel("运行时间/分钟(min)")

for a,b in zip(X,Y):   #柱子上的数字显示
    plt.text(a,b,'%.2f'%b,ha='center',va='bottom',fontsize=13)

plt.show()

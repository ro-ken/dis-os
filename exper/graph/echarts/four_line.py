from pyecharts.charts import Line
import pyecharts.options as opts
from pyecharts.faker import Faker
'''
set_global_opts是设置全局配置，title_opts是属性，这里通过别名opts调用options里的TitleOpts方法设置图表标题，title也是固定的属性
'''
topic = 'time'


if topic == 'num':
    y1= [10,14.2,12,27.6]
    y2= [40,96.5]
    y3= [7,22]
    y4= [29,70]
    title = '剩余帧数对比'
    y_name = '剩余帧数/张'
else:
    y1= [28,23,41.2,54.4]
    y2=[151.625,250.95]
    y3=[24.63,59.75]
    y4=[83.52,127.19]
    title = '剩余时间对比'
    y_name = '剩余时间/s'

line1=(
    Line() # 生成line类型图表
    .add_xaxis(['5min','10min','15min','20min'])  # 添加x轴，Faker.choose()是使用faker的随机数据生成x轴标签
    .add_yaxis('smp1 + smp2（以前算法）',y1)
    .add_yaxis('smp1 + smp2（1.15:1）',y2)
    .add_yaxis('smp1 + smp2（1.61:1）',y3)
    .add_yaxis('smp1 + smp2（1.61:1）(重测)',y4)
    .set_global_opts(
        # title_opts=opts.TitleOpts(title=title),
        yaxis_opts=opts.AxisOpts(
            name=y_name, # 设置y轴名字属性
            splitline_opts=opts.SplitLineOpts(is_show=True),# 这里将分割线显示
            is_scale=True # 这里范围设置true是显示线的顶端，设置为False的话就只会显示前2个数值
        )
    )
)
line1.render('pyecharts-line.html') # 生成一个名为pyecharts-line.html的网页文件，打开网页就是下图

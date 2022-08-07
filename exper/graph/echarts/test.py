from pyecharts.charts import Bar
from pyecharts import options as opts

y_name = "运行时间/s"

# V1 版本开始支持链式调用
bar = (
    Bar()
    .add_xaxis(["单节点", "双节点", "三节点", "四节点", "五节点", "六节点", "七节点"])
    # .add_yaxis("运行时间", [2261.15, 1238.383, 851.02, 710.09, 649.95, 618.68, 609.07])
    .add_yaxis("运行时间", [2261.15, 1238.383, 851.02, 710.09, 649.95, 618.68, 609.07])
    # .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    # .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
    .set_global_opts(
        # title_opts=opts.TitleOpts(title=title),
        yaxis_opts=opts.AxisOpts(
            name=y_name,  # 设置y轴名字属性
            # min_interval=0,
            min_=0,
            # max_=3000,
            splitline_opts=opts.SplitLineOpts(is_show=True),  # 这里将分割线显示
            is_scale=True  # 这里范围设置true是显示线的顶端，设置为False的话就只会显示前2个数值
        )
    )
)
bar.render()

# # 不习惯链式调用的开发者依旧可以单独调用方法
# bar = Bar()
# bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
# bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
# bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
# bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
# bar.render()
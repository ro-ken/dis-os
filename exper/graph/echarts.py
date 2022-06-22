
import pandas as pd
from pyecharts.chart import Chart
from pyecharts.option import get_all_options


class Bar(Chart):
    """
    <<< 柱状图/条形图 >>>
    柱状/条形图，通过柱形的高度/条形的宽度来表现数据的大小。
    """

    def __init__(self, title="", subtitle="", **kwargs):
        super(Bar, self).__init__(title, subtitle, **kwargs)

    def add(self, *args, **kwargs):
        self.__add(*args, **kwargs)

    def __add(self, name, x_axis, y_axis,
              is_stack=False,
              bar_category_gap="20%",
              **kwargs):
        """
        :param name:
            系列名称，用于 tooltip 的显示，legend 的图例筛选。
        :param x_axis:
            x 坐标轴数据。
        :param y_axis:
            y 坐标轴数据。
        :param is_stack:
            数据堆叠，同个类目轴上系列配置相同的 stack 值可以堆叠放置。默认为 False。
        :param kwargs:
        """
        assert len(x_axis) == len(y_axis)
        kwargs.update(x_axis=x_axis)
        chart = get_all_options(**kwargs)

        if is_stack:
            is_stack = "stack_" + str(self._option['series_id'])
        else:
            is_stack = ""
        xaxis, yaxis = chart['xy_axis']
        self._option.update(xAxis=xaxis, yAxis=yaxis)
        self._option.get('legend')[0].get('data').append(name)

        self._option.get('series').append({
            "type": "bar",
            "name": name,
            "data": y_axis,
            "stack": is_stack,
            "barCategoryGap": bar_category_gap,
            "label": chart['label'],
            "markPoint": chart['mark_point'],
            "markLine": chart['mark_line'],
            "seriesId": self._option.get('series_id'),
        })
        self._config_components(**kwargs)

if __name__ == "__main__":
    data = pd.read_excel("data\房价与工资.xlsx", header=None)
    x = data[0][1:]
    y1 = data[1][1:]
    y2 = data[2][1:]
    bar = Bar()
    bar.add('房屋均价',x,y1,mark_point=["max","min"],mark_line=["average"],is_label_show=True)
    bar.add('人均工资', x, y2,is_datazoom_show=True)
    bar.render('data/条形图02.html')
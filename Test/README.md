# Test Module

* 进行系统测试

## Module Structure

```python
# Test Module
# +-- Test.py
# +-- TaskTest.py
```

## Test.py

* 这是模块的API入口, 主要提供两个API: API_RandomTask_MaxLoad, API_RandomTask_LoadDict

```python
# def API_RandomTask_MaxLoad(task_number, start_label, end_label, max_times, max_load)
# +- task_number - 要生成的任务数量
# +- start_label - 指定生成任务范围开始标号
# +- end_label - 指定生成任务范围结束标号(闭区间[])
# +- max_times - 生成的任务的重复数量不超过max_times
# +- max_load - 生成任务的最大负载(任务最大执行次数)
# 返回： task_list = [(task_label, task_load),..]
```

```python
# def API_RandomTask_LoadDict(task_number, start_label, end_label, max_times, load_dict)
# +- task_number - 要生成的任务数量
# +- start_label - 指定生成任务范围开始标号
# +- end_label - 指定生成任务范围结束标号(闭区间[])
# +- max_times - 生成的任务的重复数量不超过max_times
# +- load_dict - 生成任务的最大负载(任务最大执行次数), 任务标号对应字典key, 任务负载对应字典value, 如 {task_label:task_load,..}, 任务标号要严格对应start_label和end_label
# 返回： task_list = [(task_label, task_load),..]
```
import TaskTest


# 随机生成测试任务
def API_RandomTask_MaxLoad(task_number, start_label, end_label, max_times, max_load):
    return TaskTest.RandomTask(task_number, start_label, end_label, max_times, max_load)

# 随机生成测试任务
def API_RandomTask_LoadDict(task_number, start_label, end_label, max_times, load_dict):
    task_list = TaskTest._random_task_loaddict(task_number, start_label, end_label, max_times, load_dict)
    if task_list == None:
        print("Error: 参数不合法")
        return []
    return task_list

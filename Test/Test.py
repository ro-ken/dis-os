import TaskTest


# 随机生成测试任务
def API_RandomTask_MaxLoad(task_number, start_label, end_label, max_times, max_load):
    return TaskTest.RandomTask(task_number, start_label, end_label, max_times, max_load)

# 随机生成测试任务
def API_RandomTask_LoadDict(task_number, start_label, end_label, max_times, load_dict):
    task_list = TaskTest.RandomTask_LoadList(task_number, start_label, end_label, max_times, load_dict)
    if task_list == None:
        print("Error: 参数不合法")
        return []
    return task_list


# if __name__ == '__main__':
#     task_list = API_RandomTask_MaxLoad(10, 0, 6, 3, 10)
#     print(task_list)
#     a = {1:2,2:4,3:4,4:5}
#     task_list = API_RandomTask_LoadDict(10, 1, 4,3, a)
#     print(task_list)

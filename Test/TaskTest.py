import random

MAX_Label = 20
MAX_TIMES = 20
MAX_NUMBER = 20

# 检测生成的任务是否合格
def IsValidity(task_list, max_times):
    if task_list == []:
        return False
    task_number_list = [task for task, load in task_list]
    task_set = set(task_number_list)
    for task in task_set:
        if task_number_list.count(task) > max_times:
            return False
    return True

# 生成随机任务
def _random_task(task_number, start_label, end_label, max_load):
    task_list = []
    for loop_times in range(task_number):
        task_label= random.randint(start_label, end_label)
        task_load = random.randint(1, max_load)
        task_list.append((task_label, task_load))
    return task_list

def RandomTask(task_number, start_label, end_label, max_times, max_load):
    '''
    - 生成task_number个随机任务, 约束条件为:
    -    start_label <= task_label <= end_label
    -    1 <= task_load <= load
    '''
    TaskList = []
    while not IsValidity(TaskList, max_times):
        TaskList = _random_task(task_number, start_label, end_label, max_load)
    
    return TaskList
        
    

# 检测任务负载约束是否合法
def CheckLoadDict(start_label, end_label, load_dict):
    # 检测 load_dict 是否合法
    if not isinstance(load_dict, dict):
        return False
    # 检测字典元素是否非法
    if load_dict == {}:
        return False
    if len(load_dict) != end_label - start_label + 1:
        return False
    for key, value in load_dict.items():
        if not start_label <= key <= end_label:
            return False
        if value < 0:
            return False
    return True


# 检测任务约束条件是否合法
def CheckConstraint(task_number, start_label, end_label, max_times):
    # 检测生成任务范围是否合法
    if (not 0 <= start_label <= MAX_Label) or (not 0 <= end_label <= MAX_Label):
        return False
    if end_label - start_label + 1 < 0:
        return False

    # 检测生成任务数量是否合法
    if not 0 <= task_number <= MAX_NUMBER :
        return False
    
    # 检测任务重复数量是否合法
    if not 0<= max_times <= MAX_TIMES:
        return False
    
    return True
    
# 在任务负载约束条件下生成随机任务
def _random_task_loaddict(task_number, start_label, end_label, load_dict):
    task_list = []
    for loop_times in range(task_number):
        task_label = random.randint(start_label, end_label)
        max_load = load_dict[task_label]
        task_load = random.randint(1, max_load)
        task_list.append((task_label, task_load))
    return task_list

def RandomTask_LoadList(task_number, start_label, end_label, max_times, load_dict):
    # 检测参数是否合法
    if not CheckConstraint(task_number, start_label, end_label, max_times):
        return None
    if not CheckLoadDict(start_label, end_label, load_dict):
        return None

    # 生成任务
    TaskList = []
    while not IsValidity(TaskList, max_times):
        TaskList = _random_task_loaddict(task_number, start_label, end_label, load_dict)
    
    return TaskList

# if __name__ == '__main__':
#     task_list = RandomTask(10, 0, 6, 3, 10)
#     print(task_list)
#     a = {1:2,2:4,3:4,4:5}
#     task_list = RandomTask_LoadList(10, 1, 4,3, a)
#     print(task_list)
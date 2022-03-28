from module.sched.sched  import IScheduler
from .static_tbl import task_node_table


class Scheduler(IScheduler):

    def __init__(self, node, nodes, node_resources):
        super().__init__(node, nodes, node_resources)

    def divide_tasks(self, task_list, node_resources):
        res = {"smp": [], "ywd": [], "hwj": []}
        t_time = {"smp": 0, "ywd": 0, "hwj": 0}

        for task in task_list:
            node = self.select_min_time_node(t_time, task)
            res[node].append(task)
            t_time[node] += task_node_table[node][task].time
        print(t_time)
        return [res["smp"], res["ywd"], res["hwj"]]


    def select_min_time_node(self, t_time, task) -> str:
        node = "smp"
        next_node = "hwj"
        if task_node_table[node][task].time + t_time[node] > task_node_table[next_node][task].time + t_time[next_node]:
            node = next_node
        next_node = "ywd"
        if task_node_table[node][task].time + t_time[node] > task_node_table[next_node][task].time + t_time[next_node]:
            node = next_node
        return node

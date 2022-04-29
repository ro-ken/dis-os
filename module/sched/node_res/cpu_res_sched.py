from module.sched.sched import IScheduler

# 选择当前CPU利用率最低的节点进行调度
def select_max_cpu_res_node(node_list):
    max_key = node_list.keys()[0]  # 最大剩余率的key
    max_free_ratio = node_list.values()[0]  # 还剩余多少利用率
    for key in node_list:
        res = node_list[key].res
        cpu = res.cpu
        if (1 - cpu.use_ratio) * cpu.logic_num > max_free_ratio:
            max_key = key
            max_free_ratio = (1 - cpu.use_ratio) * cpu.logic_num
    node = node_list[max_key]
    return node

# 根据当前CPU使用率进行调度
class Scheduler(IScheduler):

    def get_node(self):
        node = select_max_cpu_res_node(self.nodes)
        return node

    def single_task_sched(self, task, node_list):
        node = select_max_cpu_res_node(node_list)
        max_key = node.key
        return {max_key: [task]}

    def multi_task_sched(self, task_list, node_list):

        raise Exception("this sched can't process multiple task")

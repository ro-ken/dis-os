from module.sched.sched import IScheduler

# 根据当前CPU使用率进行调度
class Scheduler(IScheduler):

    def single_task_sched(self, task, node_list):

        max_key = node_list.keys()[0]  # 最大剩余率的key
        max_free_ratio = node_list.values()[0]  # 还剩余多少利用率
        for key in node_list:
            res = node_list[key].res
            cpu = res.cpu
            if (1 - cpu.use_ratio) * cpu.logic_num > max_free_ratio:
                max_key = key
                max_free_ratio = (1 - cpu.use_ratio) * cpu.logic_num

        return {max_key: [task]}

    def multi_task_sched(self, task_list, node_list):

        raise Exception("this sched can't process multiple task")

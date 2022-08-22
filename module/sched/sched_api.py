
# 供高层调用接口

from settings import sched_type

# 根据不同配置用不同的调度器

if sched_type == "simple_greed":
    from .greed.simple_greed_sched import Scheduler
elif sched_type == "global_greed":
    from .greed.global_greed_sched import Scheduler
elif sched_type == "cpu_greed":
    from .greed.cpu_greed_sched import Scheduler
elif sched_type == "cpu_res":
    from .node_res.cpu_res_sched import Scheduler
elif sched_type == "loop":
    from .loop.loop_sched import Scheduler
elif sched_type == "prop":
    from .proportion.proportion_sched import Scheduler
elif sched_type == "prop2":
    from .proportion2.proportion_sched import Scheduler
else:
    from .sched import IScheduler as Scheduler
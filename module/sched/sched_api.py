
# 供高层调用接口

from settings import sched_type

# 根据不同配置用不同的调度器

if sched_type == "static":
    from .static.static_sched import Scheduler

elif sched_type == "dynamic":
    from .dynamic.dynamic_sched import Scheduler








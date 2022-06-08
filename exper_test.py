
import sys
from app.exper import local_task_time_test
from app.exper import local_vedio_task_time_test


if __name__ == '__main__':

    cpu_rate = 50
    if len(sys.argv) > 1:
        cpu_rate = sys.argv[1]  # 获取参数
    # local_task_time_test.run(range(6),cpu_rate)      # 本地时间运行测试
    local_vedio_task_time_test.run(cpu_rate)      # 本地时间运行测试
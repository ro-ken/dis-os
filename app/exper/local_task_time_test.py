from tools.utils import ROOT

# 任务本地测试文件

# model
from ..app_api import api_list
from .util import *
import sys

ROOT = os.path.split(os.path.realpath(__file__))[0]

def run(list, cpu_use_rate = 0):

    path = ROOT + '/output/local_task_time_cpu_{}.txt'.format(cpu_use_rate)
    sys.argv = [sys.argv[0]]
    write_file(path, b'local task time:\n')
    for i in list:
        print("task start" + str(i))
        write_time_start(path, 'task {}'.format(i))
        api_list[i]()
        write_time_end(path, 'task {}'.format(i))
        print("task end" + str(i))

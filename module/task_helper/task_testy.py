import time

from settings import *
from tools import utils
from tools.utils import ROOT
from tools.utils import mytime


# 这个类用来做任务测试

class TaskTesty:

    def __init__(self,task_handler):
        self.task_handler = task_handler

    # 应用调用接口封装, 调用全部的7个应用
    def do_all_task(self):
        self.task_handler.task_linear_regression()
        self.task_handler.task_yolox_image()
        self.task_handler.task_yolo5()
        self.task_handler.task_compose()
        self.task_handler.task_lic_detect()
        self.task_handler.task_num_detect()
        self.task_handler.task_monet_transfer()
        self.task_handler.task_style_transfer()


    # 应用测试, 测试应用调用时间、消耗资源(CPU、内存), 结果保存在 ./oputput/out_time.txt文件下
    def per_task_time(self):
        path = ROOT + 'output/{}_per_task_time.txt'.format(arch)
        utils.write_time_start(path, arch + ' task_0', mytime(), 'w')
        self.solution(win=[0], mac=[0], smp=[0], hwj=[0], ywd=[0])
        utils.write_time_end(path, arch + ' task_0', mytime())

        utils.write_time_start(path, arch + ' task_1', mytime())
        self.solution(win=[1], mac=[1], smp=[1], hwj=[1], ywd=[1])
        utils.write_time_end(path, arch + ' task_1', mytime())

        if arch != "ywd":
            utils.write_time_start(path, arch + ' task_2', mytime())
            self.solution(win=[2], mac=[2], smp=[2], hwj=[2], ywd=[2])
            utils.write_time_end(path, arch + ' task_2', mytime())

        utils.write_time_start(path, arch + ' task_3', mytime())
        self.solution(win=[3], mac=[3], smp=[3], hwj=[3], ywd=[3])
        utils.write_time_end(path, arch + ' task_3', mytime())

        utils.write_time_start(path, arch + ' task_4', mytime())
        self.solution(win=[4], mac=[4], smp=[4], hwj=[4], ywd=[4])
        utils.write_time_end(path, arch + ' task_4', mytime())

        utils.write_time_start(path, arch + ' task_5', mytime())
        self.solution(win=[5], mac=[5], smp=[5], hwj=[5], ywd=[5])
        utils.write_time_end(path, arch + ' task_5', mytime())

        if arch == "win":
            utils.write_time_start(path, arch + ' task_6', mytime())
            self.solution(win=[6], mac=[6], smp=[6], hwj=[6], ywd=[6])
            utils.write_time_end(path, arch + ' task_6', mytime())


    # 应用测试, 测试应用调用时间、消耗资源(CPU、内存), 结果保存在 ./oputput/out_time.txt文件下
    def five_solution(self):
        path = ROOT + 'output/out_time.txt'
        utils.write_time_start(path, arch + ' solution_1', mytime(), 'w')
        self.solution(win=[2], mac=[1, 0, 5], smp=[2], hwj=[2, 3], ywd=[4])
        utils.write_time_end(path, arch + ' solution_1', mytime())

        utils.write_time_start(path, arch + ' solution_2', mytime())
        self.solution(win=[2, 2], mac=[], smp=[2, 2], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_2', mytime())

        utils.write_time_start(path, arch + ' solution_3', mytime())
        self.solution(win=[1, 1, 2, 2, 4, 4], mac=[], smp=[1, 1, 2, 2, 4, 4], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_3', mytime())

        utils.write_time_start(path, arch + ' solution_4', mytime())
        self.solution(win=[3, 3, 4, 4], mac=[], smp=[3, 3, 4, 4], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_4', mytime())

        utils.write_time_start(path, arch + ' solution_5', mytime())
        self.solution(win=[2, 4, 4], mac=[], smp=[2, 4, 4], hwj=[], ywd=[])
        utils.write_time_end(path, arch + ' solution_5', mytime())

    # 节点环境检测, 根据不同的节点调用不同的应用接口
    def solution(self, win, mac, smp, hwj, ywd):
        if arch == "win":
            self.task_handler.do_task_by_ids(win)
        elif arch == "mac":
            self.task_handler.do_task_by_ids(mac)
        elif arch == "smp":
            self.task_handler.do_task_by_ids(smp)
        elif arch == "hwj":
            self.task_handler.do_task_by_ids(hwj)
        elif arch == "ywd":
            self.task_handler.do_task_by_ids(ywd)

    def test_yolox_time(self):

        times = 5
        total_time = 0

        for i in range(times):
            start = time.time()
            image = self.task_handler.task_yolox_image()
            end = time.time()
            print("times {} = {}".format(i, end - start))
            total_time += end - start

        print("yolox grpc avg time = {}".format(total_time / times))

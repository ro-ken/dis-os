from time import time
import os
import sys
import psutil
from datetime import datetime
from model.lic_detect import detect_rec_img
from model.ai import ai
from model.face_ai.faceai import compose
from model.yolox.tools import demo
from model.yolo5 import detect
from model.style_transfer import train
import cv2

line_num = 1
pid = int(os.getpid())
proc = psutil.Process(pid)
print(proc.name())
def getCPUstate(interval=1):
    return ("CPU: " + str(proc.cpu_percent(None))+ "%")

def getMemorystate():
    phymem = psutil.virtual_memory()
    line = "Memory: %5s%% %6s/%s" % (
        phymem.percent,
        str(int(phymem.used / 1024/1024)) + "M",
        str(int(phymem.total / 1024/1024)) + "M"
    )
    return line

def getMemorystate2():
    return (' Memory:' +str(proc.memory_info().rss /1024 /1024)+'MB')

def getinfo():
    #file_name = str(datetime.now().strftime("%m-%d_%H:%M_")) + proc.name() + '.txt'
    text = getCPUstate() + getMemorystate2()
    print(text)

def choose(TaskId):
    TaskId = int(TaskId)
    if TaskId == 1:
        print("启动yolox任务......")
        demo.run()
        print("yolox任务计算完毕......")
    elif TaskId == 2:
        print("启动yolo5任务......")
        detect.main(detect.parse_opt(),None)
        print("yolo5任务计算完毕......")
    elif TaskId == 3:
        print("启动线性回归任务......")
        ai.run()
        print("线性回归任务计算完毕......")
    elif TaskId == 4:
        print("启动faceai任务......")
        img = compose.main(None,None)
        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("faceai任务计算完毕......")
    elif TaskId == 5:
        print("启动车牌识别任务......")
        detect_rec_img.run()
        print("车牌识别任务计算完毕......")
    elif TaskId == 6:
        print("启动手写数据集识别任务......")
    elif TaskId == 7:
        print("启动风格迁移任务......")
        train.start()
        print("风格迁移任务计算完毕......")

if __name__ == "__main__":
    print("请输入任务id，每个任务使用空格隔开\n1.yolox\n2.yolo5\n3.线性回归\n4.faceai\n5.车牌识别\n6.手写数据集识别\n7.风格迁移")
    temp = input("请输入:")
    d = temp.split(' ')
    start = time()
    print("目前的资源占用情况为：")
    getinfo()
    for i in range(len(d)):
        print(d[i])
        choose(str(d[i]))
    print("运行计算任务结束后资源占用情况为 ：")
    getinfo()
    end = time()
    print("总共计算时间为："+str(end-start))
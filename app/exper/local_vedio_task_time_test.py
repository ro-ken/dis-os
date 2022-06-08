import cv2

from tools.utils import ROOT

# 任务本地测试文件

# model
from ..face_recognition import face_recognition
from .util import *
import sys

ROOT = os.path.split(os.path.realpath(__file__))[0]

def run(cpu_use_rate = 0):

    path = ROOT + '/output/local_vedio_task_time_cpu_{}.txt'.format(cpu_use_rate)
    sys.argv = [sys.argv[0]]
    write_file(path, b'local vedio task time:\n')
    recognizer = face_recognition.Face_Recognizer()
    img = cv2.imread(ROOT + '/../face_recognition/test.jpg')
    for i in range(3):

        print("vedio task start" )
        write_time_start(path, 'vedio task turn {}'.format(i))
        success, res_img = recognizer.face_recognition(img, ['rq'], 0)
        # cv2.imshow('face', res_img)
        # cv2.waitKey(0)
        write_time_end(path, 'vedio task turn {}'.format(i))
        print("vedio task end")
        time.sleep(0.5)     # 让处理器休息一下

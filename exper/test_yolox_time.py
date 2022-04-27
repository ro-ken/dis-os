from time import time

import cv2

from app import app_api
from tools.utils import ROOT

times = 5

total_time = 0

for i in range(times):
    start = time()
    image = app_api.yolo_x.start(PATH=ROOT + 'dataset/gather.png')
    end = time()
    print("times {} = {}".format(i, end - start))
    total_time += end - start

print("yolox local avg time = {}".format(total_time / times))

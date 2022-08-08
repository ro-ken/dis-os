import os
import threading
from tools import utils
# 把处理完的视频显示的线程
# 显示图像
import os
import time

import cv2  # 导入从cv2模块
# 此接口通用
from tools.utils import ROOT


def vedio_show_process():
    path = ROOT + './output/frame_res/'

    rate = 6  # 每秒播放的帧数
    i = -1

    while True:
        i += 1
        next_file = "{}/{}.jpg".format(path, i)
        while not os.path.exists(next_file):
            # print(time.time())
            time.sleep(0.3)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        image = cv2.imread(next_file)  # 读取图像
        cv2.imshow("image", image)  # 显示图像
        # cv2.waitKey(1000//rate)  # 默认为0，无限等待
        if cv2.waitKey(1000 // rate) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()  # 释放所有窗口



# 下面的接口供windows 调用
class VedioHandlerThread(threading.Thread):
    def __init__(self,node):
        super().__init__()
        self.node = node

    def run(self) -> None:
        title = "searching target ... "
        while True:
            if len(self.node.recv_queue) == 0:
                time.sleep(0.3)
            else:
                frame,seq = self.node.recv_queue.pop(0)
                print("----------seq = {}".format(seq))
                utils.imshow_vedio(title,frame)
                if seq == self.node.target_frame:
                    break
        time.sleep(60 * 60 * 24)
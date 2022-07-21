# 显示图像
import os
import time

import cv2  # 导入从cv2模块

path = '../output/frame_res/'

total_num = 10  # 总共帧数

rate = 10    # 每秒播放的帧数
i = -1
quit = False

while True:
    i += 1
    next_file = "{}/{}.jpg".format(path, i)
    while not os.path.exists(next_file):
        # print(time.time())
        time.sleep(0.3)
        if cv2.waitKey(1)&0xFF==ord('q'):
            break

    image = cv2.imread(next_file)  # 读取图像
    cv2.imshow("image", image)  # 显示图像
   # cv2.waitKey(1000//rate)  # 默认为0，无限等待
    if cv2.waitKey(1000//rate)&0xFF==ord('q'):
        break

cv2.destroyAllWindows()  # 释放所有窗口
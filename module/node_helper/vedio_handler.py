import threading
from tools import utils
# 把处理完的视频显示的线程
import time


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
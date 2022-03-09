from time import time
from model.lic_detect import detect_rec_img
from model.ai import ai
from model.face_ai.faceai import compose
from model.yolox.tools import demo
from model.yolo5 import detect
from model.style_transfer import train
import cv2
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
    for i in range(len(d)):
        print(d[i])
        choose(str(d[i]))
    end = time()
    print("总共计算时间为："+str(end-start))
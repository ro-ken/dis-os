from tools.utils import ROOT

# model
from model.ai import ai
from model.yolox.tools import demo
from model.yolo5 import detect
from model.face_ai.faceai import compose
from model.lic_detect import detect_rec_img
from model.num_detect.classifier import predict
# from model.monet_transfer import

from tools.settings import arch

if arch == "win" or arch == "mac":
    from model.style_transfer import train


def task_ai():
    ai.run()


def task_yolo5(img_path=None):
    detect.start(img_path)


def task_yolox(img=None):
    demo.start(img)


def task_face_ai(img=None, img_compose=None):
    compose.start(img, img_compose)


def task_lic_detect(img=None):
    detect_rec_img.start(img)


def task_num_detect():
    predict.predict_number()


def style_transfer(content_image_path=None, style_image_path=None):
    train.start(content_image_path, style_image_path)


task_list = [task_ai, task_yolo5, task_yolox, task_face_ai, task_lic_detect, task_num_detect, style_transfer]


def run(list):
    for i in list:
        print("task start" + str(i))
        task_list[i]()
        print("task end" + str(i))

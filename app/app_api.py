from tools.utils import ROOT

# model
from app.linear_regression import linear_regression
from app.yolo_x.tools import yolo_x
from app.yolo_5 import yolo_5
from app.compose import compose
from app.lic_detect import lic_detect
from app.num_detect.classifier import num_detect
from app.monet_transfer import monet_transfer

from settings import arch

if arch == "win" or arch == "mac":
    from app.style_transfer import style_transfer


def api_linear_regression():
    linear_regression.run()


def api_yolo_5(img_path=None):
    yolo_5.start(img_path)


def api_yolo_x(img=None):
    yolo_x.start(img)


def api_compose(img=None, img_compose=None):
    compose.start(img, img_compose)


def api_lic_detect(img=None):
    lic_detect.start(img)


def api_num_detect():
    num_detect.predict_number()


def api_style_transfer(content_image_path=None, style_image_path=None):
    style_transfer.start(content_image_path, style_image_path)


def api_monet_transfer():
    monet_transfer.start()


api_list = [api_linear_regression, api_yolo_5, api_yolo_x, api_compose, api_lic_detect, api_num_detect, api_style_transfer]


def run(list):
    for i in list:
        print("task start" + str(i))
        api_list[i]()
        print("task end" + str(i))

if __name__ == '__main__':
    # run(range(7))
    # api_monet_transfer()
    api_style_transfer()
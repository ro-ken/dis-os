from tools.utils import ROOT

# model
from app.linear_regression import linear_regression
from app.yolo_x.tools import yolo_x
from app.yolo_5 import yolo_5
from app.compose import compose
from app.lic_detect import lic_detect
from app.num_detect.classifier import num_detect
from app.monet_transfer import monet_transfer
from app.path_planing import path_planning
from app.face_recognition import face_recognition
from app.face_recognition import face_recognition_local_test

from settings import arch

# if arch == "win" or arch == "mac":
#     from app.style_transfer import style_transfer

#
# def api_style_transfer(content_image_path=None, style_image_path=None):
#     return style_transfer.start(content_image_path, style_image_path)

def api_linear_regression():
    return linear_regression.run()


def api_yolo_5(img_path=None):
    return yolo_5.start(img_path)


def api_yolo_x(img=None):
    return yolo_x.start(img)


def api_compose(img=None, img_compose=None):
    return compose.start(img, img_compose)


def api_lic_detect(img=None):
    return lic_detect.start(img)


def api_num_detect():
    return num_detect.predict_number()




def api_monet_transfer():
    return monet_transfer.start()


def api_face_recognition_():
    return face_recognition.Face_Recognizer()

def api_face_recognition():
    return face_recognition_local_test.run()

def api_path_planning():
    return path_planning.main()


api_list = [api_linear_regression,  # 0
            api_compose,            # 1
            api_num_detect,         # 2
            api_monet_transfer,     # 3
            api_yolo_x,             # 4
            api_yolo_5,             # 5
            api_face_recognition    # 6
            ]



def run(list):
    for i in list:
        print("task start" + str(i))
        api_list[i]()
        print("task end" + str(i))


if __name__ == '__main__':
    run(range(6))
    # run(range(5,8))
    # api_yolo_5()
    # api_monet_transfer()
    # api_style_transfer()
    # api_face_recognition()

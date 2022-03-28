# -*- coding: utf-8 -*-
# @File    : settings.py
# @Author  : AaronJny
# @Time    : 2020/03/13
# @Desc    :


# 内容特征层及loss加权系数
import os

ROOT = os.path.split(os.path.realpath(__file__))[0] + '/'

CONTENT_LAYERS = {'block4_conv2': 0.5, 'block5_conv2': 0.5}
# 风格特征层及loss加权系数
STYLE_LAYERS = {'block1_conv1': 0.2, 'block2_conv1': 0.2, 'block3_conv1': 0.2, 'block4_conv1': 0.2,
                'block5_conv1': 0.2}
# 内容图片路径
CONTENT_IMAGE_PATH = ROOT + 'images/content.jpg'
# 风格图片路径
STYLE_IMAGE_PATH = ROOT + 'images/style.jpg'
# 生成图片的保存目录
OUTPUT_DIR = ROOT + 'output'

# 内容loss总加权系数
CONTENT_LOSS_FACTOR = 1
# 风格loss总加权系数
STYLE_LOSS_FACTOR = 100

# 图片宽度
WIDTH = 450
# 图片高度
HEIGHT = 300

# 训练epoch数
EPOCHS = 1
# 每个epoch训练多少次
# STEPS_PER_EPOCH = 100
STEPS_PER_EPOCH = 1
# 学习率
LEARNING_RATE = 0.03

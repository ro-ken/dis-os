import os
import numpy as np
import cv2
import json

from tools import  task_handler
from tools import task_service
from tools import settings
from tools import utils
from tools.proto import task_pb2
from tools.proto import task_pb2_grpc
import Const

import psutil

# 测试结果集
ApplicationPerformanceList = []

# 检测特定平台上可运行应用
#   返回一维列表, 包含每个应用的标号
def ApplicationIsRun():
    allow_applications = []

    # 获取目标平台的标号
    platform_label = -1
    for label, platform in Const.PlatformLabel.items():
        if platform == settings.arch:
            platform_label = label
            break
    # 当目标平台不合法时, 提出警告, 并返回None值
    if platform_label == -1:
        print("Error: can't confirm this node's type, please check the settings.arch varialbe")
        return None

    # 依次检测应用是否能够在该节点上运行
    for application_label in range(7):
        if Const.IsRun(application_label, platform_label) == False:
            continue
        allow_applications.append(application_label)
    
    return allow_applications

# 计算平均值
def CacAveragePerformance():
    pass

# 对应不同节点, 使用不同的测试方法
def UnifyPerformance():
    # 获取在该节点上的可运行应用
    allow_applications = ApplicationIsRun()
    pass
'''
    节点的通信模块，负责连接此系统和小车
'''
import settings
from .conn_target_follow import task_follow_target

# from .conn_face_recognition import task_target_find
from .conn_face_recognition_join import task_target_find

# 连接小车主程序
def conn_vehicle(node):
    if settings.task_type == "vedio":
        task_target_find(node)
    else:
        task_follow_target(node)


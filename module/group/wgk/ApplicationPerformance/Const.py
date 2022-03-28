# 应用数量
ApplicationNumber = 7

# 每个应用对应的标号
ApplicationLabel = {
    0:'task_linear_regression',
    1:'task_yolox_image',
    2:'task_yolo5',
    3:'task_compose',
    4:'task_lic_detect',
    5:'task_num_detect',
    6:'task_monet_transfer',
}

PlatformLabel = {
    0:'raspberry',
    1:'nanob02',
    2:'mlu220',
}

def IsRun(application_label, platform_label):
    application = ApplicationLabel[application_label]
    platform = PlatformLabel[platform_label]
    if ApplicationLimit[application][platform] == 1:
        return True
    else:
        return False

# 每个应用在特定平台上是否能够运行
#   raspberry4b - 树莓派4b
#   nanob02     - 英伟达Jetson Nano B02
#   mlu220      - 寒武纪Mlu220
ApplicationLimit = {
    'task_linear_regression':{
        'raspberry4b':1,
        'nanob02':1,
        'mlu220':1,
    },
    'task_yolox_image':{
        'raspberry4b':1,
        'nanob02':1,
        'mlu220':1,
    },
    'task_yolo5':{
        'raspberry4b':1,
        'nanob02':0,
        'mlu220':1,
    },
    'task_compose':{
        'raspberry4b':1,
        'nanob02':1,
        'mlu220':1,
    },
    'task_lic_detect':{
        'raspberry4b':1,
        'nanob02':1,
        'mlu220':1,
    },
    'task_num_detect':{
        'raspberry4b':1,
        'nanob02':0,
        'mlu220':0,
    },
    'task_monet_transfer':{
        'raspberry4b':1,
        'nanob02':1,
        'mlu220':1,
    },
    # 'task_style_transfer':{
    #     'raspberry4b':1,
    #     'nanob02':1,
    #     'mlu220':0,
    # },
}

# class Performance():
#     def __init__(self,node_name):
#         self.node_name = node_name
#         self.runtime = 0,
#         self.cpu = {
#             'use_ratio':0,
#             'real_num':0,
#             'logic_num':0,
#         }
#         self.mem = {
#             'total':0,
#             'used':0,
#             'available':0,
#         }
#         self.disc = {
#             'total':0,
#             'used':0,
#             'available':0,
#         }

# class PlatfromWithPerformance():
#     def __init__(self, name):
#         self.name = name
#         self.raspberry = Performance('')
#         self.nanob02 = Performance()
#         self.mlu220 = Performance()

# class ApplicationPerformanceInPlatform():
#     def __init__(self):
#         self.task_linear_regression = PlatfromWithPerformance('task_linear_regression')
#         self.task_yolox_image = PlatfromWithPerformance('task_yolox_image')
#         self.task_yolo5 = PlatfromWithPerformance('task_yolo5')
#         self.task_compose = PlatfromWithPerformance('task_compose')
#         self.task_lic_detect = PlatfromWithPerformance('task_lic_detect')
#         self.task_num_detect = PlatfromWithPerformance('task_num_detect')
#         self.task_monet_transfer = PlatfromWithPerformance('task_monet_transfer')

#     # 将性能测试结果保存在json文件中
#     def WriteToJson(self):
#         # 构造字典
#         pass

#     # 从json文件中读取性能测试结果
#     def ReadFromJson(self):
#         pass

# # 特定应用与特定节点之间的性能测试结果
# #   应用/节点/性能指标
# ApplicationPerformanceInPlatform 
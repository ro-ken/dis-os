import Const


# 检测指定应用是否能够在指定节点上运行
#   能成功运行则返回True
#   否则，返回False
def IsRun(application_label, platform_label):
    application = Const.ApplicationLabel[application_label]
    platform = Const.PlatformLabel[platform_label]
    if Const.ApplicationLimit[application][platform] == 1:
        return True
    else:
        return False
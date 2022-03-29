from numpy import source
import communication_api


# 测试任务查询功能是否正常
def test_communication_taskquery(SourceNode, TargetNode, TaskNumber):
    success, remark = communication_api.TaskQuery(SourceNode, TargetNode, TaskNumber)
    print(success)
    print('\n')
    print(remark)

# 测试图片发送功能是否正常
def test_communication_image(SourceNode, TargetNode, TaskNumber, ImagePath):
    success, remark = communication_api.SendImage(SourceNode, TargetNode, TaskNumber, ImagePath)
    print(success)
    print('\n')
    print(remark)

# 测试视频发送功能是否正常
def test_communication_video(SourceNode, TargetNode, TaskNumber, VideoPath):
    success, remark = communication_api.SendVideo (SourceNode, TargetNode, TaskNumber, VideoPath)
    print(success)
    print('\n')
    print(remark)

if __name__ == '__main__':
    test_communication_taskquery(1,2,0)
    test_communication_image(1,3,1,'01.jpg')
    test_communication_video(1,3,2,'test2.mp4')
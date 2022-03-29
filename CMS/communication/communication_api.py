from asyncio import FastChildWatcher, Task
import communication_server
import communication_client
import route
import communication_pb2_grpc
import communication_pb2
import grpc
from concurrent import futures

# 向TargetNode节点询问当前是否空闲
def TaskQuery(SourceNode, TargetNode, TaskNumber):
    # 如果目标节点和本节点相同，返回False
    if TargetNode == route.SelfNodeNumber:
        return False, 'Error: TargetNode equal selfNode, please check code'

    # 建立stub客户端，向目标节点发送报文询问
    replay = communication_client.TaskMessage(SourceNode, TargetNode, TaskNumber)
    return replay.recepted, replay.remark


# 向TargetNode节点发送图片，图片路径为ImagePath
def SendImage(SourceNode, TargetNode, TaskNumber, ImagePath):
    # 如果目标节点和本节点相同，返回False
    if TargetNode == route.SelfNodeNumber:
        return False, 'Error: TargetNode equal selfNode, please check code'

    # 将图片转成字节流
    image_str = route.ImageEncode(ImagePath)
    replay = communication_client.ImageMessage(SourceNode, TargetNode, TaskNumber, image_str)
    return replay.recepted, replay.remark


# 向TargetNode节点发送视频文件，视频路径为VideoPath
def SendVideo(SourceNode, TargetNode, TaskNumber, VideoPath):
    # 如果目标节点和本节点相同，返回False
    if TargetNode == route.SelfNodeNumber:
        return False, 'Error: TargetNode equal selfNode, please check code'
    
    # 获取视频属性
    VideoFps, VideoHeight, VideoWidth = route.GetVideoAttr(VideoPath)
    VideoHead = {}
    VideoHead['SourceNode'] = SourceNode
    VideoHead['TargetNode'] = TargetNode
    VideoHead['TaskNumber'] = TaskNumber
    VideoHead['VideoFps'] = VideoFps
    VideoHead['VideoHeight'] = VideoHeight
    VideoHead['VideoWidth'] = VideoWidth


    # 发送视频头报文
    replay = communication_client.VideoHeadMessage(VideoHead)
    if replay.recepted == False:
        return replay.recepted, replay.remark
    
    # 获取 yield 迭代器用来grpc的stram输出
    VideoDataRouteIterator = route.VideoEncode(SourceNode, TargetNode, TaskNumber, VideoPath)
    replay = communication_client.VideoDataMessage(TargetNode, VideoDataRouteIterator)
    return replay.recepted, replay.remark


    

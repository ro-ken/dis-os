import route
import grpc
import numpy as np
import cv2
import communication_pb2_grpc
import communication_pb2
import communication_server

# 利用grpc的远程调用，模拟查询报文发送
def TaskMessage(SourceNode,TargetNode,TaskNumber):
    # 查询路由表，发现下一跳地址
    routeinfo = route.GetNextNodeAddr(TargetNode)
    if routeinfo == None:
        return communication_pb2.TaskRouteReply(recepted = False, remark = "In Node{} Have found TargetNode{} 的 next Route".format(route.SelfNodeNumber,TargetNode))

    # 远程调用service发送查询报文
    channel = grpc.insecure_channel(routeinfo)
    stub = communication_pb2_grpc.CommunicationStub(channel)
    TaskRouteRequest = communication_pb2.TaskRouteRequest(SourceNode = SourceNode,TargetNode = TargetNode,TaskNumber = TaskNumber)
    return stub.TaskRoute(TaskRouteRequest)

# 利用grpc的远程调用，模拟数据传送报文(图片)
def ImageMessage(SourceNode, TargetNode, TaskNumber, str_encode):
    # 获取下一跳地址
    routeinfo = route.GetNextNodeAddr(TargetNode)
    if routeinfo == None:
        return communication_pb2.ImageRouteReplay(recepted = False, remark = "In Node{} Have found TargetNode{} 的 next Route".format(route.SelfNodeNumber,TargetNode), ImageSign = -1)
    
    # 图片处理，调用servicer发送图像数据报文
    channel = grpc.insecure_channel(routeinfo)
    stub = communication_pb2_grpc.CommunicationStub(channel)
    ImageRouteRequst = communication_pb2.ImageRouteRequest(SourceNode = SourceNode, TargetNode = TargetNode, TaskNumber = TaskNumber, ImageInfo = str_encode)
    return stub.ImageRoute(ImageRouteRequst)

# 利用grpc的远程调用，模拟数据传送视频头报文
def VideoHeadMessage(VideoHead):
    # 获取下一跳地址
    routeinfo = route.GetNextNodeAddr(VideoHead['TargetNode'])
    if routeinfo == None:
        return communication_pb2.VideoHeadRouteReplay(recepted = False, remark = "In Node{} Have found TargetNode{} 的 next Route".format(route.SelfNodeNumber,VideoHead['TargetNode']))
    
    # 申请客户端stub
    channel = grpc.insecure_channel(routeinfo)
    stub = communication_pb2_grpc.CommunicationStub(channel)

    # 构造request请求
    VideoHeadRouteRequest = communication_pb2.VideoHeadRouteRequest()
    VideoHeadRouteRequest.SourceNode = VideoHead['SourceNode']
    VideoHeadRouteRequest.TargetNode = VideoHead['TargetNode']
    VideoHeadRouteRequest.TaskNumber = VideoHead['TaskNumber']
    VideoHeadRouteRequest.VideoFps = VideoHead['VideoFps']
    VideoHeadRouteRequest.VideoHeight = VideoHead['VideoHeight']
    VideoHeadRouteRequest.VideoWidth = VideoHead['VideoWidth']

    # 路由转发
    return stub.VideoHeadRoute(VideoHeadRouteRequest)

# 利用grpc的远程调用，模拟数据传送视频数据报文
def VideoDataMessage(TargetNode, VideoDataRouteIterator):
    # 获取下一跳地址
    routeinfo = route.GetNextNodeAddr(TargetNode)
    if routeinfo == None:
        return communication_pb2.VideoDataRouteReplay(recepted = False, remark = "In Node{} Have found TargetNode{} 的 next Route".format(route.SelfNodeNumber,TargetNode))
    
    # 路由转发
    channel = grpc.insecure_channel(routeinfo)
    stub = communication_pb2_grpc.CommunicationStub(channel)
    return stub.VideoDataRoute(VideoDataRouteIterator)

# if __name__ == '__main__':
#     QueryMessage(2)

import route
import numpy as np
import cv2
import grpc
import json
import communication_pb2_grpc
import communication_pb2
import communication_client


class CommunicationServicer(communication_pb2_grpc.CommunicationServicer):
    def __init__(self):
        print("hello world!")
        # 初始化图片序，用来标识同一任务的不同图片
        self.ImageSign = None

    # 创建路由表
    def CreateRouteTable():
        print("还没想好")

    # 同步路由表
    def SyncRouteTable():
        print("还没想好")
    
    # stream流转发
    def StreamExchange(request_iterator):
        request_first = next(request_iterator)
        
        # 第一次yield request_first是为了获取目标节点信息 
        yield request_first

        # 第二次yield开始迭代返回视频的数据
        yield request_first
        for request in request_iterator:
            yield request
            

    # 任务报文路由
    def TaskRoute(self,request,context):
        # 数据拷贝
        SourceNode = request.SourceNode
        TargetNode = request.TargetNode
        TaskNumber = request.TaskNumber

        # 如果目标节点不是本节点，则调用communication_client的TaskMessage进行路由转发
        if TargetNode != route.SelfNodeNumber:
            print("Node %d want to link Node %d, This Node is %d!\n" %(SourceNode, TargetNode, route.SelfNodeNumber))
            return communication_client.TaskMessage(SourceNode,TargetNode,TaskNumber)

        # 目标节点是本节点，则根据调度模块判断本节点是否能够进行任务TaskNumber（当前调度模块未完善，故默认返回任务请求成功）
        if TargetNode == route.SelfNodeNumber:
            return communication_pb2.TaskRouteReply(recepted = True, remark = "Ok, This Node is 空闲")

    # 图片数据报文路由
    def ImageRoute(self, request, context):
        # 数据拷贝
        TargetNode = request.TargetNode
        SourceNode = request.SourceNode
        TaskNumber = request.TaskNumber
        str_encode = request.ImageInfo
        
        # 如果目标节点不是本节点，则调用communication_client的ImageMessage函数进行路由转发
        if TargetNode != route.SelfNodeNumber:
            print("Node %d want to link Node %d, This Node is %d!\n" %(SourceNode, TargetNode, route.SelfNodeNumber))
            return communication_client.ImageMessage(SourceNode, TargetNode, TaskNumber, str_encode)
        
        # 该节点就是目标节点，保存图像到TempImages文件夹中，命名格式为SourceNode_TargetNode_TaskNumber_ImageSign.jpg
        if self.ImageSign == None:
            self.ImageSign = 0
        route.ImageDecode(str_encode, SourceNode, TargetNode, TaskNumber, self.ImageSign)
        self.ImageSign += 1

        # 报文回复
        return communication_pb2.ImageRouteReplay(recepted = True, remark = "OK! The Image already arrive!", ImageSign = (self.ImageSign -1))
    
    # 视频头报文路由
    def VideoHeadRoute(self, request, context):
        # 从request中获取数据
        VideoHead = {}
        VideoHead['SourceNode'] = request.SourceNode
        VideoHead['TargetNode'] = request.TargetNode
        VideoHead['TaskNumber'] = request.TaskNumber
        VideoHead['VideoFps'] = request.VideoFps
        VideoHead['VideoHeight'] = request.VideoHeight
        VideoHead['VideoWidth'] = request.VideoWidth


        # 目标节点不是本节点，调用communication_client的VideoHeadMessage函数进行路由转发
        if VideoHead['TargetNode'] != route.SelfNodeNumber:
            print("Node %d want to link Node %d, This Node is %d!\n" %(VideoHead['SourceNode'], VideoHead['TargetNode'], route.SelfNodeNumber))
            return communication_client.VideoHeadMessage(VideoHead)

        VideoHeadPath = './TempJsons/' + str(VideoHead['SourceNode']) + '_' + str(VideoHead['TargetNode']) + '_' + str(VideoHead['TaskNumber']) + '.json'
        # 是则转成json文件并保存在TempJsons文件夹中，命名格式为 SourceNode_TargetNode_TaskNumber.json
        with open(VideoHeadPath, 'w') as f:
            f.write(json.dumps(VideoHead, indent=4))
    
        return communication_pb2.VideoHeadRouteReplay(recepted = True, remark = "OK! The Video Head already arrive!")

    # 传递视频数据报文(使用request stream)
    def VideoDataRoute(self, request_iterator, context):
        # 重新生成yield迭代器，并额外返回第一个request，为了获取目标节点的信息
        VideoDataRouteIterator = self.StreamExchange(request_iterator)
        VideoDataRouteFirst = next(VideoDataRouteIterator)

        # 数据拷贝
        SourceNode = VideoDataRouteFirst.SourceNode
        TargetNode = VideoDataRouteFirst.TargetNode
        TaskNumber = VideoDataRouteFirst.TaskNumber

        # 该节点不是目标节点，进行路由转发
        if TargetNode != route.SelfNodeNumber:
            print("Node %d want to link Node %d, This Node is %d!\n" %( SourceNode, TargetNode, route.SelfNodeNumber))
            return communication_client.VideoDataMessage(TargetNode, VideoDataRouteIterator)

        # 从本地的Json文件中获取之前的视频头文件
        VideoHeadPath = './TempJsons/' + str(SourceNode) + '_' + str(TargetNode) + '_' + str(TaskNumber) + '.json'
        try:
            f = open(VideoHeadPath, 'rb')
        except:
            print('Not found video head json[%s] in %d' %(VideoHeadPath, route.SelfNodeNumber))
            f.close()
            return communication_pb2.VideoDataRouteReplay(recepted = False, remark = "Error: Local No Video Head Json!")

        # 根据视频头文件信息将视频帧保存在TempVideos文件夹中
        # 这里应该还要传输视频的格式、后缀名等，留待扩展
        VideoHead = json.load(f)
        VideoPath = './TempVideos/' + str(VideoHead['SourceNode']) + '_' + str(VideoHead['TargetNode']) + '_' + str(VideoHead['TaskNumber']) + '.avi'
        if route.VideoDecode(VideoPath, VideoDataRouteIterator, VideoHead['VideoFps'], (VideoHead['VideoHeight'], VideoHead['VideoWidth'])) == False:
            return communication_pb2.VideoDataRouteReplay(recepted = False, remark = "Error: Video Can't write!")

        # 路由返回报文
        return communication_pb2.VideoDataRouteReplay(recepted = True, remark = "OK: Video success arrive!")
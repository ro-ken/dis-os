import numpy as np
import cv2
import communication_pb2
import communication_pb2_grpc

# 本节点的编号
SelfNodeNumber = 3

# 路由表
route_table = {
    1:{1:'192.168.86.48:50001'}
}

# 根据目标节点查询路由表
def GetNextNodeAddr(TargetNode):
    try:
        routedict = route_table[TargetNode]
        routeinfo = routedict[list(routedict.keys())[0]]
    except:
        print("Have not found next route in RouteTable!")
        return None
    if TargetNode == SelfNodeNumber:
        print("Warning: TargetNode is SelfNode! Please check your Code")
        return None
    return routeinfo

# 地址重组为socket
def AddrCompose(ip, port):
    return str(ip) + ":" + str(port)

# socket拆分为ip和端口
def AddrAplit(addr):
    ip = addr.split(':')[0]
    port = int(addr.split(':')[1])
    return ip, port

# 图片编码为字节流
def ImageEncode(ImagePath):
    img = cv2.imread(ImagePath)
    img_encode = cv2.imencode('.jpg',img)[1]
    data_encode = np.array(img_encode)
    str_encode = data_encode.tobytes()
    return str_encode

# 图像解码为图片,保存在Templates文件夹中, 保存格式为./TempImages/(SourceNode_TargetNode_TaskNumber_ImageSign.jpg)
# ImageSgin表示图片标号，对于相同任务内传输的不同图片，使用从0开始的累加数标识图片
def ImageDecode(str_encode, SourceNode, TargetNode, TaskNumber, ImageSign):
    with open('./TempImages/' + str(SourceNode) + '_' + str(TargetNode) + '_' + str(TaskNumber) + '_' + str(ImageSign) + +'.jpg', 'wb') as f:
        f.write(str_encode)
        f.flush()

# 获取视频属性
def GetVideoAttr(VideoPath):
    # 获取视频的 VideoCapture 对象
    VideoCapture = cv2.VideoCapture(VideoPath)
    if VideoCapture.isOpened() != True:
        return None, None, None
    
    # 依次获取视频的帧率、高、宽、总帧数
    fps = int(VideoCapture.get(cv2.CAP_PROP_FPS))
    height = int(VideoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
    width = int(VideoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # count = int(VideoCapture.get(cv2.CAP_PROP_FRAME_COUNT))

    VideoCapture.release()
    return fps, height, width

# 返回视频数据的迭代器
def VideoEncode(SourceNode, TargetNode, TaskNumber, VideoPath):
    # 获取视频的 VideoCapture 对象
    VideoCapture = cv2.VideoCapture(VideoPath)
    # 避免VideoPath指向的视频文件突然删掉或改名
    if VideoCapture.isOpened() == True:
        while ret:
            ret, frame = VideoCapture.read()
            VideoDataRouteRequst = communication_pb2.VideoDataRouteRequest(SourceNode, TargetNode, TaskNumber, frame)
            yield VideoDataRouteRequst

    if VideoCapture.isOpened() == False:
        print("Error Can't open video %s in Node%d, Please checkout your video path" % (VideoPath, SelfNodeNumber))
        return None
    VideoCapture.release()

# 视频帧解码本地保存为视频
def VideoDecode(VideoName, VideoDataRouteIterator, fps, size):
    try:
        VideoWriter = cv2.VideoWriter(VideoName, cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), int(fps), (int(size[0]), int(size[1])))
        for VideoDataRouterequest in VideoDataRouteIterator:
            VideoWriter.write(VideoDataRouterequest.VideoFrame)
    except:
        print("Error: Write Video have a unknown error in Node%d" %(SelfNodeNumber))
        return False

    VideoWriter.release()
    return True

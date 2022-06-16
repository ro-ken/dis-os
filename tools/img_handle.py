import cv2
import numpy

def ImgEncode(img, img_type):
    """将图片编码为字节流

    Args:
        img: 图片
        img_type: 图片类型
    
    Returns:
        str_encode: 图片编码的字节流
    """

    encode = cv2.imencode(img_type, img)[1].tobytes()
    data_encode = np.array(encode)
    str_encode = data_encode.tobytes()
    return str_encode


def ImgDecode(str_encode):
    """将图片从字节流解码

    Args:
        str_encode: 图片编码的字节流
    
    Returns:
        img: 图片
    """

    nparr = np.frombuffer(str_encode, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def CreateVideoCapture():
    """建立并初始化一个VideoCapture用来捕获摄像头视频流
    
    Returns:
        cap: VideoCapture
    """

    # # 建立窗口, 窗口名为 'Window'
    # cv2.namedWindow('Window', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
    
    # 建立一个VideoCapture
    cap = cv2.VideoCapture(0)
    
    # 摄像头状态及属性设置
    print('摄像头是否开启: {}'.format(cap.isOpened()))  
    print(cap.get(cv2.CAP_PROP_BUFFERSIZE))    # 显示缓存数
    cap.set(cv2.CAP_PROP_BUFFERSIZE,1)         # 设置缓存区的大小
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)    #调节摄像头分辨率 1920*1080
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    print('摄像头画面高度为: {}, 宽度为: {} '.format(cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print('摄像头设置FPS: {}, FPS为:{} '.format(cap.set(cv2.CAP_PROP_FPS, 25), cap.get(cv2.CAP_PROP_FPS))) #设置FPS
    
    # # 逐帧显示捕获的视频流, 若按下 ‘q’则退出捕获
    # while(True):
    #     ret, frame = cap.read()  #第一个参数返回一个布尔值（True/False），代表有没有读取到图片；第二个参数表示截取到一帧的图片
        
    #     cv2.imshow('Window', frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # #当一切结束后，释放VideoCapture对象
    # cap.release()
    # cv2.destroyAllWindows()

    return cap

def DestroyVideoCapture(cap):
    """释放VideoCapture"""
    cap.release()


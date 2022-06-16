# import
import sys
sys.path.append("..")

# grpc
import task_pb2
import task_pb2_grpc

# img handle
from tools.img_handle import ImgEncode
from tools.img_handle import ImgDecode

# app
from app.api import APIFaceRecognition

class TaskServer(task_pb2_grpc.TaskServiceServicer):
    """grpc server远程函数调用"""
    def __init__(self):
        print("class TaskServer initial...")
    
    def task_face_recognition(self, request, context):
        """face_recoginiton remote server
        
        Args:
            request: message FaceRecognitionRequest {
                        int32 sequence = 1;
                        bytes img_orig = 2;
                        string target = 3;
                    }
        Returns:
           FaceRecognitionReplay: FaceRecognitionRequest {
                                    int32 sequence = 1;
                                    bytes img_orig = 2;
                                    string target = 3;
                                } 
        """
        # 接收并处理参数
        sequence = request.sequence
        img_orig = ImgDecode(request.img_orig, "jpg")
        target = request.target

        # 进行人脸识别, 识别结果编组发送给调用方
        success, img_out = APIFaceRecognition(img_orig, target, sequence)
        FaceRecognitionReplay = task_pb2.FaceRecognitionReplay(sequence=sequence, img_out=ImgEncode(img_out), success=success)
        return FaceRecognitionReplay

    def heartbeat(self, request, context):
        return
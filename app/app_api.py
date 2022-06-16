from .face_recognition.face_recognition import Face_Recognizer

def APIFaceRecognition(img, target_name, img_sequence):
    """人脸识别应用api

    Args:
        img: 要识别的人脸图像
        target_name: 要识别的目标
        img_sequence:图像序列号
    
    Returns:
        success: 识别是否成功
        img_out: 识别后的图像
    """


    #建立人脸识别器
    recognizer = Face_Recognizer()

    #调用人脸识别功能
    success, img_out = recognizer.face_recognition(img, target_name, img_sequence)

    return success, img_out

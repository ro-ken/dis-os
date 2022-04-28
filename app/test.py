import datetime
from datetime import time
from app_api import yolo_x

import cv2
import numpy as np
def getTime():
    return datetime.time()
cap = cv2.VideoCapture(1)
n=0
path='../pic/'

while(1):
    #print(getTime())
    ret,frame=cap.read()
    frame = cv2.resize(frame,(800,600))
    # cv2.imshow("capture",frame)
    params = []
    if (n%5==0):
        frame = yolo_x.start(frame)
        # cv2.imwrite('../pic/'+str(n)+'.jpg',frame)
        cv2.imshow("title", frame)
        # cv2.waitKey(1)
        #print(n)
    n += 1
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
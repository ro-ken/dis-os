import datetime
from datetime import time

import cv2
import numpy as np
def getTime():
    return datetime.time()
cap = cv2.VideoCapture(0)
n=0
path='../pic/'

while(1):
    #print(getTime())
    ret,frame=cap.read()
    cv2.imshow("capture",frame)
    params = []
    if (n%25==0):
        cv2.imwrite('../pic/'+str(n)+'.bmp',frame)
        #print(n)
    n += 1
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
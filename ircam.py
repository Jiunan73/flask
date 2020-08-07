import time
from base_camera5 import BaseCamera
import cv2,datetime,os

class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

    @staticmethod
    def frames():
        while True:
            datestr=datetime.datetime.now().strftime('%Y%m%d')
            b=os.listdir('static/ir_cam/'+datestr+'/AD-HF048-P-192.168.1.20');
            a=sorted(b)
           #img = [open('static/ir_cam/'+datestr+'/AD-HF048-P-192.168.1.20/'+f, 'rb').read() for f in a]
            img = open('static/ir_cam/'+datestr+'/AD-HF048-P-192.168.1.20/'+a[len(a)-2], 'rb').read()
            time.sleep(3)
            #print(int(time.time()))
            yield img

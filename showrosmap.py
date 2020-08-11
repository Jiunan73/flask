import time
from base_camera6 import BaseCamera
import cv2,random
class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    print('map_init\r\n')
    img = cv2.imread('map.png')
    print('map_start')
    mapx=0
    mapy=0
    @staticmethod
    def frames():
        while True:

	    time.sleep(1)
       	    f=open('map.txt', 'r')
	    s=f.readline()
	    f.close()
	    try:
	        k=s.split(',',2)
		print(k[0],k[1])
           
                X=int(float(k[0])*100+2048)
                Y=int(float(k[1])*100+2048)
            except:
                X=0
                Y=0
	    print(X,Y)
	    time.sleep(1)
            Camera.img=cv2.imread('map.pgm')
            cv2.rectangle(Camera.img,(X,Y),(X+80,Y+80),(255,255,0),-1)
            yield cv2.imencode('.jpg', Camera.img)[1].tobytes()

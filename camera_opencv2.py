import requests,time
from base_camera2 import BaseCamera
class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    #imgs = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]
    
    @staticmethod
    def frames():
        while True:
            r=requests.get('http://192.168.2.162/image.jpg',auth=('admin',''))

            img=r.content
	    
            yield img


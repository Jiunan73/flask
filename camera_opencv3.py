import requests,time
from base_camera3 import BaseCamera
class Camera(BaseCamera):

    
    
    @staticmethod
    def frames():
        while True:
            #r=requests.get('http://192.168.31.23/image.jpg',auth=('admin',''))
            r=requests.get('http://192.168.1.161/image/jpeg.cgi',auth=('admin',''))
            img=r.content
            
            yield img




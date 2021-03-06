import os
import cv2
from base_camera1 import BaseCamera


class Camera(BaseCamera):
    video_source = 2

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source
    @staticmethod
    def get_sensor():
        return 0 
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
    #camera.set(3,640)
    #camera.set(4.480)  
    
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()
            #print 'Camera.video_source=',Camera.video_source
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

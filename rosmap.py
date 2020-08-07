import os
import cv2



class RosMap():
    video_source = 0

    def __init__(self):

    @staticmethod
 
    def set_xy(valx,valy):
        return 0 
    @staticmethod
    def frames():
        while True:
            # read current frame
            img = cv2.imread('web1.jpg')
            #print 'Camera.video_source=',Camera.video_source
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

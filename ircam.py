import time
from base_camera5 import BaseCamera
import cv2,datetime,os

class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    filepath='1.jpg'
    @staticmethod
    def setfile(path):
	Camera.filepath=path
    @staticmethod
    def frames():
		while True:
			img= open(Camera.filepath, 'rb').read()
			yield img

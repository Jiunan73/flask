import os
import cv2
import RPi.GPIO as GPIO
import time
from base_camera import BaseCamera
trigger_pin=[17,22,9,5]
echo_pin=[27,10,11,6]
sensor_idx=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
def send_trigger_pulse(idx):
    GPIO.output(trigger_pin[idx], True)
    time.sleep(0.001)
    GPIO.output(trigger_pin[idx], False)

def wait_for_echo(idx,value, timeout):
    count = timeout
    while GPIO.input(echo_pin[idx]) != value and count > 0:
        count = count - 1

def get_distance(idx):
    send_trigger_pulse(idx)
    wait_for_echo(idx,True, 5000)
    start = time.time()
    wait_for_echo(idx,False, 5000)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len * 340 *100 /2
    return (distance_cm)

def set_video_source(source):
    print('set_video_source')
    Camera.video_source = source
class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source 
    @staticmethod
    def get_sensor(idx):
        return Camera.sensor[idx]
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
	#camera.set(3,640)
	#camera.set(4
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        loopcnt=0
        Camera.sensor=[0.0,0.0,0.0,0.0]
        sensor_str=['0.0','0.0','0.0','0.0']
        while True:
            # read current frame
            if loopcnt == 3:
                Camera.sensor[0]=get_distance(0)
                sensor_str[0]=str(round(Camera.sensor[0],1))
            elif loopcnt == 6:
                Camera.sensor[1]=get_distance(1)
                sensor_str[1]=str(round(Camera.sensor[1],1))
            elif loopcnt == 9:
                Camera.sensor[2]=get_distance(2)
                sensor_str[2]=str(round(Camera.sensor[2],1))
            elif loopcnt > 11:
                Camera.sensor[3]=get_distance(3)
                sensor_str[3]=str(round(Camera.sensor[3],1))
                loopcnt=0
            
            
            loopcnt+=1
            _, img = camera.read()
            if Camera.sensor[0] > 10:
                cv2.rectangle(img,(10,85),(80,55),(255,255,255),-1)
            else :
                cv2.rectangle(img,(10,85),(80,55),(0,0,255),-1)
                
            if Camera.sensor[1] > 10:   
                cv2.rectangle(img,(550,85),(620,55),(255,255,255),-1)
            else :
                cv2.rectangle(img,(550,85),(620,55),(0,0,255),-1)
            if Camera.sensor[2] > 10:
                cv2.rectangle(img,(10,450),(80,425),(255,255,255),-1)
            else :
                cv2.rectangle(img,(10,450),(80,425),(0,0,255),-1)
            if Camera.sensor[3] > 10:
                cv2.rectangle(img,(550,450),(620,425),(255,255,255),-1)
            else :
                cv2.rectangle(img,(550,450),(620,425),(0,0,255),-1)
            cv2.putText(img,sensor_str[0],(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(img,sensor_str[1],(550,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(img,sensor_str[2],(10,450),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(img,sensor_str[3],(550,450),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1,cv2.LINE_AA)
            
            #print 'Camera.video_source=',Camera.video_source
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

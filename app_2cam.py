#!/usr/bin/env python
from importlib import import_module
import os
import time
from flask import Flask, render_template, Response

# import camera driver
#if os.environ.get('CAMERA'):
#    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
#else:
#    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_opencv import Camera
from camera_opencv2 import Camera as Camera2
import RPi.GPIO as gpio
GOPIN=18
BACKPIN=23
LEFTPIN=24
RIGHTPIN=25
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(GOPIN, gpio.OUT)
gpio.setup(BACKPIN, gpio.OUT)
gpio.setup(LEFTPIN, gpio.OUT)
gpio.setup(RIGHTPIN, gpio.OUT)
app = Flask(__name__)


@app.route('/')
@app.route('/<cmd>')
def index(cmd=None):
    """Video streaming home page."""
    if cmd == 'go':
        setio(True, False, False, False)
    elif cmd == 'stop':
        setio(False, False, False, False)
    elif cmd == 'back':
        setio(False, True, False, False)
    elif cmd == 'right':
        setio(False, False, True, False)
    elif cmd == 'left':
        setio(False, False, False, True)
    return render_template('index.html',cmd=cmd)

def setio(p14, p15, p18, p23):
    gpio.output(GOPIN, p14)
    gpio.output(BACKPIN, p15)
    gpio.output(LEFTPIN, p18)
    gpio.output(RIGHTPIN, p23)
    """time.sleep(1)
    gpio.output(14, False)
    gpio.output(15, False)
    gpio.output(18, False)
    gpio.output(23, False)  """
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen0(camera):
    """Video streaming generator function."""
    cnt=[0,0,0,0]
    while True: 
        frame = camera.get_frame()
        for i in range(4):        
            sensor1=camera.get_sensor(i)
            if sensor1 < 10 :
                print(i)
                print ("<10cm")
                cnt[i]=cnt[i]+1
                if cnt > 10 :
                    setio(False, False, False, False)
                    cnt[i]=0
            else:
                cnt[i]=0
                
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def gen2(camera):
    """Video streaming generator function."""
    
    while True:
        frame = camera.get_frame()
        #print(camera.get_sensor())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed0')
def video_feed0():
    """Video streaming route. Put this in the src attribute of an img tag."""
    a=Camera

    print("Video streaming=",a.video_source)
    return Response(gen0(a()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed2')
def video_feed2():
    """Video streaming route. Put this in the src attribute of an img tag.""" 
    b=Camera2
    print("Video streaming=",b.video_source)
    return Response(gen2(b()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

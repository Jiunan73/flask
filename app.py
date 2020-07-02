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
from camera_pi import Camera
import RPi.GPIO as gpio
 
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(23, gpio.OUT)
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
    gpio.output(14, p14)
    gpio.output(15, p15)
    gpio.output(18, p18)
    gpio.output(23, p23)
    """time.sleep(1)
    gpio.output(14, False)
    gpio.output(15, False)
    gpio.output(18, False)
    gpio.output(23, False)  """
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

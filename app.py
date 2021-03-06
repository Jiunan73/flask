#!/usr/bin/env python
from importlib import import_module
import os
import time
from flask import Flask, render_template, Response ,jsonify, request
import datetime
# import camera driver
#if os.environ.get('CAMERA'):
#    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
#else:
#    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_opencv import Camera
from camera_opencv1 import Camera as Camera1
from camera_opencv2  import Camera as Camera2
from camera_opencv3 import Camera as Camera3
from showrosmap import Camera as rosmap
from ircam import Camera as ircam
from fallcam import Camera as fallcam
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
    print(cmd)
    if cmd == 'go' :
        setio(True, True, False, False)
    elif cmd == 'stop':
        setio(False, False, False, False)
    elif cmd == 'back':
        setio(True, False, False, False)
    elif cmd == 'right':
        setio(True, False, True, False)
    elif cmd == 'left':
        setio(True, False, False, True)
    return render_template('index.html',cmd=cmd)

def setio(p14, p15, p18, p23):
    gpio.output(GOPIN, p14)
    gpio.output(BACKPIN, p15)
    gpio.output(LEFTPIN, p18)
    gpio.output(RIGHTPIN, p23)
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
                #print(i)
                #print ("<10cm")
                cnt[i]=cnt[i]+1
                if cnt > 10 :
                    #setio(False, False, False, False)
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
def ir_gen(camera):
    """Video streaming generator function."""
    while True:
	try:
		datestr=datetime.datetime.now().strftime('%Y%m%d')
		b=os.listdir('static/ir_cam/'+datestr+'/AD-HF048-P-192.168.1.20')
		a=sorted(b)
		ir_path='static/ir_cam/'+datestr+'/AD-HF048-P-192.168.1.20/'+a[len(a)-1]
		img_file=ir_path
		t=os.stat(ir_path)
		print(t.st_ctime)
		print(time.localtime(t.st_ctime))
		b= os.listdir('static/ir_cam/fall/') 
		for s in b:
			if s.endswith('.jpg')==False:
				b.remove(s)
		a=sorted(b)
		fall_path='static/ir_cam/fall/'+a[len(a)-1]
		t=os.stat(fall_path)
		print(t.st_ctime)
		print(time.localtime(t.st_ctime))
		print time.time()
		print a[len(a)-1]
		print((t.st_ctime-time.time())/60)

		if time.time()-t.st_ctime < 60	:
			print('pelpo fall',time.time()-t.st_ctime)
			img_file=fall_path
			setio(1, 0, 0, 0 )
		time.sleep(1)
		camera.setfile(img_file)
	        frame = camera.get_frame()
	        #print(camera.get_sensor())

	        yield (b'--frame\r\n'
	               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
	except:
		print('ir error')
@app.route('/video_feed1')
def video_feed1():
    """Video streaming route. Put this in the src attribute of an img tag.""" 
    time.sleep(5)
    b=Camera1
    print("Video streaming=",b.video_source)
    return Response(gen2(b()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed2')
def video_feed2():
    time.sleep(8)
    """Video streaming route. Put this in the src attribute of an img tag.""" 
    b=Camera2
    return Response(gen2(b()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed3')
def video_feed3():
    time.sleep(10)
    """Video streaming route. Put this in the src attribute of an img tag.""" 
    b=Camera3
    return Response(gen2(b()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/Showmap')
def Showmap():
    b=rosmap
    return Response(gen2(b()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/ir_cam')
def ir_cam():
    b=ircam
    return Response(ir_gen(b()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/showfall')
def showfall():
    b=fallcam
    return Response(gen2(b()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
if __name__ == '__main__':
    setio(0, 0, 0, 0)
    app.run(host='0.0.0.0', threaded=True)

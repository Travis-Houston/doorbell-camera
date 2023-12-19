from flask import Flask, render_template, Response, request
from RemoteCamera import VidCamera
import time
import threading
from timeit import default_timer as timer
import os
import RPi.GPIO as GPIO
import subprocess
from datetime import datetime

#flip if camera is upside down
piCamera = VidCamera(flip=False)

state = False

# CHANGME Change variables depending on your situation
url = "https://discord.com/api/webhooks/1183288853650477116/F_efA77TF_Mjbg_FdmegWmAXkV_TloVB7r7zUjkmJkLfxMuei0X5LO2ZjDCtjfOz-BEv"
ip_address = subprocess.getoutput('hostname -I')
camURL = "http://" + ip_address.strip() + ":5000/"

# Flask
app = Flask(__name__)

startTimer = timer()
endTimer = 0

#background process
@app.route('/lock')
def lock():
    print("Locked!")
    os.system("python servo.py 1 2 0.4 1")
    return ("nothing")

@app.route('/unlock')
def unlock():
    print("Unlocked!")
    os.system("python servo.py 89 90 0.3 1")   
    return ("nothing")

@app.route('/', methods = ['GET', 'POST'])
def move():
    result = ""
    if request.method == 'POST':
        return render_template('index.html', res_str=result)
    return render_template('index.html')  # Render the index.html template

def gen(camera):
    # Camera frame generator
    while True:
        frame = camera.getFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(piCamera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/picture')
def take_picture():
    piCamera.takePic()
    return "None"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

button_pressed = False  # Flag to track the button state

@app.route('/button')    
def button_callback(channel):
    
    state = GPIO.input(channel)
    
    if(state == 1):
        now = datetime.now()
        webhook = "Someone is knocking your door at {}: {}".format(now, camURL)
        subprocess.Popen(['/home/pi/Desktop/BellCamera2/webhookdiscord.sh', webhook], stdout=subprocess.DEVNULL)
        print("button pushed")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(13, GPIO.RISING, callback=button_callback)

#Button testing (Still in progress)
"""
@app.route('/button')
def button_callback(channel):
    state = GPIO.input(13)
    
    if state == False and not button_pressed: # Assuming GPIO.HIGH represents button pressed
        now = datetime.now()
        webhook = "Someone is at your door: '{}'".format(camURL)
        subprocess.Popen(['/home/pi/Desktop/BellCamera2/webhookdiscord.sh', webhook], stdout=subprocess.DEVNULL)
        print("Button pushed")
        button_pressed = True
    
    if state == True:
        button_pressed = False    
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

from flask import Flask, render_template, Response, request
from RemoteCamera import VidCamera
import time
import threading
import os

#flip if camera is upside down
piCamera = VidCamera(flip=False)

# Flask
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
    

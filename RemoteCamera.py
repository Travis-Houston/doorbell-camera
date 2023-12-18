import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np
import os

#define haarcascade variable
haar_cascade=cv.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6

class VidCamera(object):
    def __init__(self, flip = False, fileType = ".jpg", photoString = "stream_photo"):
        self.vs = cv.VideoCapture(0)
        self.flip = flip                #Vertical frame flip
        self.fileType = fileType        #img type
        self.photoString = photoString  #Photo name
        
    def __del__(self):
        self.vs.release()
        
    def flipRequired(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame
    
    def getFrame(self):
        #Iterating over each frame
        stream, image = self.vs.read()
        image=cv.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv.INTER_AREA)
        gray=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        obect_rects=haar_cascade.detectMultiScale(gray,1.3,5)
 
        for (x,y,w,h) in obect_rects:
            cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            break
        #OpenCV video capture to JPEG -> to main.py
        ret, jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def takePic(self):
        ret, frame = self.vs.read()
        frame = self.flipRequired(frame)
        # Current time
        todayDate = datetime.now().strftime("%m%d%Y-%H%M%S")
        photo_path = os.path.join("/home/pi/Desktop/bellcamera/picture", f"{self.photoString}_{todayDate}{self.fileType}")
        cv.imwrite(photo_path, frame)
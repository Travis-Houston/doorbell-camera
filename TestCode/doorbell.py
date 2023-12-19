import os
import subprocess
import RPi.GPIO as GPIO
import time
from timeit import default_timer as timer
from datetime import datetime

status = False

startCommand = 'wget -O- http://localhost:7999/1/detection/start'
pauseCommand = 'wget -O- http://localhost:7999/1/detection/pause'

# CHANGME Change variables depending on your situation
url = "https://discord.com/api/webhooks/1183288853650477116/F_efA77TF_Mjbg_FdmegWmAXkV_TloVB7r7zUjkmJkLfxMuei0X5LO2ZjDCtjfOz-BEv"
camURL = "http://192.168.0.126:9081/"

startTimer = timer()
endTimer = 0

#waiting time until next button detection
timeThreshold = 30
recordTime = 30
isRecording = False

#wait 30sec before starting to allow camera initialization
time.sleep(30)

process = subprocess.Popen(pauseCommand.split(), stdout=subprocess.DEVNULL)

def button_callback(channel):
    status = GPIO.input(channel)
    
    global isRecording
    global startTimer
    global endTimer
    
    #Stop detecting button input when camera is in progress
    if not isRecording:
        if status == 0:
            if endTimer == 0:
                endTimer = timer() + 30
            else:
                endTimer = timer()
                
            if endTimer - startTimer >= timeThreshold:
                now = datetime.now()
                process = subprocess.Popen(startCommand.split(), stdout=subprocess.DEVNULL)
                webhook = "Someone is at your door: '{}'".format(camURL)
                subprocess.Popen(['/home/pi/Desktop/OtherProjects/Doorbell/webhookdiscord.sh', webhook], stdout=subprocess.DEVNULL)
                
                subprocess.Popen(['/home/pi/Desktop/OtherProjects/Doorbell/playdoorbellsound.sh'], stdout=subprocess.DEVNULL)
                startTimer = timer()
                isRecording = True

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(13, GPIO.FALLING, callback=button_callback)

#wait for button input 
while True:
    if isRecording:
        currentTime = timer()
        
        #stop recording after awhile of record time
        if currentTime - startTimer >= recordTime:
            process = subprocess.Popen(pauseCommand.split(), stdout=subprocess.DEVNULL)
            isRecording = False
        
        time.sleep(0.25)
        
    GPIO.cleanup
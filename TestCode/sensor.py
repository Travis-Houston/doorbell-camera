"""
import RPi.GPIO as GPIO

state = False

def button_callback(channel):
    
    state = GPIO.input(channel)
    
    if(state == 1):
        print("Button was pushed")
    else:
        print("button released!")
        
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(13, GPIO.BOTH, callback=button_callback)
message = input("Press enter to exit\n\n")
GPIO.cleanup()
"""
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_pressed = False  # Flag to track the button state

while True:
    input_state = GPIO.input(13)

    if input_state == False and not button_pressed:
        button_pressed = True
        print('Button Pressed')
        time.sleep(0.2)

    if input_state == True:
        button_pressed = False
# OpenCV smart doorbell

A simple doorbell camera utilizes openCV and servo to Lock/Unlock doors.

## Description

This is one of my starting projects for a smart doorbell system using OpenCV and raspberry pi. I plan to expand my project with a touchpad that will trigger a speaker as a doorbell and fix face detection in the future.
For now, The project consists of just a camera, a servo, a touch sensor, and a Raspberry Pi 3:
* When the sensor is touched, it will send a discord webhook message to your discord server.
* A flask Website that shows the camera with features like: taking images, unlocking/ locking the door with a servo.

## How it works
The output of the camera module (which is the live video) will be streamed through Flask. Through the same network, all devices will be able to see these outputs through a webpage:
```
<your raspberry pi IP:5000>
 ```

## Dependencies

You can just install the following dependencies to create a camera stream.

```
sudo apt-get update 
sudo apt-get upgrade

sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test
sudo apt-get install libhdf5-dev

sudo pip3 install flask
sudo pip3 install numpy
sudo pip3 install opencv-contrib-python
sudo pip3 install imutils
sudo pip3 install opencv-python
```

## Installing

If you want to try, clone this repository through:
```
git clone https://github.com/Travis-Houston/doorbell-camera.git
```
## Executing program

* Install the code through cloning in github (note that all of the files and dependencies should be downloaded so that it could work properly)
* Run the code through this command:
```
sudo python3 your_path_to_project/Main.cpp
```

## Authors

### Travis Houston (Huynh Nguyen Quoc Bao):
* Phone: 0707191380
* Email: baohnq2003@gmail.com

## Acknowledgments


* [Pi-Smart-Doorbell](https://github.com/EbenKouao/Pi-Smart-Doorbell.git)
* [pi-camera-stream-flask](https://github.com/EbenKouao/pi-camera-stream-flask)

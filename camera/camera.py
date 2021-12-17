from picamera import PiCamera
from time import sleep
from datetime import datetime

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.zoom= (0.25, 0.25, 0.5, 0.5)
camera.framerate = 15
camera.brightness = 50
sleep(5)#Has to be at least two seconds as to let the camera adjust to light levels 
now = datetime.now()
timestamp = now.strftime("%m-%d-%Y_%H-%M-%S")
camera.capture('/home/pi/rover/camera/spectra/img%s.jpg' % timestamp)
print(f"Picture taken at {timestamp}")
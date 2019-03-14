from time import sleep
from picamera import PiCamera
import keyboard
from datetime import datetime, timedelta

n = 1
camera = PiCamera()
# camera.resolution = (1920,1080)
camera.resolution = (3280,2464)
camera.start_preview(fullscreen=False,window=(900,100,1000,700))
# Camera warm-up time
while True:
    if keyboard.is_pressed('q'):
        print('exit!')
        break
    if keyboard.is_pressed('c'):
        camera.stop_preview()
        # print('capture!')
        #  camera.resolution = (3280,2464)
        filename = 'image'+str(n).zfill(2)+'.jpg'
        n = n+1
        camera.capture(filename)
        camera.start_preview(fullscreen=False,window=(900,100,1000,700))
        # camera.resolution = (1920,1080) 
        # sleep(1)
# sleep(2)
# camera.capture('foo.jpg')

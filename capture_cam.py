from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (2592,1944)
camera.shutter_speed = 7500
camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = 1
camera.start_preview()
# Camera warm-up time
# sleep(2)
camera.capture('foo.jpg')

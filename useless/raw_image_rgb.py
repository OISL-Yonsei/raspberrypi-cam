import time
from picamera  import PiCamera
import io
import picamera.array
import numpy as np
import cv2
import sys

camera = PiCamera()
camera.resolution = camera.MAX_RESOLUTION
time.sleep(1)
camera.shutter_speed = int(sys.argv[1])
camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = 1
time.sleep(1)

print(camera.exposure_speed)

with picamera.array.PiRGBArray(camera) as pirgb:
	camera.capture(pirgb, 'rgb')
	image = pirgb.array
	timestr = time.strftime("%Y%m%d_%H%M%S");
	np.save("captured_rgb_"+timestr,image)
	print("image saved") 
	pirgb.truncate(0)

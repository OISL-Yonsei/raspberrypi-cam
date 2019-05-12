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
        
output = picamera.array.PiBayerArray(camera)
camera.capture(output,format='jpeg',bayer=True)
print(output.array.shape)
output2 = output.array
timestr = time.strftime("%Y%m%d_%H%M%S");
np.save("captured_bayer_"+timestr,output2)
print("npy saved")
output.truncate(0)

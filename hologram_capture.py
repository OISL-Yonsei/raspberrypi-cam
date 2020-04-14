##################################
# @author Lukael
# @email lukael.jung@gmail.com
# @create date 2019-07-26 11:41:07
# @modify date 2019-07-26 11:41:07
##################################
import numpy as np
import picamera
import picamera.array 
from picamera import mmal, mmalobj, exc
from picamera.mmalobj import to_rational
import cv2
import time


MMAL_PARAMETER_ANALOG_GAIN = mmal.MMAL_PARAMETER_GROUP_CAMERA + 0x59
MMAL_PARAMETER_DIGITAL_GAIN = mmal.MMAL_PARAMETER_GROUP_CAMERA + 0x5A

def set_gain(camera, gain, value):
    """Set the analog gain of a PiCamera.
    
    camera: the picamera.PiCamera() instance you are configuring
    gain: either MMAL_PARAMETER_ANALOG_GAIN or MMAL_PARAMETER_DIGITAL_GAIN
    value: a numeric value that can be converted to a rational number.
    """
    if gain not in [MMAL_PARAMETER_ANALOG_GAIN, MMAL_PARAMETER_DIGITAL_GAIN]:
        raise ValueError("The gain parameter was not valid")
    ret = mmal.mmal_port_parameter_set_rational(camera._camera.control._port, gain, to_rational(value))
    if ret == 4:
        raise exc.PiCameraMMALError(ret, "Are you running the latest version of the userland libraries? Gain setting was introduced in late 2017.")
    elif ret != 0:
        raise exc.PiCameraMMALError(ret)

def set_analog_gain(camera, value):
    """Set the gain of a PiCamera object to a given value."""
    set_gain(camera, MMAL_PARAMETER_ANALOG_GAIN, value)

def set_digital_gain(camera, value):
    """Set the digital gain of a PiCamera object to a given value."""
    set_gain(camera, MMAL_PARAMETER_DIGITAL_GAIN, value)


picam = picamera.PiCamera()
time.sleep(0.5)
picam.resolution = (1640,1232)
# picam.resolution = picam.MAX_RESOLUTION
# picam.shutter_speed = 100
# picam.framerate = 30  
picam.shutter_speed = 50
# picam.iso = 100
# Wait for the automatic gain control to settle
time.sleep(2)
picam.exposure_mode = 'off'
picam.shutter_speed = picam.exposure_speed

print(picam.shutter_speed)

picam.awb_mode = 'off'
picam.awb_gains = (1,1)

set_analog_gain(picam, 1)
set_digital_gain(picam, 1)

time.sleep(2)

print(picam._get_analog_gain())
print(picam._get_digital_gain()) 
# pibgr = picamera.array.PiRGBArray(picam, size=(1640,1232))
pibgr = picamera.array.PiRGBArray(picam)
time.sleep(0.5)
sizex = 640
sizey = 480
# sizex = 1920
# sizey = 1080
image = []
while (True):
    picam.resolution = (1640,1232)
    # picam.resolution = (640,480)
    # picam.capture(pibgr, "bgr", use_video_port = "True")
    picam.capture(pibgr, "bgr")
    frame = pibgr.array
    (h, w) = frame.shape[:2]
    frame_small = cv2.resize(frame, (sizex,sizey))
    frame_b, frame_g, frame_r = cv2.split(frame_small)
    frame_concat = np.hstack((frame_r, frame_g))
    cv2.imshow("live", frame_g)
    cv2.moveWindow("live",0,0)
    # cv2.imshow("live", frame_r)
    key = cv2.waitKey(1) & 0xFF
    pibgr.truncate(0)

    if key == ord("q"):  #exit
        break;

    if key == ord("w"): #decrease exposuretime
        current_shutter_speed = picam.exposure_speed
        picam.shutter_speed = np.max([5, current_shutter_speed-50])
        print("current: ", + current_shutter_speed, " new: ", picam.shutter_speed)

    if key == ord("e"): #increase exposure time
        current_shutter_speed = picam.exposure_speed
        picam.shutter_speed = np.min([5000, current_shutter_speed+100])
        print("current: ", current_shutter_speed, " new: ", picam.shutter_speed)

    if key == ord("s"): #save image
        picam.resolution = picam.MAX_RESOLUTION
        picam.capture(pibgr, "bgr")
        image = pibgr.array
        timestr = time.strftime("%Y%m%d_%H%M%S");
        filename = "captured_bgr_{}.tiff".format(timestr)
        cv2.imwrite(filename, image)
        print("[INFO] saved {}".format(filename))
        pibgr.truncate(0)

    if key == ord("b"): #save bayer
        pibayer = picamera.array.PiBayerArray(picam)
        picam.capture(pibayer, "jpeg", bayer = "True")
        image = pibayer.array
        # bayer_image = image.sum(axis=2)
        # print(bayer_image.shape)
        timestr = time.strftime("%Y%m%d_%H%M%S");
        filename = "captured_bayer_{}.tiff".format(timestr)
        cv2.imwrite(filename, image)
        print("[INFO] saved {}".format(filename))
        pibayer.truncate(0)

    if key == ord("d"): #save multiple x20 image
        for i in range(1,21):
        # for i in range(1,101):
            picam.resolution = picam.MAX_RESOLUTION
            print(picam._get_analog_gain())
            print(picam._get_digital_gain())
            picam.capture(pibgr, "bgr")
            image = pibgr.array
            timestr = time.strftime("%Y%m%d_%H%M%S");
            filename = "captured_bgr_{}.tiff".format(timestr)
            cv2.imwrite(filename, image)
            print("[INFO] {} saved {}".format(i,filename))
            pibgr.truncate(0)
        print("[INFO] Finish!")

    if key == ord("v"): #save bayer multiple x20 image
        for i in range(1,11):
            pibayer = picamera.array.PiBayerArray(picam)
            # print("\033[36m[INFO] Current analog/digital gains : {}, {}".format(round(float(picam.analog_gain), 4),round(float(picam.digital_gain), 4)))
            print(picam._get_analog_gain())
            print(picam._get_digital_gain())
            picam.capture(pibayer, "jpeg", bayer = "True")
            image = pibayer.array
            timestr = time.strftime("%Y%m%d_%H%M%S");
            filename = "captured_bayer_{}.tiff".format(timestr)
            cv2.imwrite(filename, image)
            print("[INFO] {} saved {}".format(i,filename))
            pibayer.truncate(0)
        print("[INFO] Finish!")

cv2.destroyAllWindows()

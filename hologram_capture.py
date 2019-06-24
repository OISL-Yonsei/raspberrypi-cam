import numpy as np
import picamera
import picamera.array 
import cv2
import time

picam = picamera.PiCamera()
time.sleep(0.5)
picam.resolution = (1640,1232)
# picam.resolution = picam.MAX_RESOLUTION
picam.shutter_speed = 100
picam.framerate = 30
time.sleep(2)
picam.exposure_mode = 'off'
picam.shutter_speed = picam.exposure_speed;
print(picam.exposure_speed)
picam.awb_mode = 'off'
picam.awb_gains = (1,1)
picam.iso = 100
# pibgr = picamera.array.PiRGBArray(picam, size=(1640,1232))
pibgr = picamera.array.PiRGBArray(picam)
time.sleep(0.5)
sizex = 640
sizey = 480
image = []
while (True):
    picam.resolution = (1640,1232)
    picam.capture(pibgr, "bgr", use_video_port = "True")
    frame = pibgr.array
    (h, w) = frame.shape[:2]
    frame_small = cv2.resize(frame, (sizex,sizey))
    frame_b, frame_g, frame_r = cv2.split(frame_small)
    frame_concat = np.hstack((frame_r, frame_g))
    cv2.imshow("live", frame_concat)
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
            picam.resolution = picam.MAX_RESOLUTION
            picam.capture(pibgr, "bgr")
            image = pibgr.array
            timestr = time.strftime("%Y%m%d_%H%M%S");
            filename = "captured_bgr_{}.tiff".format(timestr)
            cv2.imwrite(filename, image)
            print("[INFO] saved {}".format(filename))
            pibgr.truncate(0)

    if key == ord("v"): #save bayer multiple x20 image
        for i in range(1,21):
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

cv2.destroyAllWindows()

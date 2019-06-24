from __future__ import print_function
from PIL import Image, ImageTk
import tkinter as tki
import threading
import cv2
import os, time
import picamera
import picamera.array 

class MicroscopeApp:
    def __init__(self, picam, pibgr):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.picam = picam
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.pibgr = pibgr

        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None
        
        # create a button, that when pressed, will take the current
        # frame and save it to file
        btn = tki.Button(self.root, text="Snapshot!", command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
 
        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
 
        # set a callback to handle when the window is closed
        self.root.wm_title("Microscope imaging")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        while not self.stopEvent.is_set():
            # grab the frame from the video stream and resize it
            self.picam.capture(self.pibgr, "bgr", use_video_port = "True")
            self.frame = self.pibgr.array
            frame_small = cv2.resize(self.frame, (420,300))
            
            # clear buffer(if not it occurs incorrect error)
            self.pibgr.truncate(0)
            
            image = Image.fromarray(frame_small)
            image = ImageTk.PhotoImage(image)

            # if the panel is not None, we need to initialize it
            if self.panel is None:
                self.panel = tki.Label(image=image)
                self.panel.image = image
                self.panel.pack(side="left", padx=10, pady=10)
            
            # otherwise, simply update the panel
            else:
                self.panel.configure(image=image)
                self.panel.image = image 

    def takeSnapshot(self):
        timestr = time.strftime("%Y%m%d_%H%M%S");
        filename = "microscope_{}.tiff".format(timestr)
        cv2.imwrite(filename, self.frame)
        print("[INFO] saved {}".format(filename))

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()  
        self.root.quit()    

if __name__ == '__main__':
    
    # initialize the video stream and allow the camera sensor to warmup
    print("[INFO] warming up camera...")
    picam = picamera.PiCamera()
    time.sleep(0.5)
    picam.resolution = (1640,1232)
    time.sleep(2)
    pibgr = picamera.array.PiRGBArray(picam)
    time.sleep(0.5)

    # start the app
    pba = MicroscopeApp(picam,pibgr)
    pba.root.mainloop()
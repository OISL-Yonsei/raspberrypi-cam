import sys, os
from time import sleep
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QGridLayout, QCheckBox)
from PyQt5.QtCore import Qt


class CameraApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.recording_flag = 0
        self.start_flag = 0


        # Button initialize
        ############################### 
        self.cap_button = QPushButton('Capture(c)', self)
        self.cap_button.setToolTip("This is a Capture button")
        
        self.rec_button = QPushButton('Record(v)', self)
        self.rec_button.setToolTip("This is a Record button")
        
        self.start_button = QPushButton('Start(s)', self)
        self.start_button.setToolTip("This is a Start Button")
        

        # Setting value initialize
        ############################### 
        # shutter speed, awb gain, image name(prefix, suffix), file format, ISO
        shutter_label = QLabel('Shutter speed', self)
        self.shutter_value = QLineEdit(self)
        shutter_label.setAlignment(Qt.AlignCenter)
        shutter_auto = QCheckBox(self)
        shutter_auto.toggle()

        image_prefix_label = QLabel('Image name', self)
        self.image_prefix = QLineEdit(self)
        image_prefix_label.setAlignment(Qt.AlignCenter)

        iso_label = QLabel('ISO', self)
        self.iso_value = QLineEdit(self)
        iso_label.setAlignment(Qt.AlignCenter)
        iso_auto = QCheckBox(self)
        iso_auto.toggle()
        
        gain_label = QLabel('Gain(awb)', self)
        self.gain_value = QLineEdit(self)
        gain_label.setAlignment(Qt.AlignCenter)
        gain_auto = QCheckBox(self)
        gain_auto.toggle()
        
        auto_label = QLabel('Auto',self)
        auto_label.setAlignment(Qt.AlignCenter)
        

        # Window Layout
        #######################################
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(auto_label, 0, 2)
        grid.addWidget(image_prefix_label, 1, 0)
        grid.addWidget(shutter_label, 2, 0)
        grid.addWidget(iso_label, 3, 0)
        grid.addWidget(gain_label, 4, 0)

        grid.addWidget(self.image_prefix, 1, 1)
        grid.addWidget(self.shutter_value, 2, 1)
        grid.addWidget(self.iso_value, 3, 1)
        grid.addWidget(self.gain_value, 4, 1)

        grid.addWidget(shutter_auto, 2, 2)
        grid.addWidget(iso_auto, 3, 2)
        grid.addWidget(gain_auto, 4, 2)

        grid.addWidget(self.cap_button, 5, 0)
        grid.addWidget(self.rec_button, 5, 1)
        grid.addWidget(self.start_button, 5, 2)
        
        # hbox_button = QHBoxLayout()
        # hbox_button.addWidget(self.cap_button)
        # hbox_button.addWidget(self.rec_button)
        # hbox_button.addWidget(self.start_button)

        # hbox_shutter = QHBoxLayout()
        # hbox_shutter.addWidget(shutter_label)
        # hbox_shutter.addWidget(self.shutter_value)

        # hbox_image = QHBoxLayout()
        # hbox_image.addWidget(image_prefix_label)
        # hbox_image.addWidget(self.image_prefix)

        # hbox_iso = QHBoxLayout()
        # hbox_iso.addWidget(iso_label)
        # hbox_iso.addWidget(self.iso_value)

        # hbox_gain = QHBoxLayout()
        # hbox_gain.addWidget(gain_label)
        # hbox_gain.addWidget(self.gain_value)
        
        # vbox = QVBoxLayout()
        # vbox.addLayout(hbox_shutter)
        # vbox.addLayout(hbox_image)
        # vbox.addLayout(hbox_iso)
        # vbox.addLayout(hbox_gain)
        # vbox.addStretch(4)
        # vbox.addLayout(hbox_button)
        # vbox.addStretch(0.5)
        # self.setLayout(vbox)


        # Connection funtion
        #############################################
        self.cap_button.clicked.connect(self.capture)
        self.rec_button.clicked.connect(self.record)
        self.start_button.clicked.connect(self.setting)

        self.setWindowTitle('Raspberry-pi Camera')
        self.move(1000, 200)
        self.show()


    def capture(self):
        print('Capture Complete')
    

    def record(self):
        if self.recording_flag == 0:
            print('Start Recording')
            self.rec_button.setText('Stop(v)')
            self.recording_flag = 1
        else:
            print('Stop Recording')
            self.rec_button.setText('Record(v)')
            self.recording_flag = 0
        

    def setting(self):
        if self.start_flag == 0:
            self.start_button.setText('Setting(s)')
            self.start_flag = 1



    # keyboard interrupt
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape: # esc = close window
            self.close()
        elif e.key() == Qt.Key_C: # c = capture image
            self.capture()
        elif e.key() == Qt.Key_V: # v = recoding video
            self.record()
        elif e.key() == Qt.Key_S: # s = Set the setting value
            self.setting()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = CameraApp()
    sys.exit(app.exec_())
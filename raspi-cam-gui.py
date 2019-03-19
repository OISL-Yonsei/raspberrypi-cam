import sys
from time import sleep
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit)
from PyQt5.QtCore import Qt


class CameraApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        self.recording_flag = 0

        self.cap_button = QPushButton('Capture(c)', self)
        self.cap_button.setToolTip("This is a Capture button")
        
        self.rec_button = QPushButton('Record(v)', self)
        self.rec_button.setToolTip("This is a Record button")
        
        self.set_button = QPushButton('Setting(s)', self)
        self.set_button.setToolTip("This is a set button. Press when settings are complete.")
        

        # shutter speed, awb gain, image name(prefix, suffix), file format
        shutter_label = QLabel('Shutter speed', self)
        self.shutter_value = QLineEdit(self)
        self.shutter_value.move(60, 100)
        
        # Button Layout
        hbox_button = QHBoxLayout()
        # hbox.addStretch(1)
        hbox_button.addWidget(self.cap_button)
        hbox_button.addWidget(self.rec_button)
        hbox_button.addWidget(self.set_button)
        # hbox.addStretch(1)

        hbox_shutter = QHBoxLayout()
        hbox_shutter.addWidget(shutter_label)
        hbox_shutter.addWidget(self.shutter_value)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_shutter)
        vbox.addStretch(4)
        vbox.addLayout(hbox_button)
        vbox.addStretch(0.5)
        self.setLayout(vbox)

        self.cap_button.clicked.connect(self.capture)
        self.rec_button.clicked.connect(self.record)
        self.set_button.clicked.connect(self.setting)

        self.setWindowTitle('Raspberry-pi Camera')
        self.setGeometry(1000, 200, 500, 700)
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
        test = self.shutter_value.text()
        print(test)


    def keyPressEvent(self, e): # keyboard interrupt

        if e.key() == Qt.Key_Escape: # esc = close window
            self.close()
        elif e.key() == Qt.Key_C: # c = capture image
            self.showFullScreen()
        elif e.key() == Qt.Key_V: # v = recoding video
            self.showNormal()
        elif e.key() == Qt.Key_S: # s = Set the setting value
            self.setting()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = CameraApp()
    sys.exit(app.exec_())
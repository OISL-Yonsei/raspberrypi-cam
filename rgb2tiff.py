import numpy as np
import os
import cv2
from matplotlib import pyplot as plt

path = os.getcwd()

for filename in os.listdir(path):
    npy = np.load(filename)
    BGR = cv2.cvtColor(npy, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename[:-4]+'.tiff', BGR)

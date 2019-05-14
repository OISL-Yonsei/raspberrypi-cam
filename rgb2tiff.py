import numpy as np
import os
import cv2
from matplotlib import pyplot as plt
from glob import glob

path = os.getcwd()

numpy_list = list()
for numpy_name in glob('*.npy'):
    numpy_list.append(numpy_name)

for filename in numpy_list:
    npy = np.load(filename)
    BGR = cv2.cvtColor(npy, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename[:-4]+'.tiff', BGR)
    print(filename + " converting end")

os.system("Pause")
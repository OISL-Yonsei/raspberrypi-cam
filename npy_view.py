import numpy as np
import os
import cv2
from matplotlib import pyplot as plt
import sys

npy = np.load(sys.argv[1]+'.npy')
print(npy.shape)

plt.figure()
plt.imshow(npy[:,:,0])
plt.figure()
plt.imshow(npy[:,:,1])
plt.figure()
plt.imshow(npy[:,:,2])
plt.figure()
plt.imshow(npy)

plt.show()

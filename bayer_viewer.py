import numpy as np
import os
import cv2
from matplotlib import pyplot as plt
import sys

npy = np.load(sys.argv[1]+'.npy')
print(npy.shape)
r = npy[1::2,1::2,0]
g1 = npy[0::2,1::2,1]
g2 = npy[1::2,0::2,1]
b = npy[0::2,0::2,2]
RGB = np.dstack((r, g2, b))[:, :, :]
bayer_layer = npy.sum(axis=2)
print(bayer_layer)

plt.figure()
plt.imshow(r)
plt.figure()
plt.imshow(g1)
plt.figure()
plt.imshow(g2)
plt.figure()
plt.imshow(b)
plt.figure()
plt.imshow(RGB)
plt.figure()
plt.imshow(bayer_layer)

plt.show()
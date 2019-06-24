import numpy as np
import os
import cv2

filename = "rgbyuv_colorful.data"
width = 3280
height = 2464
fwidth = (width + 31) // 32 * 32
fheight = (height + 15) // 16 * 16
f = open(filename)
# Load the Y (luminance) data from the stream
Y = np.fromfile(f, dtype=np.uint8, count=fwidth*fheight).\
        reshape((fheight, fwidth))
# Load the UV (chrominance) data from the stream, and double its size
f.seek(fwidth*fheight, os.SEEK_SET)
U = np.fromfile(f, dtype=np.uint8, count=(fwidth//2)*(fheight//2)).\
        reshape((fheight//2, fwidth//2)).\
        repeat(2, axis=0).repeat(2, axis=1)
f.seek(fwidth*fheight+(fwidth//2)*(fheight//2), os.SEEK_SET)
V = np.fromfile(f, dtype=np.uint8, count=(fwidth//2)*(fheight//2)).\
        reshape((fheight//2, fwidth//2)).\
        repeat(2, axis=0).repeat(2, axis=1)
# Stack the YUV channels together, crop the actual resolution, convert to
# floating point for later calculations, and apply the standard biases
YUV = np.dstack((Y, U, V))[:height, :width, :].astype(np.float)
YUV[:, :, 0]  = YUV[:, :, 0]  - 16   # Offset Y by 16
YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
# YUV conversion matrix from ITU-R BT.601 version (SDTV)
#              Y       U       V
M = np.array([[1.164,  0.000,  1.596],    # R
              [1.164, -0.392, -0.813],    # G
              [1.164,  2.017,  0.000]])   # B
# Take the dot product with the matrix to produce RGB output, clamp the
# results to byte range and convert to bytes
RGB = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
# Translate RGB to BGR
BGR = cv2.cvtColor(RGB, cv2.COLOR_RGB2BGR)
cv2.imwrite(filename[:-4]+'tiff', BGR)

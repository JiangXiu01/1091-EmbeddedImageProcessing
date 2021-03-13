import cv2
import numpy as np


def olbp(src):
    dst = np.zeros(src.shape,dtype=src.dtype)
    for i in range(1,src.shape[0]-1):
        for j in range(1,src.shape[1]-1):
            pass
            center = src[i][j]
            code = 0;
            code |= (src[i-1][j-1] >= center) << 7;
            code |= (src[i-1][j  ] >= center) << 6;
            code |= (src[i-1][j+1] >= center) << 5;
            code |= (src[i  ][j+1] >= center) << 4;
            code |= (src[i+1][j+1] >= center) << 3;
            code |= (src[i+1][j  ] >= center) << 2;
            code |= (src[i+1][j-1] >= center) << 1;
            code |= (src[i  ][j-1] >= center) << 0;

            dst[i-1][j-1]= code;
    return dst


lena = cv2.imread('road_orign.jpg')
'''
cv2.namedWindow('lena')
cv2.imshow('lena', lena)
cv2.waitKey(0)
'''
gray = cv2.cvtColor(lena,cv2.COLOR_RGB2GRAY)
x = olbp(gray)

cv2.namedWindow('olbp')
cv2.imshow('olbp', x)
cv2.waitKey(0)
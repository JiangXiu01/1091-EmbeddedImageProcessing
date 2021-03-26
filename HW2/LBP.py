#Local Binary Pattern (LBP)
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

def LBP(src):
    dst = np.zeros(src.shape, dtype=src.dtype)
    print('影像大小(x,y):', src.shape[0], 'x', src.shape[1])
    for i in range(1,src.shape[0]-1): #逐行掃描
        for j in range(1, src.shape[1]-1): #逐列掃描
            pass
            center = src[i][j] #中間值 [i  ,j  ]
            code = 0;
            '''
            print('i:',i, ' j:', j, '   src[i][j]:', center)
            print(src[i-1][j+1],'  ', src[i][j+1],'  ', src[i+1][j+1])
            print(src[i-1][j],'  ', src[i][j],'  ', src[i+1][j])
            print(src[i-1][j-1],'  ', src[i][j-1],'  ', src[i+1][j-1])
            '''
            #time.sleep(1)
            #[i-1 ,j+1] [i  ,j+1] [i+1 ,j+1]
            #[i-1 ,j  ] [i  ,j  ] [i+1 ,j  ]
            #[i-1 ,j-1] [i  ,j-1] [i+1 ,j-1]
            # 2^0  2^1  2^2
            # 2^3  2^4  2^5
            # 2^6  2^7  2^8
            code |= (src[i-1][j+1] >= center) << 0;
            code |= (src[i  ][j+1] >= center) << 1;
            code |= (src[i+1][j+1] >= center) << 2;
            code |= (src[i-1][j  ] >= center) << 3;
            code |= (src[i+1][j  ] >= center) << 4;
            code |= (src[i-1][j-1] >= center) << 5;
            code |= (src[i  ][j-1] >= center) << 6;
            code |= (src[i+1][j-1] >= center) << 7;

            #print('code==> ', code)
            dst[i-1][j-1]= code;
    return dst

img = cv2.imread('road_orign.jpg') #讀取圖檔
'''
cv2.namedWindow('img')
cv2.imshow('img', img)
cv2.waitKey(0)
'''
img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #轉為灰階
img_LBP = LBP(img_gray)

Hist = cv2.calcHist([img_LBP], [0], None, [256], [0,256]) #cv2.calcHist(影像, 通道, 遮罩, 區間數量, 數值範圍)
#灰階影像==> 通道指定: [0]
#彩色影像==> [0], [1], [2] 指定藍色, 綠色, 紅色的通道
plt.plot(Hist)
plt.show()

cv2.namedWindow('img_LBP')
cv2.imshow('img_LBP', img_LBP)
cv2.waitKey(0)





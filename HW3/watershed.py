import numpy as np
import cv2
from matplotlib import pyplot as plt
 
img = cv2.imread('road.jpg')
img_orign = cv2.imread('road_orign.jpg')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #轉換灰階

Hist = cv2.calcHist([img], [0], None, [256], [0,256]) #cv2.calcHist(影像, 通道, 遮罩, 區間數量, 數值範圍)
#灰階影像==> 通道指定: [0]
#彩色影像==> [0], [1], [2] 指定藍色, 綠色, 紅色的通道
plt.plot(Hist)
plt.show()

#-------------二值化-------------
#ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
ret, thresh = cv2.threshold(gray,150,255,0) #cv2.THRESH_TRIANGLE 
ret2, thresh2 = cv2.threshold(gray,105,255,1) #門檻值 二值化
thresh3 = cv2.bitwise_or(thresh,thresh2)

cv2.imshow("thresh",thresh)

cv2.imshow("thresh2",thresh2)

cv2.imshow("thresh3",thresh3)
cv2.waitKey(0)
#---------------------------------

# noise removal 去雜訊
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh2,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area 噪音消除
sure_bg = cv2.dilate(opening,kernel,iterations=3)

# Finding sure foreground area 尋找確定的前景區域
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.55*dist_transform.max(),255,0)

# Finding unknown region 尋找未知地區
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)
 
# Marker labelling 標記標籤
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers + 1
 
# Now, mark the region of unknown with zero
markers[unknown == 255] = 0
markers = cv2.watershed(img_orign, markers)
img_orign[markers == -1] = [255,0,0]

plt.subplot(2, 2, 1)
plt.title('img')
plt.imshow(img)

plt.subplot(2, 2, 2)
plt.title('img_orign')
plt.imshow(img_orign)

plt.subplot(2, 2, 3)
plt.title('markers')
plt.imshow(markers)

plt.subplot(2, 2, 4)
plt.title('thresh3')
plt.imshow(thresh3)
#plt.savefig('./markers.jpg')

#cv2.imshow("img_orign",img_orign)
#cv2.waitKey(0)
plt.show()
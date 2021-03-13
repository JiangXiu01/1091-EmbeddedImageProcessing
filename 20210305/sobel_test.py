import cv2
import numpy as np

img = cv2.imread("./road.jpg", 0)

img_CV_16S = cv2.Sobel(img,cv2.CV_16S,1,0) #CV_16S(16位無符號數)
abs = cv2.convertScaleAbs(img_CV_16S)
#cv2.imshow("orign", img)
cv2.imshow('img_CV_16S',abs)

cv2.waitKey()
cv2.destroyAllWindows()
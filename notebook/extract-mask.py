import numpy as np
import cv2 as cv
img = cv.imread('0-mask.png',0)
original_img = cv.imread('0.jpg',1)
ret,thresh = cv.threshold(img,127,255,0)
contours,hierarchy = cv.findContours(thresh, 1, 2)

# rect = cv.minAreaRect(contours[1])
# box = cv.boxPoints(rect)
# box = np.int0(box)
# cv.drawContours(original_img,[box],0,(0,0,255),2)
for i in range(len(contours)):
    x,y,w,h = cv.boundingRect(contours[i])
    crop_img = original_img[y:y+ int(h*1.1), x:x+ int(w*1.1)]
    cv.imshow(str(i), crop_img)

cv.drawContours(original_img, contours, -1,(100,0,0) , 3)
cv.imshow("Origin", original_img)
cv.waitKey(0)
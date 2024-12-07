import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv

cv2.namedWindow("Pencils",cv2.WINDOW_NORMAL)
all_pencils=0
for i in range(1,13):
    pencil=cv2.imread("img ("+str(i)+").jpg")
    gray = cv2.cvtColor(pencil, cv2.COLOR_BGR2GRAY)
    mask=cv2.inRange(gray, np.array([0]), np.array([100]))
    result=cv2.bitwise_and(gray, gray, mask=mask)
    tresh=cv2.threshold(result,25,255,cv2.THRESH_BINARY)[1]
    tresh=cv2.dilate(tresh, np.ones((10,10)))
    contours, hierarchy = cv2.findContours(tresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    num_of_pencils=0
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        if max(rect[1])/min(rect[1])>15 and min(rect[1])>70:
            num_of_pencils+=1
    print(f"На картинке под номером {i} видно {num_of_pencils} карандашей")
    all_pencils+=num_of_pencils
    cv2.imshow("Pencils",tresh)
    key = cv2.waitKey()
    if key==ord('q'):
        break
    else:
        continue
print(f"Всего карандашей {all_pencils}")
cv2.destroyAllWindows()

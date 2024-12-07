from mss import mss
import pyautogui
import cv2
import numpy as np
import time
def get_dino_center():
    screenWidth, screenHeight = pyautogui.size()
    with mss() as sct:
        monitor = {'top':200, 'left':0,\
                   'width':int(screenWidth), 'height':int(screenHeight/2)}
        img=np.array(sct.grab(monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tresh=cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)[1]
        tresh=cv2.dilate(tresh, np.ones((25,25)))
        contours, hierarchy = cv2.findContours(tresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        minarea=100000000
        cx,cy=(0,0)
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            if max(rect[1])/min(rect[1])<3 and minarea>rect[1][0]*rect[1][1]:
                M = cv2.moments(cnt)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                minarea=max(rect[1])*min(rect[1])
        return int(cx),int(cy)+200

def get_road(dx,dy):
    with mss() as sct:
        monitor = {'top':dy-100, 'left':dx,\
                       'width':700, 'height':100}
        img=np.array(sct.grab(monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tresh=cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)[1]
        return tresh 
def get_objects_centers(img):
    objects=[]
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        M = cv2.moments(cnt)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        x,y,w,h = cv2.boundingRect(cnt)
        objects+=[(x,cy,h,w)]
    return objects
def get_left_object(centers, end):
    except_dino=list(filter(lambda x: (x[0]>end) ,centers))
    if len(except_dino)>0:
         return min(except_dino, key=lambda x:x[0])
    else:
        return None
            
cx,cy=get_dino_center()
screenWidth, screenHeight = pyautogui.size()
pyautogui.click(cx,cy)
pyautogui.press('space')
time.sleep(4)
dot=230
speed=0.08
#pred_img=np.array([1])
#print(pred_img.shape)
count=0
last=0
insky=False
with mss() as sct:
    monitor = {'top':cy-100, 'left':cx,\
                       'width':700, 'height':100}
    while True:
        if dot<470:
            dot+=speed
        else:
            end=5
        print(dot)
        img=np.array(sct.grab(monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tresh=cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)[1]
        tresh=cv2.dilate(tresh,np.ones((5,5)))
        centers=get_objects_centers(tresh)
        left_obj=get_left_object(centers, int(dot/9))
        if left_obj!=None: 
            if left_obj[0]+left_obj[3]<=int(dot) and left_obj[1]>80:
                pyautogui.press('space')
            elif left_obj[0]+left_obj[3]<=int(dot/2) and left_obj[1]>50:
                pyautogui.keyDown('down')
                while True:
                    img=np.array(sct.grab(monitor))
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    tresh=cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)[1]
                    tresh=cv2.dilate(tresh,np.ones((5,5)))
                    centers=get_objects_centers(tresh)
                    left_obj=get_left_object(centers,int(dot/9))
                    if left_obj is not None:
                        if left_obj[1]>80:
                            break
                #pyautogui.sleep(0.2)
                pyautogui.keyUp('down')

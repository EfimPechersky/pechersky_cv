import zmq
import cv2
import numpy as np
import time
import random
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
#SSID lessons PASSWORD: robolab123
port=5555
socket.connect("tcp://192.168.0.100:%s" %port)
cv2.namedWindow("Client recv", cv2.WINDOW_GUI_NORMAL)
count=0
filmit = 94
silmit=20

def fupdate(value):
    global filmit
    filmit=value

def supdate(value):
    global silmit
    silmit=value

cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
cv2.createTrackbar("F", "Mask", filmit, 255, fupdate)
cv2.createTrackbar("S", "Mask", silmit, 255, supdate)

def get_objects(image):
    frame=image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = hsv[:,:,2]
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    contours = cv2.Canny(gray, filmit, silmit)
    contours = cv2.dilate(contours, np.ones((5,5)))
    num=0
    circles=0
    cnts, hierarchy = cv2.findContours(contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(cnts)):
        if hierarchy[0][i][3]==-1:
            (x,y), rad=cv2.minEnclosingCircle(cnts[i])
            center = int(x),int(y)
            if 3.14*(rad**2)/cv2.contourArea(cnts[i])<1.1:
                circles+=1
            cv2.circle(image, center, 4, (0,255,0), 3)
            num+=1
    print("Всего:",num,"Круги", circles,"Квадраты",num-circles)
        
    cv2.drawContours(frame, cnts, -1, (0,0,0),3)
    return num
objects_num=[]
while True:
    msg=socket.recv()
    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), -1)
    count+=1
    key=cv2.waitKey(100)
    num = get_objects(frame)
    if len(objects_num)<10:
        objects_num+=[num]
    else:
        objects_num=objects_num[1:]+[num]
    print(int(sum(objects_num)/len(objects_num)))
    if key==ord('q'):
        break
    cv2.imshow("Client recv", frame)
cv2.destroyAllWindows()

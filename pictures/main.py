import cv2
import numpy as np

def get_colors_sum(colors, keys, num):
    return sum(colors[keys[i]] for i in range(num))

def check_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv[:, :, 0], (7, 7), 3)
    
    hist = np.bincount(hsv.flatten())
    colors = {i: count for i, count in enumerate(hist) if count > 0}
    
    if len(colors) < 4:
        return False
    
    sortcol = sorted(colors, key=lambda x: -colors[x])
    if get_colors_sum(colors, sortcol, 4) / hsv.size < 0.7 and (colors[sortcol[0]] - colors[sortcol[1]]) / colors[sortcol[0]] < 0.01:
        return True
    else:
        return False

vidcap = cv2.VideoCapture('output.avi')
success, image = vidcap.read()
rightcount = 0
allcount = 0

while success:
    if check_image(image):
        rightcount += 1
        print(f"Картинка под номером {allcount} моя")
    allcount += 1
    success, image = vidcap.read()

print(f"В видео было найдено {rightcount} моих картинок среди {allcount} картинок всего")

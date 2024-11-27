import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv
im=plt.imread("balls_and_rects.png")
binary=im.mean(2)
binary[binary>0]=1
labeled=label(binary)
regions=regionprops(labeled)
im_hsv=rgb2hsv(im)
rect_colors=[]
ball_colors=[]
for region in  regions:
    cy, cx=region.centroid
    ecn=region.eccentricity
    color=im_hsv[int(cy), int(cx)][0]
    if ecn>0.1:
        rect_colors.append(color)
    else:
        ball_colors+=[color]

ball_hues=np.unique(list(map(lambda x:round(x,1), ball_colors)))
rect_hues=np.unique(list(map(lambda x:round(x,1), rect_colors)))
roundbc=np.array([round(i,1) for i in ball_colors])
roundrc=np.array([round(i,1) for i in rect_colors])
all_dict={}
for i in ball_hues:
    bcolor=len(roundbc[roundbc==i])
    all_dict[i]=bcolor
    print("Кругов оттенка со значением",i,"-",bcolor)
for i in rect_hues:
    if i not in all_dict:
        all_dict[i]=0
    rcolor=len(roundrc[roundrc==i])
    all_dict[i]+=rcolor
    print("Четырёхугольников оттенка со значением",i,"-",rcolor)
for i in all_dict:
    print("Всего объектов оттенка со значением",i,"-",all_dict[i])

plt.figure()
plt.plot(sorted(rect_colors),"o")
plt.figure()
plt.plot(sorted(ball_colors),"o")
plt.show()

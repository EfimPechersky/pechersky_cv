import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face
import scipy.ndimage.morphology as snm

def neighbours2(y,x):
    return (y, x-1), (y-1, x)

def exist(B, nbs):
    left, top=nbs
    if left[0] >=0 and left[0]<B.shape[0] and left[1]>=0 and left[1]<B.shape[1]:
        if B[left]==0:
            left=None
    else:
        left=None
    
    if top[0] >=0 and top[0]<B.shape[0] and top[1]>=0 and top[1]<B.shape[1]:
        if B[top]==0:
            top=None

    else:
        top=None
    
    return left, top

def find(label, linked):
    j = label
    while linked[int(j)] !=0:
        j = linked[int(j)]
    return j

def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)
    if j!=k:
        linked[int(k)] = j

def two_pass(B):
    LB = np.zeros_like(B, dtype="uint16")
    linked = np.zeros(B.size // 2, dtype="uint16")
    label = 1
    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y,x]!=0:
                nbs=neighbours2(y,x)
                existed = exist(B,nbs)
                if  existed[0] is None and existed[1] is None:
                    m = label
                    label+=1
                else:
                    lbs = [LB[n] for n in existed if n is not None]
                    m = min(lbs)
                LB[y,x]=m
                for n in existed:
                    if n is not None:
                        lb = LB[n]
                        if lb!=m:
                            union(m, lb, linked)

    
    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y,x]!=0:
                new_label = find(LB[y, x], linked)
                LB[y,x] = new_label
    
    for i,x in enumerate(np.unique(LB)):
        LB[LB == x]=i
    return LB

def maxel(arr):
    return int(np.max(arr))


image=np.load("ps.npy.txt")
tpimage = two_pass(image)
objnum = maxel(tpimage)
print("Всего объектов: "+str(objnum))
structlist=[]
numlist=[]
for i in  range(1,objnum+1):
    oneobj = (tpimage == i)*1
    wob=np.where(oneobj==1)
    starty=wob[0][0]
    startx=wob[1][0]
    endy=wob[0][-1]
    endx=wob[1][-1]
    struct = list(map(list,list(oneobj[starty:endy+1, startx:endx+1])))
    if struct not in structlist:
        structlist+=[struct]
        numlist+=[1]
    else:
        numlist[structlist.index(struct)]+=1

for st in range(0,len(structlist)):
    plt.subplot(1,len(structlist),st+1)
    plt.title("Объект "+str(st+1))
    plt.imshow(structlist[st])
    print("Количество объектов "+str(st+1)+": "+str(numlist[st]))
plt.show()

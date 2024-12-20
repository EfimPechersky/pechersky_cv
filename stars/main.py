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
    LB = np.zeros_like(B)
    linked = np.zeros(B.size // 2, dtype="uint")
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


image=np.load("stars.npy")
dil=two_pass(snm.binary_dilation(image, structure=np.array([[1,1]]))*1)
er = two_pass(snm.binary_erosion(image, structure=np.array([[1,1], [1,1]]))*1)
print("Количество звездочек: ",maxel(dil) - maxel(er))
plt.subplot(2,2,1)
plt.imshow(dil)
plt.subplot(2,2,2)
plt.imshow(er)
plt.subplot(2,2,3)
plt.imshow(image)
plt.show()



import numpy as np
import matplotlib.pyplot as plt
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

for i in range(1,7):
    image=np.load("wires"+str(i)+"npy.txt")
    s=np.array([[0,1,0],[0,1,0],[0,1,0]])
    new_image = two_pass(image)
    wiresnum = maxel(new_image)
    print("В файле под номером "+str(i))
    def check_wire(wire):
        for y in range(0, wire.shape[0]):
            for x in range(0, wire.shape[1]):
                if wire[y,x]>0:
                    if not np.all(wire[y,:]==np.ones([1,wire.shape[1]])):
                        return False
                    else:
                        return True
                    
    print("Общее количество проводов: "+str(wiresnum))
    for i in  range(1,wiresnum+1):
        wire = (new_image == i)*1
        wire_parts = two_pass(snm.binary_erosion(wire, structure = s).astype("int8"))
        if maxel(wire_parts)==1 and check_wire(wire_parts):
            print("Провод под номером "+str(i)+" целый")
        elif maxel(wire_parts)>1:
            print("Провод под номером "+str(i)+" разорван на "+str(maxel(wire_parts))+" частей")
        elif maxel(wire_parts)==0:
            print("Провод под номером "+str(i)+" польностью разорван")
    print()

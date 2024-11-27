import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops



trs=[]
for i in range(0,100):
    data=np.load("motion/h_"+str(i)+".npy")
    labeled=label(data)
    regions=regionprops(labeled)
    for r in regions:
        center=[r.centroid[0],r.centroid[1]]
        if len(trs)<labeled.max():
            trs+=[[center.copy()]]
        else:
            distances=[]
            for t in trs:
                d=(t[-1][0]-center[0])**2 + (t[-1][1]-center[1])**2 
                distances+=[d]
            distances=np.array(distances)
            trs[distances.argmin()]+=[center.copy()]
trs=np.array(trs)
for t in trs:
    plt.plot(t[:,1], t[:,0])
plt.show()

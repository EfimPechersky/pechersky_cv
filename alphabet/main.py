import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage.measure import label, regionprops, euler_number
from collections import defaultdict
def recognize(region):
    if region.image.mean()==1:
        return '-'
    else:
        enum = euler_number(region.image,2)
        if enum == -1:#B or 8
            if np.sum(np.mean(region.image[:,:region.image.shape[1]//2], 0)==1)>3:
                return "B"
            else:
                return "8"
            pass
        elif enum == 0:#A 0 P D *
            if np.sum(np.mean(region.image, 0)==1)>3:
                if region.eccentricity<0.6:
                    return "D"
                else:
                    return "P"
            else:
                holearea=(region.filled_area-np.sum(region.image))/region.image.size
                if holearea>0.2:
                    return "0"
                elif holearea>0.05:
                    return "A"
                else:
                    return "*"
        else:#/ W X * 1
            if np.sum(np.mean(region.image, 0)==1)>3:
                return "1"
            else:
                if region.eccentricity <0.4:
                    return '*'
                else:
                    image = region .image.copy()
                    image[0, :] = 1
                    image[-1, :] = 1
                    image[:, 0] = 1
                    image[:, -1] = 1
                    enumber = euler_number(image)
                    if enumber == -1:
                        return "/"
                    elif enumber == -3:
                        return "X"
                    else:
                        return "W"
    return '@'
arr=(plt.imread('symbols.png')[:,:,0]>0)*1
path=Path("./symbols")
path.mkdir(exist_ok=True)
labarr=label(arr)
alreg=regionprops(labarr)
result=defaultdict(lambda: 0)
for i,r in enumerate(alreg):
    symbol=recognize(r) 
    result[symbol]+=1
print(result)
plt.imshow(labarr)
plt.show()

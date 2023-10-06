import numpy as np
import cv2 as cv
img = cv.imread('test6.jpg')
assert img is not None, "file could not be read, check with os.path.exists()"
px = img[100,100]
print( px )
# accessing only blue pixel
blue = img[100,100,0]
print( blue )
img[100,100] = [255,255,255]
print( img[100,100] )
img.item(10,10,2)
59
# modifying RED value
img.itemset((10,10,2),100)
img.item(10,10,2)
print( img.shape )
print( img.size )
print( img.dtype )
ball = img[280:340, 330:390]
img[273:333, 100:160] = ball
b,g,r = cv.split(img)
img = cv.merge((b,g,r))
b = img[:,:,0]
img[:,:,2] = 0

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
BLUE = [255,0,0]
img1 = cv.imread('test6.jpg')
assert img1 is not None, "file could not be read, check with os.path.exists()"
replicate = cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_REPLICATE)
reflect = cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_REFLECT)
reflect101 = cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_REFLECT_101)
wrap = cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_WRAP)
constant= cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_CONSTANT,value=BLUE)
plt.subplot(231),plt.imshow(img1,'gray'),plt.title('ORIGINAL')
plt.subplot(232),plt.imshow(replicate,'gray'),plt.title('REPLICATE')
plt.subplot(233),plt.imshow(reflect,'gray'),plt.title('REFLECT')
plt.subplot(234),plt.imshow(reflect101,'gray'),plt.title('REFLECT_101')
plt.subplot(235),plt.imshow(wrap,'gray'),plt.title('WRAP')
plt.subplot(236),plt.imshow(constant,'gray'),plt.title('CONSTANT')
plt.show()
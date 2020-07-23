
import cv2
import numpy as np
 
def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread(r'C:\Users\Owen\Pictures\weixin1.jpg')
original = cv2.resize(img, None, fx=0.5, fy=0.5)

cv_show('original',original)
kernel = np.array([[0,-1,0],
                  [-1,5,-1],
                  [0,-1,0]])

image_enhance=cv2.filter2D(original,ddepth=cv2.CV_8UC3,kernel=kernel)

cv_show('image_enhance',image_enhance)
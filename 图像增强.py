import cv2
import numpy as np


def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


original = cv2.imread(r'C:\Users\Owen\Pictures\weixin1.jpg')
cv_show('original',original)

(b,g,r) = cv2.split(original)
bh = cv2.equalizeHist(b)
gh = cv2.equalizeHist(g)
rh = cv2.equalizeHist(r)

cv_show('bh',bh)
cv_show('gh',gh)
cv_show('rh',rh)



equalizeHisted = cv2.merge((bh,gh,rh))

cv_show('equalizeHist',equalizeHisted)



hls = cv2.cvtColor(original,cv2.COLOR_BGR2HLS)
(h,l,s) = cv2.split(hls)
hh = cv2.equalizeHist(h)
lh = cv2.equalizeHist(l)
sh = cv2.equalizeHist(s)

cv_show('hh',hh)
cv_show('lh',lh)
cv_show('sh',sh)

equalizeHisted = cv2.merge((h,lh,s))

bgr_equalizeHisted = cv2.cvtColor(equalizeHisted,cv2.COLOR_HLS2BGR)


cv_show('hls equalizeHist',bgr_equalizeHisted)




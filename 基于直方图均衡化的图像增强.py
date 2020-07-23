
import cv2
 
def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread(r'C:\Users\Owen\Pictures\weixin1.jpg')
original = cv2.resize(img, None, fx=0.5, fy=0.5)


img_hist = img.copy()
for i in range(3):
    img_hist[i]=cv2.equalizeHist(img[i])

cv_show('img',img)
cv_show('img_hist',img_hist)
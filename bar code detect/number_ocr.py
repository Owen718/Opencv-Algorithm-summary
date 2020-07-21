import cv2
import numpy as np
import pytesseract
from PIL import Image
import scan

def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread(r'C:\Users\Owen\Pictures\scan_ocr\10.jpg')
cv_show('original',img)

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

if img.shape[1]<img.shape[0]:
    res = rotate_bound(img,90)
else:
    res = img


scanned = scan.scan_image(img)          #文本内容边框识别，变换处理，若需要则将下面第二行的img改为scanned
#cv_show('scan',scanned)


print(res.shape)
print(img.shape)

cv_show('res',res)
cv_show('img',img)
roi = res[0:int(res.shape[0]*0.08),int(res.shape[1]*0.7):res.shape[1]]
#cv_show('roi',roi)

ret,roi_binary = cv2.threshold(roi,127,255,cv2.THRESH_BINARY_INV)  #翻转二值化处理
cv_show('roi_binary',roi_binary)
number = pytesseract.image_to_string(roi_binary)
print(number)

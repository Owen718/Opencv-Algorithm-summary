import cv2
import numpy as np
import time
import os

cap = cv2.VideoCapture(0)
cap.set(5,30)
net = cv2.dnn.readNetFromCaffe(prototxt="D:\github\Opencv-Algorithm-summary\deploy.prototxt",
                               caffeModel="D:\\github\\Opencv-Algorithm-summary\\res10_300x300_ssd_iter_140000_fp16.caffemodel")

face_positon=[0,0,0,0]

def face_detected(img):
    
    eye_cascade = cv2.CascadeClassifier('D:\python_code\haarcascades\haarcascade_eye.xml')  #眼部haar特征文件
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blob = cv2.dnn.blobFromImage(cv2.resize(img,(300,300)),
                                1.0,
                                (300,300),
                                (104.0,177.0,123.0))
    net.setInput(blob)
    detections = net.forward()
    h,w,c=img.shape
    for i in range(0,detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence > 0.6:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(img, (startX, startY), (endX, endY),
                (0, 255,0), 1)
            cv2.putText(img, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
    return img

  



while True:
    ret,frame = cap.read()
    if ret == True:
        start = time.time()
        
        face_position = [0,0,frame.shape[1],frame.shape[0]]
        frame = face_detected(frame)
  
        end = time.time()
        seconds = end-start
        #print( "Time taken : {0} seconds".format(seconds))
        fps = 1 / seconds
        #print( "Estimated frames per second : {0}".format(fps))
        #print(face_position)
        cv2.putText(frame, "FPS: {0}".format(float('%.1f'%fps)),(int(frame.shape[0]/10),int(frame.shape[1]/10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                    1)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
    else:
        break

cap.release()

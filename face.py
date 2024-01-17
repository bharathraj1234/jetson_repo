import numpy as np
import cv2
import os
# dispW=640
# dispH=480
cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH,dispW)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT,dispH)
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
while True:
 ret, frame = cam.read()
 gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
 faces=face_cascade.detectMultiScale(gray,1.3,5)
 for (x,y,w,h) in faces:
  cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
 framesmall=cv2.resize(frame,(640,480))
 cv2.imshow('frame', framesmall)
 cv2.moveWindow('frame',0,0)
 if cv2.waitKey(1) & 0xFF == ord('q'):
   break
# When everything done, release the capture
t, frame = cam.read()
 gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
 faces=face_cascade.detectMultiScale(gray,1.3,5)
 for (x,y,w,h) in faces:
  cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
 framesmall=cv2.resize(frame,(640,480))
 cv2.imshow('frame', framesmall)
 cv2.moveWindow('frame',0,0)
 if cv2.waitKey(1) & 0xFF == ord('q'):
=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
 faces=face_cascade.detectMultiScale(gray,1.3,5)
 for (x,y,w,h) in faces:
  cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
 framesmall=cv2.resize(frame,(640,480))
 cv2.imshow('frame', framesmall)
 cv2.moveWindow('frame',0,0)
 if cv2.waitKey(1) & 0xFF == ord('q'):
   break
# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
   break
# When everything done, release the capture
cam.release()
cam.release()
cv2.destroyAllWindows()

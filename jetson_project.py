# import cv2
# import serial
# import time

# # Set initial pan and tilt angles
# pan = 90
# tilt = 90

# # OpenCV video capture
# cam = cv2.VideoCapture(0)

# # Haarcascades for face and eyes
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# # Serial communication setup
# ser = serial.Serial('COM8', 115200, timeout=1)  # Change 'COM3' to your Arduino's COM port

# time.sleep(2)  # Allow time for the Arduino to initialize

# while True:
#     ret, frame = cam.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#     for (x, y, w, h) in faces:
#         Xcent = x + w / 2
#         Ycent = y + h / 2

#         # Calculate errors and adjust pan and tilt
#         errorPan = Xcent - 640 / 2
#         errorTilt = Ycent - 480 / 2

#         if abs(errorPan) > 15:
#             pan = pan - errorPan / 50
#         if abs(errorTilt) > 15:
#             tilt = tilt - errorTilt / 50

#         # Ensure pan and tilt are within valid range
#         pan = max(0, min(180, pan))
#         tilt = max(0, min(180, tilt))

#         # Send pan and tilt values to Arduino through serial
#         ser.write(f"{int(pan)} {int(tilt)}\n".encode())

#         # Region of interest for eyes
#         roi_gray = gray[y:y+h, x:x+w]
#         roi_color = frame[y:y+h, x:x+w]

#         # Detect eyes in the region of interest
#         eyes = eye_cascade.detectMultiScale(roi_gray)
#         for (ex, ey, ew, eh) in eyes:
#             cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (225, 0, 0), 2)

#     cv2.imshow('nanoCam', frame)
#     cv2.moveWindow('nanoCam', 0, 0)

#     if cv2.waitKey(1) == ord('q'):
#         break

# cam.release()
# cv2.destroyAllWindows()
# ser.close()
import cv2
import serial
import time

# Set initial pan and tilt angles
pan = 90
tilt = 90

# OpenCV video capture
cam = cv2.VideoCapture(0)

# Haarcascades for face and eyes
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('eye_glass_detection1.xml')

# Serial communication setup
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # Change 'COM3' to your Arduino's COM port

time.sleep(2)  # Allow time for the Arduino to initialize

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        Xcent = x + w / 2
        Ycent = y + h / 2

        # Calculate errors and adjust pan and tilt
        errorPan = Xcent - 640 / 2
        errorTilt = Ycent - 480 / 2

        if abs(errorPan) > 15:
            pan = pan - errorPan / 50
        if abs(errorTilt) > 15:
            tilt = tilt - errorTilt / 50

        # Ensure pan and tilt are within valid range
        pan = max(0, min(180, pan))
        tilt = max(0, min(180, tilt))

        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Send pan and tilt values to Arduino through serial
        ser.write(f"{int(pan)} {int(tilt)}\n".encode())

        # Region of interest for eyes
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect eyes in the region of interest
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (225, 0, 0), 2)

    cv2.imshow('nanoCam', frame)
    cv2.moveWindow('nanoCam', 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
ser.close()


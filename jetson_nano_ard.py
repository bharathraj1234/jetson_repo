import cv2
import serial
import time
import mediapipe as mp

# Set initial pan and tilt angles
pan = 90
tilt = 90

# OpenCV video capture
cam = cv2.VideoCapture(0)

# MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Serial communication setup
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # Change 'COM3' to your Arduino's COM port

time.sleep(2)  # Allow time for the Arduino to initialize

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert the BGR image to RGB before processing with MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                # Draw a rectangle around the detected face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Calculate errors and adjust pan and tilt
                errorPan = x + w / 2 - iw / 2
                errorTilt = y + h / 2 - ih / 2

                if abs(errorPan) > 15:
                    pan = pan - errorPan / 50
                if abs(errorTilt) > 15:
                    tilt = tilt - errorTilt / 50

                # Ensure pan and tilt are within valid range
                pan = max(0, min(180, pan))
                tilt = max(0, min(180, tilt))

                # Send pan and tilt values to Arduino through serial
                ser.write(f"{int(pan)} {int(tilt)}\n".encode())

        # Display the frame
        cv2.imshow('nanoCam', frame)
        cv2.moveWindow('nanoCam', 0, 0)

        if cv2.waitKey(1) == ord('q'):
            break

# Release resources
cam.release()
cv2.destroyAllWindows()
ser.close()

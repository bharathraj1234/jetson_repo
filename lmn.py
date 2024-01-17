from flask import Flask, render_template, Response
import cv2
import os

app = Flask(__name__)

# Use the path to the haarcascades directory
haarcascades_path = cv2.data.haarcascades

# Use the haarcascade files directly without joining paths
haarcascades_face_path = os.path.join(haarcascades_path, 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(haarcascades_face_path)

haarcascades_body_path = os.path.join(haarcascades_path, 'haarcascade_fullbody.xml')
body_cascade = cv2.CascadeClassifier(haarcascades_body_path)

# Use 0 as the camera index, which usually corresponds to the default camera


def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    num_faces = len(faces)
    cv2.putText(frame, f'Faces: {num_faces}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame

def detect_bodies(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    num_bodies = len(bodies)
    cv2.putText(frame, f'Bodies: {num_bodies}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame

def generate_frames():
    camera = cv2.VideoCapture(-1)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame_with_faces = detect_faces(frame.copy())
            frame_with_bodies = detect_bodies(frame.copy())
            ret, buffer_faces = cv2.imencode('.jpg', frame_with_faces)
            ret, buffer_bodies = cv2.imencode('.jpg', frame_with_bodies)

            frame_encoded_faces = buffer_faces.tobytes()
            frame_encoded_bodies = buffer_bodies.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded_faces + b'\r\n' +
                   b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded_bodies + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


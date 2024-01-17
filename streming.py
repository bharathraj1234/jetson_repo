from flask import Flask, render_template, Response

app = Flask(__name__)

def generate_frames():
    # Your frame generation logic here
    while True:
        # Your frame generation logic here
        frame = b''  # Replace this with your actual frame data
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


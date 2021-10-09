from flask import Flask, render_template, request, session
from flask.helpers import url_for
from flask.wrappers import Response
import cv2
from werkzeug.utils import redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh_so_secret'

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success,frame=camera.read()
        if not success:
            break
        else:
            detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')
            faces=detector.detectMultiScale(frame,1.1,7)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
             #Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            '''
            ret,buffer=cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   '''

@app.route('/')
def index():
    if session.get("username") == "admin" and session.get("password") == "admin1234":
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/stream-live-camera-1')
def streamLive():
    return render_template('stream-live-index.html')

@app.route('/video')
def video():
    if session.get("username") == "admin" and session.get("password") == "admin1234":
        return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        if username == "admin" and password == "admin1234":
            session['username'] = username
            session['password'] = password
            return redirect(url_for('index'))
        else:
            return render_template('login.html',error_message="Wrong Credentials")

    if session.get("username") == "admin" and session.get("password") == "admin1234":
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session["username"] = None
    session["password"] = None
    cv2.destroyAllWindows()
    #camera.release()
    return redirect(url_for('index'))

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000,debug=True)
    app.run(debug=True)
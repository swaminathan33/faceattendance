from flask import Flask, Response
import cv2
from deepface import DeepFace
import threading
import datetime
import pymongo

person1 = cv2.imread('./bill.jpeg')
person2 = cv2.imread('./elon.jpeg')
attendant = set()

f = open('attendance.txt', 'w')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["camera"]
mycol = mydb["attendance"]


def recogniser(name):
    if name not in attendant:
        print(name)
        attendant.add(name)
        add = {
            "name": name,
            "time": datetime.datetime.now().ctime()
        }
        mycol.insert_one(add)

face_match = False
def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, person1)['verified']:
            face_match = True
            recogniser('bill')

        elif DeepFace.verify(frame, person2)['verified']:
            face_match = True
            recogniser('elon')
        else:
            face_match = False

    except ValueError:
        face_match = False

app = Flask(__name__)
video = cv2.VideoCapture(0)

@app.route('/')
def index():
    return "Default Message"
def gen(video):
    counter = 0
    while True:
        success, image = video.read()
        if success:
            if counter % 30 == 0:
                try:
                    threading.Thread(target=check_face, args=(image.copy(),)).start()
                except ValueError:
                    pass
            counter += 1

            if face_match:
                cv2.putText(image, 'Match !', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            else:
                cv2.putText(image, 'No Match !', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)
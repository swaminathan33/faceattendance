# face attendance using streamlit

import streamlit as st
import cv2
from deepface import DeepFace
import threading
from streamlit_webrtc import webrtc_streamer
import av
import datetime
import pymongo
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["camera"]
mycol = mydb["attendance"]

person1 = cv2.imread('./bill.jpeg')
person2 = cv2.imread('./elon.jpeg')
attendant = set()

face_match = False

def recogniser(name):
    if name not in attendant:
        print(name)
        attendant.add(name)
        add = {
            "name": name,
            "time": datetime.datetime.now().ctime()
        }
        mycol.insert_one(add)

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





def call(frame):

    img1 = frame.to_ndarray(format='bgr24')
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

    check_face(img)

    if face_match:
        cv2.putText(img, 'Match !', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    else:
        cv2.putText(img, 'No Match !', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    img = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)

    return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(key='example', video_frame_callback=call)

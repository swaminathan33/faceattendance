# trying using streamlit webrtc

import streamlit as st
from streamlit_webrtc import webrtc_streamer
import numpy as np
import av
import cv2

def hello(frame):
    
    img = frame.to_ndarray(format='bgr24')

    cv2.putText(img, 'Match !', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(key='hello', video_frame_callback=hello)

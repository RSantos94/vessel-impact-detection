import threading

import cv2
from flask import Flask
from flask import Response
from flask import render_template
import tkinter as tk
from imutils.video import VideoStream

from Background_subtraction_KNN import BackgroundSubtractionKNN
from cameraTransformation import CameraTransformation

outputFrame = None
bs1 = None
bs2 = None
bsz3 = None
cap1 = None
cap2 = None
lock = threading.Lock()
app = Flask(__name__)


@app.route("/")
def web_page():
    # return the rendered template
    return render_template("impactDetection.html")


@app.route("/video_feed_1")
def video_feed_1():
    # return the response generated along with the specific media
    # type (mime type)
    global bs1
    return Response(generate(bs1),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/video_feed_2")
def video_feed_2():
    # return the response generated along with the specific media
    # type (mime type)
    global bs2
    return Response(generate(bs2),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/video_feed_test")
def video_feed_test():
    # return the response generated along with the specific media
    # type (mime type)
    global bs2
    return Response(gen_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def generate(bs):
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            if bs is None:
                continue

            outputFrame = bs.frame()
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


def gen_frames():
    global cap1

    while True:
        if cap1 is None:
            continue
        success, frame_test = cap1.read()  # read the camera frame
        if not success:
            break
        else:
            resized_frame = cv2.resize(frame_test, (960, 540))
            ret, buffer = cv2.imencode('.jpg', resized_frame)
            resized_frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + resized_frame + b'\r\n')


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)
    # cap1 = cv2.VideoCapture('video_files/GH010731.MP4')
    # cap2 = cv2.VideoCapture('video_files/MVI_2438.MP4')
    # bs1 = BackgroundSubtractionKNN('video_files/GH010731_cut.MP4')
    # bs1.subtractor(lock, 5000)
    # bs2 = BackgroundSubtractionKNN('video_files/MVI_2438.MP4')
    # bs2.subtractor(lock, 5000)
    bsz3 = BackgroundSubtractionKNN('GH010890')
    bsz3.create_centroids_file()
    bsz3.subtractor(lock, 1000)
    ct = CameraTransformation('GH010890')
    ct.configure()

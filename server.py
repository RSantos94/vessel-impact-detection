import threading

import cv2
from flask import Flask
from flask import Response
from flask import render_template
import tkinter as tk
from imutils.video import VideoStream

from Background_subtraction_KNN import BackgroundSubtractionKNN
from processCentroids import ProcessCentroids


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

    #source = 'MVI_2438' #lnec camara
    source = 'GH010731_cut' #lnec gopro
    #source = 'GH010890' #Z3
    # window_size = (640, 360)
    # window_size = (1280, 720)
    window_size = (1980, 1080)
    # window_size = (3840, 2160)

    #bs = BackgroundSubtractionKNN(source, window_size)
    #bs.create_centroids_file()
    #history = 10 #Z3 fica bem
    #detectShadows = False #Z3 fica bem
    #dist2Threshold = 100 #Z3 fica bem
    # object_min_area = 1000 #Z3 fica bem
    history = 10  # lnec gp fica bem
    detectShadows = False  # lnec gp fica bem
    dist2Threshold = 1000  # lnec gp fica bem
    object_min_area = 1200  # lnec gp fica bem
    #bs.subtractor(lock, object_min_area, history, detectShadows, dist2Threshold)

    objects_to_track = ['18']
    # objects_to_track = None
    pc = ProcessCentroids(source, objects_to_track)
    pc.execute()



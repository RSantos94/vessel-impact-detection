import threading

import cv2
from flask import Flask
from flask import Response
from flask import render_template
import tkinter as tk
from imutils.video import VideoStream

from Background_subtraction_KNN import BackgroundSubtractionKNN
from processCentroids import ProcessCentroids
from stereoProcessing import StereoProcessing

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
        else:
            success, frame_test = cap1.read()  # read the camera frame
            if not success:
                break
            else:
                resized_frame = cv2.resize(frame_test, (960, 540))
                ret, buffer = cv2.imencode('.jpg', resized_frame)
                resized_frame = buffer.tobytes()
                yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + resized_frame + b'\r\n'


def create_bs(source_file, compute_window_size):
    return BackgroundSubtractionKNN(source_file, compute_window_size)


def run(bs, bs_history, detect_shadows, dist_2_threshold, centroid_object_min_area):
    bs.subtractor(lock, centroid_object_min_area, bs_history, detect_shadows, dist_2_threshold)

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)

    # stereo = True

    # window_size = (640, 360)
    # window_size = (1280, 720)
    window_size = (1980, 1080)
    # window_size = (3840, 2160)

    # bs.create_centroids_file()

    # objects_to_track = None
    stereo = input("Stereo (y/n)?:")

    if stereo == 'y':
        # source1 = 'MVI_2438'  # lnec camara
        # source2 = 'GH010731_cut'  # lnec gopro
        source1 = 'GH010946_1'
        source2 = 'PXL_20220308_141209924_1'

        history1 = 20  # piscina gp fica bem
        detectShadows1 = False  # piscina gp fica bem
        dist2Threshold1 = 2000  # piscina gp fica bem
        object_min_area1 = 800  # piscina gp fica bem
        history2 = 20  # piscina pxl fica bem
        detectShadows2 = False  # piscina pxl fica bem
        dist2Threshold2 = 800  # piscina pxl fica bem
        object_min_area2 = 11000  # piscina pxl fica bem
        # window_size1 = (1280, 720)
        window_size1 = (1980, 1080)
        window_size2 = (1980, 1080)

        # frame = []

        bs1 = create_bs(source1, window_size1)
        bs2 = create_bs(source2, window_size2)

        sp = StereoProcessing(source1, source2)

        if sp.has_points_file(source1) is not True:
            bs1.get_screenshot()
            bs2.frames = bs1.frames

        if sp.has_points_file(source2) is not True:
            bs2.get_screenshot()

        if sp.has_points_file(source1) is not True and sp.has_points_file(source2) is not True:
            input("Create corresponding points file at config/{source}-points.txt and press enter")

        run(bs1, history1, detectShadows1, dist2Threshold1, object_min_area1)
        run(bs2, history2, detectShadows2, dist2Threshold2, object_min_area2)

        objects_to_track1 = []  # ['18']
        objects_to_track2 = []  # ['18']

        text1 = input("Object ids to track from first camera (separated by comma):")
        text2 = input("Object ids to track from second camera (separated by comma):")

        arr1 = text1.split(',')
        for x in arr1:
            objects_to_track1.append(str(x.split()))

        arr2 = text2.split(',')
        for x in arr2:
            objects_to_track2.append(str(x.split()))

        sp.objects_to_track1 = objects_to_track1
        sp.centroid_file_2 = objects_to_track2
        sp.configure_points(source1, source2)
        sp.execute()

    else:
        # source = 'MVI_2438' #lnec camara
        source = 'GH010731_cut'  # lnec gopro
        # source = 'GH010890' #Z3
        # history = 10 #Z3 fica bem
        # detectShadows = False #Z3 fica bem
        # dist2Threshold = 100 #Z3 fica bem
        # object_min_area = 1000 #Z3 fica bem
        history = 20  # lnec gp fica bem
        detectShadows = False  # lnec gp fica bem
        dist2Threshold = 1000  # lnec gp fica bem
        object_min_area = 1200  # lnec gp fica bem
        # history1 = 10  # lnec gp fica bem
        # detectShadows1 = False  # lnec gp fica bem
        # dist2Threshold1 = 1000  # lnec gp fica bem
        # object_min_area1 = 1200  # lnec gp fica bem
        # history2 = 10  # lnec gp fica bem
        # detectShadows2 = False  # lnec gp fica bem
        # dist2Threshold2 = 1000  # lnec gp fica bem
        # object_min_area2 = 1200  # lnec gp fica bem

        bs = create_bs(source, window_size)

        run(bs, history, detectShadows, dist2Threshold, object_min_area)

        objects_to_track = []  # ['18']

        text = input("Object ids to track (separated by comma):")

        arr1 = text.split(',')
        for x in arr1:
            objects_to_track.append(str(x.split()))

        pc = ProcessCentroids(source, objects_to_track)
        pc.execute()

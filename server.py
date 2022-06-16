import os
import platform
import threading

import sys

import cv2
from flask import Flask
from flask import Response
from flask import render_template
import tkinter as tk
from imutils.video import VideoStream
from os.path import exists


from tools.Background_subtraction_KNN import BackgroundSubtractionKNN
from tools.processCentroids import ProcessCentroids
from tools.interpolate_centroids import InterpolateCentroids

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


def create_bs(source_file, compute_window_size, os_name):
    return BackgroundSubtractionKNN(source_file, compute_window_size, os_name)


def run(bs, is_test):
    bs.create_centroids_file()
    bs.subtractor(is_test)

# check to see if this is the main thread of execution
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

    # stereo = True

    # window_size = (640, 360)
    # window_size = (1280, 720)
    window_size = (1980, 1080)
    # window_size = (3840, 2160)

    # bs.create_centroids_file()

    # objects_to_track = None
    os_name = platform.system()

    test = input("Test (y/n)?:")
    if test == 'y':
        source = input("Video 1 or 2:")
        if source == '1':
            sourceName = 'GH010949-cut'
        elif source == '2':
            sourceName = 'PXL_20220311_123649450-cut'

        window_size1 = (1980, 1080)
        bs1 = create_bs(sourceName, window_size1, os_name)

        run(bs1, is_test=True)
    else:
        stereo = input("Stereo (y/n)?:")

        if stereo == 'y':
            source1 = input("Video file 1 name:")
            source2 = input("Video file 2 name:")

            # source1 = 'MVI_2438'  # lnec camara
            # source2 = 'GH010731_cut'  # lnec gopro
            # source1 = 'GH010946_1' # teste piscina 1
            # source2 = 'PXL_20220308_141209924_1' # teste piscina 1
            source1 = 'GH010949-cut'  # teste piscina 2
            source2 = 'PXL_20220311_123649450-cut'  # teste piscina 2
            # source1 = 'GH010954_1'  # teste piscina tupperware 1
            # source2 = 'PXL_20220319_165746871_1'  # teste piscina tupperware 1

            # window_size1 = (1280, 720)
            window_size1 = (1980, 1080)
            window_size2 = (1980, 1080)

            # frame = []

            bs1 = create_bs(source1, window_size1, os_name)
            bs2 = create_bs(source2, window_size2, os_name)

            # sp = StereoProcessing(source1, source2)

            # if sp.has_points_file(source1) is not True:
            # bs1.get_screenshot()
            # bs2.frames = bs1.frames

            # if sp.has_points_file(source2) is not True:
            # bs2.get_screenshot()

            # if sp.has_points_file(source1) is not True and sp.has_points_file(source2) is not True:
            # input("Create corresponding points file at config/{source}-points.txt and press enter")

            # bs1.create_undistorted_video_file()
            # bs2.create_undistorted_video_file()

            # run(bs1, history1, detectShadows1, dist2Threshold1, object_min_area1, is_test=False)
            # run(bs2, history2, detectShadows2, dist2Threshold2, object_min_area2, is_test=False)

            objects_to_track1 = []
            objects_to_track2 = []

            text1 = input("Object ids to track from first camera (separated by comma):")
            text2 = input("Object ids to track from second camera (separated by comma):")

            arr1 = text1.split(',')
            for x in arr1:
                if x != '':
                    objects_to_track1.append(x)

            arr2 = text2.split(',')
            for x in arr2:
                if x != '':
                    objects_to_track2.append(x)

            ic = InterpolateCentroids(source1, source2, os_name)
            ic.objects_to_track1 = objects_to_track1
            ic.objects_to_track2 = objects_to_track2
            ic.execute()

            # sp.objects_to_track1 = objects_to_track1
            # sp.objects_to_track2 = objects_to_track2
            # sp.configure_points(source1, source2)
            # sp.execute()

        else:
            source = input("Video file name:")

            # source = 'MVI_2438' #lnec camara
            source = 'GH010731_cut'  # lnec gopro
            # source = 'GH010890' #Z3

            history, detectShadows, dist2Threshold, object_min_area = get_bs_param(source)

            bs = create_bs(source, window_size)

            run(bs, history, detectShadows, dist2Threshold, object_min_area)

            objects_to_track = []  # ['18']

            text = input("Object ids to track (separated by comma):")

            arr1 = text.split(',')
            for x in arr1:
                objects_to_track.append(str(x.split()))

            pc = ProcessCentroids(source, objects_to_track)
            pc.execute()

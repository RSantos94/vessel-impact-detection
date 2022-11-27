import glob
import os
import platform
#import ffmpeg

import cv2

from tools.camera_calibration import CameraCalibration
from os.path import exists

def calibrate (source):
    os_name = platform.system()
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)

    if os_name == "Windows":
        video_name = path + '\\video_files\\' + source + '.mp4'
        converted_path = path + '\\video_files\\converted\\' + source + '\\'
        fps_file = converted_path + 'fps.txt'
        video_file = converted_path + 'video.mp4'
    else:
        video_name = path + '/video_files/' + source + '.mp4'
        converted_path = path + '/video_files/converted/' + source + '/'
        fps_file = converted_path + 'fps.txt'
        video_file = converted_path + 'video.mp4'

    if exists(video_name):
        camera_calibration = CameraCalibration(source, os_name)
        camera_calibration.calibrate()

        cap = cv2.VideoCapture(video_name)

        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        if not os.path.exists(converted_path):
            os.makedirs(converted_path)

        with open(fps_file, 'w') as f:
            f.write(str(fps))

        # cap.release()

        img_counter = 0

        height = None
        width = None

        while cap.isOpened():
            # timer = cv2.getTickCount()
            success, img = cap.read()

            if not success:
             break

            if img is not None:

                if height is None:
                    height = img.shape[0]
                    width = img.shape[1]
                undistorted_img = camera_calibration.undistort(img)
                # cv2.imshow("Pier cam", img)

                img_name = converted_path + (str(img_counter)).zfill(10) + '.png'
                cv2.imwrite(img_name, undistorted_img)

                img_counter += 1

        cv2.destroyAllWindows()
        cap.release()

        images = sorted(glob.glob(converted_path + '*.png'), key=os.path.basename)

        f = open(fps_file, "r")
        fps = float(f.read())

        # process = ffmpeg.input('pipe:', format='png_pipe', r=str(fps)).output(video_file, vcodec='libx264').overwrite_output().run_async(pipe_stdin=True)

        # process2 = (
        #     ffmpeg
        #     .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
        #     .output(video_file, pix_fmt='yuv420p')
        #     .overwrite_output()
        #     .run_async(pipe_stdin=True)
        # )

        # for image in images:
        #     with open(image, 'rb') as f:
        #         # Read the JPEG file content to jpeg_data (bytes array)
        #         jpeg_data = f.read()
        #
        #         # Write JPEG data to stdin pipe of FFmpeg process
        #         process.stdin.write(jpeg_data)
        #
        # process.stdin.close()

    else:
        print("Video " + video_name + "doesn't exists!")
if __name__ == '__main__':
    source = input("Video file name:")

    calibrate(source)

import glob
import os
import platform
import time

import cv2

from tools.camera_calibration import CameraCalibration

if __name__ == '__main__':
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    parent_path = os.path.dirname(path)

    os_name = platform.system()

    if os_name == "Windows":
        images = glob.glob(parent_path + '\\Camera calibration\\cam_calibration\\gopro\\*.jpg')
    else:
        images = glob.glob('Camera calibration/cam_calibration/gopro/*.jpg')

    calibration = CameraCalibration('GH', os_name)
    calibration.calibrate()

    i = 0
    for image in images:
        img = cv2.imread(image)
        imS = calibration.undistort(img)
        csv_name = image[:-3] + "-undistorted.png"
        cv2.imshow("Image undistorted " + image, imS)
        cv2.imshow("Image " + image, img)
        cv2.imwrite(csv_name, imS)
        # time.sleep(10)
        i += 1

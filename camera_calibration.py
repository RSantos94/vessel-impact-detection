import glob
import os

import cv2
import cv2 as cv
import numpy as np


class CameraCalibration:

    def __init__(self, video_name):
        self.dist = None
        self.mtx = None
        self.video_name = video_name

    def calibrate(self):

        if os.path.isfile('Camera calibration/' + self.video_name[12:14] + '-mtx.csv') and os.path.isfile(
                'Camera calibration/' + self.video_name[12:14] + '-dist.csv'):
            # data = pd.read_csv('Camera calibration/' + self.video_name[12:14] + '.csv')

            self.mtx = np.loadtxt('Camera calibration/' + self.video_name[12:14] + '-mtx.csv', delimiter=',')
            self.dist = np.loadtxt('Camera calibration/' + self.video_name[12:14] + '-dist.csv', delimiter=',')

        else:
            # termination criteria
            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
            objp = np.zeros((9 * 6, 3), np.float32)
            objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
            # Arrays to store object points and image points from all the images.
            objpoints = []  # 3d point in real world space
            imgpoints = []  # 2d points in image plane.
            gray = None
            if self.video_name[12:14] == 'GH':
                images = glob.glob('Camera calibration/cam_calibration/gopro/2/*.jpg')
            elif self.video_name[12:14] == 'PX':
                images = glob.glob('Camera calibration/cam_calibration/pxl/*.jpg')
            else:
                images = None  # = glob.glob('video_files/cam_calibration/gopro/2/*.jpg')
            if images is not None:
                for fname in images:
                    img = cv.imread(fname)
                    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                    # Find the chess board corners
                    ret, corners = cv.findChessboardCorners(gray, (9, 6), None)
                    # If found, add object points, image points (after refining them)
                    if ret == True:
                        objpoints.append(objp)
                        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                        imgpoints.append(corners)
                        # Draw and display the corners
                        cv.drawChessboardCorners(img, (7, 5), corners2, ret)
                        imS = cv2.resize(img, (960, 540))
                        cv.imshow('img', imS)
                        cv.waitKey(500)
                cv.destroyAllWindows()

            if gray is not None:
                ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

                mtx_array = np.asarray(mtx)
                np.savetxt('Camera calibration/' + self.video_name[12:14] + '-mtx.csv', mtx_array, delimiter=',')
                dist_array = np.asarray(dist)
                np.savetxt('Camera calibration/' + self.video_name[12:14] + '-dist.csv', dist_array, delimiter=',')

                self.mtx = mtx
                self.dist = dist
            else:
                self.mtx = None
                self.dist = None

    def undistort(self, img):
        if self.dist is not None and self.mtx is not None:
            h, w = img.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w, h), 1, (w, h))

            # unsdistor
            dst = cv.undistort(img, self.mtx, self.dist, None, newcameramtx)

            # crop image
            x, y, w, h = roi
            dst = dst[y:y + h, x:x + w]
            return dst

import cv2
import imutils

import csv

from camera_calibration import CameraCalibration
from centroidTracker import CentroidTracker
from os.path import exists


class BackgroundSubtractionKNN:
    outputFrame = None

    def __init__(self, source_name, resolution):
        self.video_name = 'video_files/' + source_name + '.MP4'
        self.camera_calibration = CameraCalibration(self.video_name)
        self.camera_calibration.calibrate()
        self.screenshot_name = 'screenshot_files/' + source_name
        self.ct = CentroidTracker()
        self.centroid_file = 'results/' + source_name + '-centroids.csv'
        self.window_size = resolution
        self.frames = []

    def get_screenshot(self):

        cap = cv2.VideoCapture(self.video_name)

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 40)
        img_counter = 0
        frame_counter = 0

        print("Press s to save picture or q to exit()")
        while cap.isOpened():
            # timer = cv2.getTickCount()
            success, img = cap.read()
            frame_counter += 1

            undistorted_img = self.camera_calibration.undistort(img)

            img_denoise = None

            # cv2.fastNlMeansDenoising(src=img, dst=img_denoise, h=2)
            if undistorted_img is not None:
                imS = cv2.resize(undistorted_img, self.window_size)

                if frame_counter in self.frames:
                    img_name = self.screenshot_name + '_' + str(img_counter) + '.png'
                    cv2.imwrite(img_name, imS)
                    print("{} written!".format(img_name))
                    img_counter += 1
                    if frame_counter == max(self.frames):
                        break

                if self.frames == []:
                    cv2.imshow("Pier cam undistorted", imS)

                wait_key = cv2.waitKey(1)
                if wait_key == 113:
                    break
                elif wait_key == 115:
                    # SPACE pressed
                    img_name = self.screenshot_name + '_' + str(img_counter) + '.png'
                    cv2.imwrite(img_name, imS)
                    print("{} written!".format(img_name))
                    img_counter += 1
                    self.frames.append(frame_counter)
        cv2.destroyAllWindows()
        cap.release()

    def subtractor(self, area, history, shadows, threshold):
        cap = cv2.VideoCapture(self.video_name)

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 40)

        bs_knn = cv2.createBackgroundSubtractorKNN(history=history, detectShadows=shadows, dist2Threshold=threshold)

        # tracker = cv2.TrackerMOSSE_create()
        while cap.isOpened():
            # timer = cv2.getTickCount()
            success, img = cap.read()
            # success2, img2 = cap2.read()

            # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            # cv2.putText(img, str(int(cap.get(cv2.CAP_PROP_FPS))), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.putText(img2, str(int(cap2.get(cv2.CAP_PROP_FPS))), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            if img is not None:
                # cv2.namedWindow("Pier cam", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions

                imS = cv2.resize(img, self.window_size)  # Resize image
                # imS2 = cv2.resize(img2, (960, 540))  # Resize image

                undistorted_img = self.camera_calibration.undistort(img)
                undistorted_img_s = cv2.resize(undistorted_img, self.window_size)

                cv2.rectangle(imS, (10, 2), (100, 20), (255, 255, 255), -1)
                cv2.putText(imS, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                cv2.imshow("Pier cam", imS)

                if undistorted_img_s is not None:
                    fgKnn = bs_knn.apply(undistorted_img_s)

                    cv2.namedWindow("Pier cam undistorted", cv2.WINDOW_NORMAL)
                    cv2.rectangle(undistorted_img_s, (10, 2), (100, 20), (255, 255, 255), -1)
                    cv2.putText(undistorted_img_s, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
                    cv2.namedWindow("Pier cam undistorted", cv2.WINDOW_NORMAL)
                    cv2.imshow("Pier cam undistorted", undistorted_img_s)

                    # fgKnn = bs_knn.apply(undistorted_img)

                    self.select_objects(area, cap, fgKnn, history)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        cv2.destroyAllWindows()
        cap.release()

    def select_objects(self, area, cap, fgKnn, history):
        if fgKnn is not None:
            fgKnnRs = self.get_centroid(area, fgKnn, cap, history)

            # cv2.namedWindow("Foreground", cv2.WINDOW_NORMAL)
            # cv2.rectangle(fgKnnRs, (10, 2), (140, 20), (255, 255, 255), -1)
            # cv2.putText(fgKnnRs, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
            # cv2.putText(fgKnnRs, str(int(cap.get(cv2.CAP_PROP_FPS))), (75, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            #             (0, 0, 0))
            # cv2.namedWindow("Foreground", cv2.WINDOW_NORMAL)
            cv2.imshow("Foreground", fgKnnRs)

    def get_centroid(self, area, fgKnnRs, cap, history):
        (contours, hierarchy) = cv2.findContours(fgKnnRs, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = []

        for idx, c in enumerate(contours):
            if cv2.contourArea(c) < area:
                continue

            if hierarchy[0, idx, 3] == -1:
                continue
            # print(hierarchy[0, idx, 3])

            # get bounding box from countour
            (x, y, w, h) = cv2.boundingRect(c)

            # draw bounding box
            cv2.rectangle(fgKnnRs, (x, y), (x + w, y + h), (100, 0, 255), 2)

            rects.append([x, y, x + w, y + h])

        # update our centroid tracker using the computed set of bounding
        # box rectangles
        objects = self.ct.update(rects)

        if objects is not None:

            for (objectID, centroid) in objects.items():
                # draw both the ID of the object and the centroid of the
                # object on the output frame

                if history < cap.get(cv2.CAP_PROP_POS_FRAMES):
                    text = "ID {}".format(objectID)
                    cv2.putText(fgKnnRs, text, (centroid[0] - 10, centroid[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    cv2.circle(fgKnnRs, (centroid[0], centroid[1]), 4, (255, 0, 0), -1)

                    self.save_centroids(float(cap.get(cv2.CAP_PROP_FPS)), int(cap.get(cv2.CAP_PROP_POS_FRAMES)), objectID,
                                        centroid[0], centroid[1])

        return fgKnnRs

    def create_centroids_file(self):
        header_list = ['fps', 'frame', 'Object ID', 'x', 'y']
        with open(self.centroid_file, 'w', encoding='UTF8', newline='') as f:
            dw = csv.DictWriter(f, delimiter=',', fieldnames=header_list)
            dw.writeheader()

    def save_centroids(self, fps, frame, object_id, x, y):

        with open(self.centroid_file, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            data = [fps, frame, object_id, x, y]
            writer.writerow(data)

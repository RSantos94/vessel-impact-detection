import os
import sys

import cv2

import csv

from cv2 import VideoCapture

from tools.camera_calibration import CameraCalibration
from external_libraries.centroidTracker import CentroidTracker


class BackgroundSubtractionKNN:
    outputFrame = None

    def __init__(self, source_name: str, resolution: (int, int), os_name: str):
        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        parent_path = os.path.dirname(path)

        if os_name == "Windows":
            self.video_name = parent_path + '\\video_files\\' + source_name + '.MP4'
            self.video_undistorted_name = parent_path + '\\video_files\\' + source_name + '-undistorted.MP4'
            self.screenshot_name = parent_path + '\\screenshot_files\\' + source_name
            self.centroid_file = parent_path + '\\results\\' + source_name + '-centroids.csv'
        else:
            self.video_name = 'video_files/' + source_name + '.MP4'
            self.video_undistorted_name = 'video_files/' + source_name + '-undistorted.MP4'
            self.screenshot_name = 'screenshot_files/' + source_name
            self.centroid_file = 'results/' + source_name + '-centroids.csv'

        self.camera_calibration = CameraCalibration(source_name, os_name)
        self.camera_calibration.calibrate()

        self.source_name = source_name
        self.ct = CentroidTracker()
        self.os_name = os_name
        self.window_size = resolution
        self.frames = []

    def create_undistorted_video_file(self):
        cap = cv2.VideoCapture(self.video_name)

        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        writer = cv2.VideoWriter(self.video_undistorted_name, fourcc, fps, size)

        while cap.isOpened():
            success, img = cap.read()

            if not success:
                break

            undistorted_img = self.camera_calibration.undistort(img)
            writer.write(undistorted_img)

        cv2.destroyAllWindows()
        cap.release()

    def get_screenshot(self):

        cap = cv2.VideoCapture(self.video_name)

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 40)
        img_counter = 0
        frame_counter = 0

        print("Press space to save picture or q to exit")
        while cap.isOpened():
            # timer = cv2.getTickCount()
            success, img = cap.read()
            frame_counter += 1

            if img is not None:
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
                    elif wait_key == 32:
                        # SPACE pressed
                        img_name = self.screenshot_name + '_' + str(img_counter) + '.png'
                        img_original_name = self.screenshot_name + '_original_' + str(img_counter) + '.png'
                        cv2.imwrite(img_name, imS)
                        cv2.imwrite(img_original_name, img)
                        print("{} written!".format(img_name))
                        print("{} written!".format(img_original_name))
                        img_counter += 1
                        self.frames.append(frame_counter)

                else:
                    print("Calibration failed!")

        cv2.destroyAllWindows()
        cap.release()

    def subtractor(self, is_test: bool):

        history, detect_shadows, dist_2_threshold, centroid_object_min_area = self.get_bs_param(self.source_name)
        cap = cv2.VideoCapture(self.video_name)

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 40)

        bs_knn = cv2.createBackgroundSubtractorKNN(history=history, detectShadows=detect_shadows,
                                                   dist2Threshold=dist_2_threshold)

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

                    self.select_objects(centroid_object_min_area, cap, fgKnn, history, is_test)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        cv2.destroyAllWindows()
        cap.release()

    def select_objects(self, area: int, cap: VideoCapture, fg_knn, history: int, is_test: bool):
        if fg_knn is not None:
            fg_knn_rs = self.get_centroid(area, fg_knn, cap, history, is_test)

            # cv2.namedWindow("Foreground", cv2.WINDOW_NORMAL)
            # cv2.rectangle(fg_knn_rs, (10, 2), (140, 20), (255, 255, 255), -1)
            # cv2.putText(fg_knn_rs, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
            # cv2.putText(fg_knn_rs, str(int(cap.get(cv2.CAP_PROP_FPS))), (75, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            #             (0, 0, 0))
            # cv2.namedWindow("Foreground", cv2.WINDOW_NORMAL)
            cv2.imshow("Foreground", fg_knn_rs)

    def get_centroid(self, area: int, fg_knn_rs, cap: VideoCapture, history: int, is_test: bool):
        (contours, hierarchy) = cv2.findContours(fg_knn_rs, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
            cv2.rectangle(fg_knn_rs, (x, y), (x + w, y + h), (100, 0, 255), 2)

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
                    cv2.putText(fg_knn_rs, text, (centroid[0] - 10, centroid[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    cv2.circle(fg_knn_rs, (centroid[0], centroid[1]), 4, (255, 0, 0), -1)

                    if not is_test:
                        self.save_centroids(float(cap.get(cv2.CAP_PROP_FPS)), int(cap.get(cv2.CAP_PROP_POS_FRAMES)),
                                            objectID,
                                            centroid[0], centroid[1])

        return fg_knn_rs

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

    def get_bs_param(self, source_name):
        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        parent_path = os.path.dirname(path)

        if self.os_name == "Windows":
            bs_config_file_name = parent_path + '\\config\\' + source_name + '-backgroundsubtractor.txt'
        else:
            bs_config_file_name = 'config/' + source_name + '-backgroundsubtractor.txt'

        try:
            f = open(bs_config_file_name, "r")
            for x in f:
                arr = x.split(':')
                if arr[0] == 'History':
                    history_param = int(arr[1].strip())
                elif arr[0] == 'Detect Shadows':
                    if arr[1].strip().capitalize() == 'TRUE':
                        detect_shadows_param = True
                    else:
                        detect_shadows_param = False
                elif arr[0] == 'Distance To Threshold':
                    dist_2_threshold_param = int(arr[1].strip())
                elif arr[0] == 'Object min area':
                    object_min_area_param = int(arr[1].strip())

            return history_param, detect_shadows_param, dist_2_threshold_param, object_min_area_param

        except FileNotFoundError:
            print('O ficheiro ' + source_name + '-backgroundsubtractor.txt não existe!')
            sys.exit(0)

    def get_screenshot_tool(self):

        cap = cv2.VideoCapture(self.video_name)

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 40)
        img_counter = 0
        frame_counter = 0

        print("Press space to save picture or q to exit")
        while cap.isOpened():
            success, img = cap.read()
            frame_counter += 1

            if img is not None:
                undistorted_img = self.camera_calibration.undistort(img)

                if undistorted_img is not None:
                    imS = cv2.resize(undistorted_img, self.window_size)
                    height = img.shape[0]
                    width = img.shape[1]
                    undistorted_img_resized = cv2.resize(undistorted_img, (width, height))

                    cv2.imshow("Pier cam undistorted", imS)

                    wait_key = cv2.waitKey(1)
                    if wait_key == 113:
                        break
                    elif wait_key == 32:
                        # SPACE pressed
                        img_name = self.screenshot_name + '_' + str(img_counter) + '.png'
                        img_original_name = self.screenshot_name + '_' + str(img_counter) + '_original.png'
                        cv2.imwrite(img_name, undistorted_img_resized)
                        cv2.imwrite(img_original_name, img)
                        print("{} written!".format(img_name))
                        print("{} written!".format(img_original_name))
                        img_counter += 1

                else:
                    print("Calibration failed!")

        cv2.destroyAllWindows()
        cap.release()
import csv
import math
import os
import statistics
from os.path import exists

import numpy as np
from scipy.interpolate import UnivariateSpline

from external_libraries.spline import get_natural_cubic_spline_model
from tools import reports


def is_between_equations(obj_x, obj_y, m1, m2, b1, b2):
    are_fields_empty = m1 is not None and m2 is not None and b1 is not None and b2 is not None
    return True #Comment if equations should be considered
    if are_fields_empty:
        if obj_y >= m2 * obj_x + b2 and obj_y >= m1 * obj_x + b1:
            return True
        else:
            return False
    else:
        return True


def get_list_distances(list_x, list_y):
    temp_x = None
    temp_y = None
    list_distances = []
    i = 0
    while i < len(list_x):
        if temp_x is None:
            temp_x = list_x[i]
            temp_y = list_y[i]
        else:
            prev = [temp_x, temp_y]
            curr = [list_x[i], list_y[i]]
            distance = math.dist(prev, curr)
            list_distances.append(distance)
            temp_x = list_x[i]
            temp_y = list_y[i]
        i += 1

    return list_distances


def remove_outliers(orig_list_x, orig_list_y, orig_list_frames, distance_stdev):
    temp_x = None
    temp_y = None
    list_x = []
    list_y = []
    list_frames = []
    i = 0
    while i < len(orig_list_x):
        if temp_x is None:
            temp_x = orig_list_x[i]
            temp_y = orig_list_y[i]
            list_x.append(orig_list_x[i])
            list_y.append(orig_list_y[i])
            list_frames.append(orig_list_frames[i])
        else:
            prev = [temp_x, temp_y]
            curr = [orig_list_x[i], orig_list_y[i]]
            distance = math.dist(prev, curr)
            if distance < distance_stdev:
                list_x.append(orig_list_x[i])
                list_y.append(orig_list_y[i])
                list_frames.append(orig_list_frames[i])
                temp_x = orig_list_x[i]
                temp_y = orig_list_y[i]
        i += 1

    return list_x, list_y, list_frames


class InterpolateCentroids:

    def __init__(self, source, os_name):
        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        parent_path = os.path.dirname(path)
        if os_name == "Windows":
            # D:\git\\vessel-impact-detection\\
            self.centroid_file = parent_path + '\\results\\' + source + '-centroids.csv'
            self.interpolated_centroid_file = parent_path + '\\results\\' + source + '-interpolated_centroids.csv'
            self.referential_points_file = parent_path + '\\config\\' + source + '-referential-points.txt'

        else:
            self.centroid_file = 'results/' + source + '-centroids.csv'
            self.interpolated_centroid_file = 'results/' + source + '-interpolated_centroids.csv'
            self.referential_points_file = 'config/' + source + '-referential-points.txt'

        self.objects_to_track = []
        self.source = source

    def execute(self):
        if self.has_points_file(self.centroid_file):
            self.interpolate_file(self.centroid_file, self.objects_to_track, self.source)
        else:
            print('O ficheiro ' + self.centroid_file + ' não existe')

    def has_points_file(self, source):
        return exists(source)

    def interpolate_file(self, file, objects_to_track, source):
        with open(file, encoding='UTF8') as f:
            reader = csv.DictReader(f)
            result = sorted(reader, key=lambda d: (int(d['Object ID']), float(d['frame'])))

            curr_object = None
            curr_min_frame = None
            curr_max_frame = None
            fps = None
            curr_object_x = []
            curr_object_y = []
            curr_object_frames = []

            if self.has_points_file(self.referential_points_file):
                m1 = None
                m2 = None
                b1 = None
                b2 = None
                f = open(self.referential_points_file, "r")
                for x in f:
                    arr = x.split(':')
                    if arr[0] == 'm limite':
                        m1_string = arr[1].strip()
                        if m1_string != "":
                            m1 = float(m1_string)
                    elif arr[0] == 'm cais':
                        m2_string = arr[1].strip()
                        if m2_string != "":
                            m2 = float(m2_string)
                    elif arr[0] == 'b limite':
                        b1_string = arr[1].strip()
                        if b1_string != "":
                            b1 = float(b1_string)
                    elif arr[0] == 'b cais':
                        b2_string = arr[1].strip()
                        if b2_string != "":
                            b2 = float(b2_string)

            for a in result:
                if fps is None:
                    fps = a['fps']

                if curr_object is None and a['Object ID'] in objects_to_track:
                    curr_object = a['Object ID']

                if curr_object is not None:
                    if a['Object ID'] == curr_object:
                        obj_x = float(a['x'])
                        obj_y = float(a['y'])
                        obj_frame = int(float(a['frame']))

                        if self.has_points_file(self.referential_points_file):

                            if is_between_equations(obj_x, obj_y, m1, m2, b1, b2):
                                curr_object_x.append(obj_x)
                                curr_object_y.append(obj_y)
                                curr_object_frames.append(obj_frame)
                        else:
                            curr_object_x.append(obj_x)
                            curr_object_y.append(obj_y)
                            curr_object_frames.append(obj_frame)

                        if curr_min_frame is None:
                            curr_min_frame = float(a['frame'])

                        if curr_max_frame is None:
                            curr_max_frame = float(a['frame'])

                        if curr_min_frame > float(a['frame']):
                            curr_min_frame = float(a['frame'])

                        if curr_max_frame < float(a['frame']):
                            curr_max_frame = float(a['frame'])

                    elif a['Object ID'] != curr_object:
                        if curr_object in objects_to_track:
                            # list_x, list_y, list_frames = self.remove_duplicates(curr_object_x, curr_object_y,
                            #                                                     curr_object_frames)

                            x_stdev = statistics.stdev(curr_object_x)
                            y_stdev = statistics.stdev(curr_object_y)
                            distances = get_list_distances(curr_object_x, curr_object_y)
                            distance_stdev = statistics.stdev(distances)

                            list_x, list_y, list_frames = remove_outliers(curr_object_x, curr_object_y, curr_object_frames, distance_stdev)

                            array_list_x = np.array(list_x)
                            array_list_y = np.array(list_y)
                            array_list_frames = np.array(list_frames)


                            #self.spline(array_list_x, array_list_y, array_list_frames, source, curr_object + "-outliered", fps)

                            array_x = np.array(curr_object_x)
                            array_y = np.array(curr_object_y)
                            array_frames = np.array(curr_object_frames)

                            # array_x = np.array(list_x)
                            # array_y = np.array(list_y)
                            # array_frames = np.array(list_frames)
                            x, y, all_frames = self.spline(array_x, array_y, array_frames, source, curr_object, fps)

                            points = self.stack_coordinates(x, y)

                            distance = self.cumulative_sum(points)
                            distance = self.calc_distance(distance)

                            self.choose_impact_period(x, y)

                            x_1d = self.calc_first_derivative(np.array(all_frames), np.array(x))
                            x_2d = self.calc_second_derivative(np.array(all_frames), np.array(x))
                            y_1d = self.calc_first_derivative(np.array(all_frames), np.array(y))
                            y_2d = self.calc_second_derivative(np.array(all_frames), np.array(y))

                            reports.derivate_report(x_1d(np.array(all_frames)), x_2d(np.array(all_frames)),
                                                    y_1d(np.array(all_frames)), y_2d(np.array(all_frames)),
                                                    np.array(all_frames), source, curr_object)

                            # reports.spline_report(array_x, array_y, np.array(all_frames), x, y, source, curr_object, fps)
                            # Build a list of the spline function, one for each dimension:
                            # splines = self.calc_splines(distance, points)

                            # points_fitted = np.vstack(spl(curr_object_frames) for spl in splines).T

                            # for cent in points_fitted:

                            # frames = np.arrange(curr_min_frame, curr_max_frame, 1)
                            # res = interpolate.bisplrep(curr_object_x, curr_object_y, frames)
                            curr_object_x = []
                            curr_object_y = []
                            curr_object_frames = []

                        curr_object = None


            if curr_object in objects_to_track:
                # list_x, list_y, list_frames = self.remove_duplicates(curr_object_x, curr_object_y,
                #                                                     curr_object_frames)

                x_stdev = statistics.stdev(curr_object_x)
                y_stdev = statistics.stdev(curr_object_y)
                distances = get_list_distances(curr_object_x, curr_object_y)
                distance_stdev = statistics.stdev(distances)

                list_x, list_y, list_frames = remove_outliers(curr_object_x, curr_object_y, curr_object_frames,
                                                              distance_stdev)

                array_list_x = np.array(list_x)
                array_list_y = np.array(list_y)
                array_list_frames = np.array(list_frames)

                # self.spline(array_list_x, array_list_y, array_list_frames, source, curr_object + "-outliered", fps)

                array_x = np.array(curr_object_x)
                array_y = np.array(curr_object_y)
                array_frames = np.array(curr_object_frames)

                # array_x = np.array(list_x)
                # array_y = np.array(list_y)
                # array_frames = np.array(list_frames)
                x, y, all_frames = self.spline(array_x, array_y, array_frames, source, curr_object, fps)

                points = self.stack_coordinates(x, y)

                distance = self.cumulative_sum(points)
                distance = self.calc_distance(distance)

                self.choose_impact_period(x, y)

                x_1d = self.calc_first_derivative(np.array(all_frames), np.array(x))
                x_2d = self.calc_second_derivative(np.array(all_frames), np.array(x))
                y_1d = self.calc_first_derivative(np.array(all_frames), np.array(y))
                y_2d = self.calc_second_derivative(np.array(all_frames), np.array(y))

                reports.derivate_report(x_1d(np.array(all_frames)), x_2d(np.array(all_frames)),
                                        y_1d(np.array(all_frames)), y_2d(np.array(all_frames)),
                                        np.array(all_frames), source, curr_object)

                # reports.spline_report(array_x, array_y, np.array(all_frames), x, y, source, curr_object, fps)
                # Build a list of the spline function, one for each dimension:
                # splines = self.calc_splines(distance, points)

                # points_fitted = np.vstack(spl(curr_object_frames) for spl in splines).T

                # for cent in points_fitted:

                # frames = np.arrange(curr_min_frame, curr_max_frame, 1)
                # res = interpolate.bisplrep(curr_object_x, curr_object_y, frames)
                curr_object_x = []
                curr_object_y = []
                curr_object_frames = []

    def spline(self, x=None, y=None, frames=None, source=None, current=None, frame_rate=None):
        nodes = max(frames) - min(frames)

        spline_x = get_natural_cubic_spline_model(x=frames, y=x, minval=min(frames), maxval=max(frames),
                                                  n_knots=int(nodes / 2))
        spline_y = get_natural_cubic_spline_model(x=frames, y=y, minval=min(frames), maxval=max(frames),
                                                  n_knots=int(nodes / 2))

        all_frames = np.arange(min(frames), max(frames), 1)
        x_est = spline_x.predict(all_frames)
        y_est = spline_y.predict(all_frames)

        reports.spline_report(x=x, y=y, frames=frames, splined_x=x_est, splined_y=y_est, source=source, current=current,
                              frame_rate=frame_rate)

        return x_est, y_est, all_frames

    def stack_coordinates(self, x, y):
        return np.vstack((x, y)).T

    def difference(self, points):
        return np.diff(points, axis=0)

    def sum(self, points):
        return np.sum(self.difference(points) ** 2, axis=1)

    def square(self, points):
        return np.sqrt(self.sum(points))

    def cumulative_sum(self, points):
        return np.cumsum(self.square(points))

    def calc_distance(self, distance):
        return np.insert(distance, 0, 0) / distance[-1]

    def choose_impact_period(self, x, y):
        window = []

        return window

    def calc_first_derivative(self, x, y):
        y_spl = UnivariateSpline(x, y, s=0, k=4)
        y_spl_1d = y_spl.derivative(n=1)
        return y_spl_1d

    def calc_second_derivative(self, x, y):
        y_spl = UnivariateSpline(x, y, s=0, k=4)
        y_spl_2d = y_spl.derivative(n=2)
        return y_spl_2d

    def remove_duplicates(self, x, y, frames):
        previous_x = None
        previous_y = None
        list_x = []
        list_y = []
        list_frames = []
        for i in range(len(x)):
            if previous_x is None and previous_y is None:
                previous_x = x[i]
                previous_y = y[i]
                list_x.append(x[i])
                list_y.append(y[i])
                list_frames.append(frames[i])
            else:
                if previous_x != x[i] and previous_y != y[i]:
                    previous_x = x[i]
                    previous_y = y[i]
                    list_x.append(x[i])
                    list_y.append(y[i])
                    list_frames.append(frames[i])

        return list_x, list_y, list_frames

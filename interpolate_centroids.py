from os.path import exists
import csv
import numpy as np

import reports
import os

from spline import get_natural_cubic_spline_model


class InterpolateCentroids:

    def __init__(self, source1, source2, os_name):
        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        if os_name == "Windows":
            # D:\git\\vessel-impact-detection\\
            self.centroid_file_1 = path + '\\results\\' + source1 + '-centroids.csv'
            self.centroid_file_2 = path + '\\results\\' + source2 + '-centroids.csv'
            self.interpolated_centroid_file_1 = path + '\\results\\' + source1 + '-interpolated_centroids.csv'
            self.interpolated_centroid_file_2 = path + '\\results\\' + source2 + '-interpolated_centroids.csv'

        else:
            self.centroid_file_1 = 'results/' + source1 + '-centroids.csv'
            self.centroid_file_2 = 'results/' + source2 + '-centroids.csv'
            self.interpolated_centroid_file_1 = 'results/' + source1 + '-interpolated_centroids.csv'
            self.interpolated_centroid_file_2 = 'results/' + source2 + '-interpolated_centroids.csv'

        self.objects_to_track1 = []
        self.objects_to_track2 = []
        self.source1 = source1
        self.source2 = source2

    def execute(self):
        if self.has_points_file(self.centroid_file_1):
            self.interpolate_file(self.centroid_file_1, self.objects_to_track1, self.source1)
        else:
            print('O ficheiro ' + self.centroid_file_1 + ' não existe')
        if self.has_points_file(self.centroid_file_2):
            self.interpolate_file(self.centroid_file_2, self.objects_to_track2, self.source2)
        else:
            print('O ficheiro ' + self.centroid_file_2 + ' não existe')

    def has_points_file(self, source):
        return exists(source)

    def interpolate_file(self, file, objects_to_track, source):
        with open(file, encoding='UTF8') as f:
            reader = csv.DictReader(f)
            result = sorted(reader, key=lambda d: (int(d['Object ID']), int(d['frame'])))

            curr_object = None
            curr_min_frame = None
            curr_max_frame = None
            fps = None
            curr_object_x = []
            curr_object_y = []
            curr_object_frames = []
            for a in result:
                if fps is None:
                    fps = a['fps']

                if curr_object is None and a['Object ID'] in objects_to_track:
                    curr_object = a['Object ID']

                if curr_object is not None:
                    if a['Object ID'] == curr_object:
                        curr_object_x.append(float(a['x']))
                        curr_object_y.append(float(a['y']))
                        curr_object_frames.append(int(a['frame']))

                        if curr_min_frame is None:
                            curr_min_frame = a['frame']

                        if curr_max_frame is None:
                            curr_max_frame = a['frame']

                        if curr_min_frame > a['frame']:
                            curr_min_frame = a['frame']

                        if curr_max_frame < a['frame']:
                            curr_max_frame = a['frame']

                    elif a['Object ID'] != curr_object:
                        list_x, list_y, list_frames = self.remove_duplicates(curr_object_x, curr_object_y,
                                                                             curr_object_frames)

                        array_x = np.array(list_x)
                        array_y = np.array(list_y)
                        array_frames = np.array(list_frames)
                        x, y = self.spline(array_x, array_y, array_frames, source, curr_object)

                        points = self.stack_coordinates(x, y)

                        distance = self.cumulative_sum(points)
                        distance = self.calc_distance(distance)

                        # Build a list of the spline function, one for each dimension:
                        # splines = self.calc_splines(distance, points)

                        # points_fitted = np.vstack(spl(curr_object_frames) for spl in splines).T

                        # for cent in points_fitted:

                        # frames = np.arrange(curr_min_frame, curr_max_frame, 1)
                        # res = interpolate.bisplrep(curr_object_x, curr_object_y, frames)
                        curr_object_x = []
                        curr_object_y = []
                        curr_object_frames = []
                        curr_object = a['Object ID']

    def spline(self, x=None, y=None, frames=None, source=None, current=None):
        nodes = max(frames) - min(frames)

        spline_x = get_natural_cubic_spline_model(x=frames, y=x, minval=min(frames), maxval=max(frames),
                                                  n_knots=nodes)
        spline_y = get_natural_cubic_spline_model(x=frames, y=y, minval=min(frames), maxval=max(frames),
                                                  n_knots=nodes)
        x_est = spline_x.predict(frames)
        y_est = spline_y.predict(frames)

        return x_est, y_est

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

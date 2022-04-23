from os.path import exists
import csv
import numpy as np
import spline
import os

from csaps import csaps

from scipy.interpolate import UnivariateSpline


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

    def execute(self):
        if self.has_points_file(self.centroid_file_1):
            self.interpolate_file(self.centroid_file_1, self.objects_to_track1)
        else:
            print('O ficheiro ' + self.centroid_file_1 + ' não existe')
        if self.has_points_file(self.centroid_file_2):
            self.interpolate_file(self.centroid_file_2, self.objects_to_track1)
        else:
            print('O ficheiro ' + self.centroid_file_2 + ' não existe')

    def has_points_file(self, source):
        return exists(source)

    def interpolate_file(self, file, objects_to_track):
        with open(file, encoding='UTF8') as f:
            reader = csv.DictReader(f)
            result = sorted(reader, key=lambda d: (int(d['Object ID']), int(d['frame'])))

            curr_object = None
            curr_min_frame = None
            curr_max_frame = None
            fps = None
            curr_object_x = []
            curr_object_y = []
            frames = []
            for a in result:
                if fps is None:
                    fps = a['fps']

                if curr_object is None and a['Object ID'] in objects_to_track:
                    curr_object = a['Object ID']

                if curr_object is not None:
                    if a['Object ID'] == curr_object:
                        curr_object_x.append(float(a['x']))
                        curr_object_y.append(float(a['y']))
                        frames.append(int(a['frame']))

                        if curr_min_frame is None:
                            curr_min_frame = a['frame']

                        if curr_max_frame is None:
                            curr_max_frame = a['frame']

                        if curr_min_frame > a['frame']:
                            curr_min_frame = a['frame']

                        if curr_max_frame < a['frame']:
                            curr_max_frame = a['frame']

                    elif a['Object ID'] != curr_object:
                        knots = int(curr_max_frame) - int(curr_min_frame) + 1

                        np.random.seed(1234)
                        theta = np.linspace(0, 2 * np.pi, 35)
                        x = np.array(curr_object_x)
                        y = np.array(curr_object_y)
                        data = [x, y]
                        theta_i = np.linspace(0, 2 * np.pi, 200)

                        data_i = self.spline(x, y, theta_i, smooth=0.95)

                        points = self.stack_coordinates(curr_object_x, curr_object_y)

                        distance = self.cumulative_sum(points)
                        distance = self.calc_distance(distance)

                        # Build a list of the spline function, one for each dimension:
                        splines = self.calc_splines(distance, points)

                        points_fitted = np.vstack(spl(frames) for spl in splines).T

                        # for cent in points_fitted:

                        # frames = np.arange(curr_min_frame, curr_max_frame, 1)
                        # res = interpolate.bisplrep(curr_object_x, curr_object_y, frames)
                        curr_object_x = []
                        curr_object_x = []
                        frames = []
                        curr_object = a['Object ID']

    def spline(self, theta=None, data=None, theta_i=None, smooth=None):
        return csaps(theta, data, theta_i, smooth)

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

    def calc_splines(self, distance, points):
        return [UnivariateSpline(distance, coords, k=3, s=.2) for coords in points.T]

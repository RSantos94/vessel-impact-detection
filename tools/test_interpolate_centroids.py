from unittest import TestCase

import numpy as np

from tools.interpolate_centroids import InterpolateCentroids


class TestInterpolateCentroids(TestCase):
    def test_spline(self):
        ic = InterpolateCentroids("source1", "source2", "os_name")
        np.random.seed(1234)
        theta = np.linspace(0, 2 * np.pi, 35)
        x = np.cos(theta) + np.random.randn(35) * 0.1
        y = np.sin(theta) + np.random.randn(35) * 0.1
        data = [x, y]
        theta_i = np.linspace(0, 2 * np.pi, 200)

        data_i = ic.spline(theta, data, theta_i, 0.95)
        assert data_i is not None

    def test_remove_duplicates(self):
        ic = InterpolateCentroids("source1", "source2", "os_name")
        x = [2, 3, 3, 4, 5, 6, 7]
        y = [1, 4, 4, 6, 8, 5, 8]
        list_x, list_y = ic.remove_duplicates(x, y)

        assert list_x == [2, 3, 4, 5, 6, 7]
        assert list_y == [1, 4, 6, 8, 5, 8]

    def test_split_increasing_x(self):
        ic = InterpolateCentroids("source1", "source2", "os_name")
        x = [2, 3, 4, 5, 6, 7, 6, 5, 4, 6, 8]
        y = [1, 4, 6, 8, 5, 8, 7, 4, 2, 4, 7]
        res_x, res_y, directions = ic.split_increasing_x(x, y)
        assert res_x == [[2, 3, 4, 5, 6, 7], [6, 5, 4], [6, 8]]
        assert res_y == [[1, 4, 6, 8, 5, 8], [7, 4, 2], [4, 7]]
        assert directions == [1, -1, 1]

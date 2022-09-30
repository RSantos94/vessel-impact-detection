import math

import numpy as np
from scipy.interpolate import UnivariateSpline

from tools import reports


def calc_first_derivative(x, y):
    y_spl = UnivariateSpline(x, y, s=0, k=4)
    y_spl_1d = y_spl.derivative(n=1)
    return y_spl_1d


def calc_second_derivative(x, y):
    y_spl = UnivariateSpline(x, y, s=0, k=4)
    y_spl_2d = y_spl.derivative(n=2)
    return y_spl_2d


def get_impact_moment(x_1d, y_1d, time_list):
    pass


class CalculatePhysics:

    def __init__(self, coordinates: list, frame_rate: list, time_list: list, mass: float, source: str, object: str):
        self.coordinates = coordinates
        self.frame_rate = frame_rate
        self.time_list = time_list
        self.mass = mass
        self.source = source
        self.object = object

    def execute(self):
        x = []
        y = []
        for coordinate in self.coordinates:
            x.append(coordinate[0])
            y.append(coordinate[1])

        x_1d = calc_first_derivative(np.array(self.time_list), np.array(x))
        x_2d = calc_second_derivative(np.array(self.time_list), np.array(x))
        y_1d = calc_first_derivative(np.array(self.time_list), np.array(y))
        y_2d = calc_second_derivative(np.array(self.time_list), np.array(y))

        # times = get_impact_moment(x_1d, y_1d, self.time_list)

        # i: int = 0

        # x_acc_list = []
        # y_acc_list = []
        # for time in self.time_list:
        #     if time in times:
        #         x_acc_list.append(x_2d(np.array(self.time_list))[i])
        #         y_acc_list.append(y_2d(np.array(self.time_list))[i])
        #     i += 1

        reports.real_units_derivate_report(x_1d(np.array(self.time_list)), x_2d(np.array(self.time_list)),
                                           y_1d(np.array(self.time_list)), y_2d(np.array(self.time_list)),
                                           np.array(self.time_list), self.source, self.object)
        i = 0
        max_x = min(x_2d(np.array(self.time_list)))
        max_y_list = []
        max_x_pos_list = []
        for i in range(0, x_2d(np.array(self.time_list)).size):
            if x_2d(np.array(self.time_list))[i] == max_x:
                max_x_pos_list.append(i)

        for i in range(0, y_2d(np.array(self.time_list)).size):
            if i in max_x_pos_list:
                max_y_list.append(y_2d(np.array(self.time_list))[i])

        max_y = min(max_y_list)

        max_acc = math.sqrt(max_x ** 2 + max_y ** 2)

        max_force = max_acc * self.mass

        return max_acc, max_force

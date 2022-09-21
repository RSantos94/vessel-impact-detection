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


class CalculatePhysics:

    def __init__(self, coordinates :list, frame_rate: list, time_list: list, mass: float):
        self.coordinates = coordinates
        self.frame_rate = frame_rate
        self.time_list = time_list
        self.mass = mass

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

        reports.derivate_report(x_1d(np.array(self.time_list)), x_2d(np.array(self.time_list)),
                                y_1d(np.array(self.time_list)), y_2d(np.array(self.time_list)),
                                np.array(self.time_list), "boat", "test")

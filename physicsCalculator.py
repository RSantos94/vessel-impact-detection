import numpy as np

class PhysicsCalculator:

    @staticmethod
    def calculate_acceleration(distance, initial_velocity, start_time, end_time):
        return (2 * (distance - initial_velocity * (end_time - start_time))) / (end_time - start_time) ** 2

    @staticmethod
    def calculate_force(acceleration, mass):
        return acceleration * mass

    @staticmethod
    def calculate_3d_distance(start_x, start_y, start_z, end_x, end_y, end_z):
        start = np.array([start_x, start_y, start_z])
        end = np.array([end_x, end_y, end_z])

        squared_dist = np.sum((start - end) ** 2, axis=0)
        return np.sqrt(squared_dist)

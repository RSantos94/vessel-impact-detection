import csv
import os
import platform

from tools import reports

if __name__ == '__main__':
    os_name = platform.system()
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    parent_path = os.path.dirname(path)
    if os_name == "Windows":
        # D:\git\\vessel-impact-detection\\
        acc_number = 'acc002'
        file_location = parent_path + '\\Data collection\\teste piscina 1\\data-' + acc_number + '.csv'
        report_location = parent_path + '\\reports\\accelometer-' + acc_number + '\\'

    else:
        acc_number = 'acc002'
        file_location = '/Data collection/teste piscina 1/data-' + acc_number + '.csv'
        report_location = '/reports/accelometer-' + acc_number + '/'

    with open(file_location, encoding='UTF8') as f:
        reader = csv.DictReader(f)

        x_acceleration_list = []
        y_acceleration_list = []
        z_acceleration_list = []
        gyro_x_list = []
        gyro_y_list = []
        gyro_z_list = []
        timestamp_list = []

        start_cutoff = 50000
        end_cutoff = 251000

        for row in reader:

            if start_cutoff <= int(row[' Hour ']) <= end_cutoff:
                x_acceleration = row[' acceleration x(*1000)'].strip()
                y_acceleration = row[' acceleration y(*1000)'].strip()
                z_acceleration = row[' acceleration z(*1000)'].strip()
                gyro_x = row[' gyro x'].strip()
                gyro_y = row[' gyro y'].strip()
                gyro_z = row[' gyro z'].strip()
                timestamp = row[' Hour ']
                x_acceleration_list.append(float(x_acceleration))
                y_acceleration_list.append(float(y_acceleration))
                z_acceleration_list.append(float(z_acceleration))
                gyro_x_list.append(float(gyro_x))
                gyro_y_list.append(float(gyro_y))
                gyro_z_list.append(float(gyro_z))
                timestamp_list.append(float(timestamp))

        reports.accelerometer_report(x_acceleration_list, y_acceleration_list, z_acceleration_list, gyro_x_list,
                                     gyro_y_list, gyro_z_list, timestamp_list, report_location)

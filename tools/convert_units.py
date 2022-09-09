import csv
import math
import os

from external_libraries.transforma import Transforma


def vertical_equation_1_y(x):
    return 0.5288461538461539 * x + -255.56730769230762


def vertical_equation_1_x(y):
    return 1 / 55 * (104 * y + 26579)


def vertical_equation_2_y(x):
    return 0.4906937394247039 * x + -168.52961082910315


def vertical_equation_2_x(y):
    return 1 / 290 * (591 * y + 99601)


def vertical_equation_3_y(x):
    return 0.44954128440366975 * x + -77.0733944954128


def vertical_equation_3_x(y):
    return 1 / 49 * (109 * y + 8401)


def horizontal_equation_1_y(x):
    return -0.3359375 * x + -1392.5625


def horizontal_equation_1_x(y):
    return -8 / 43 * (16 * y + 22281)


def horizontal_equation_2_y(x):
    return -0.402 * x + -1625.778


def horizontal_equation_2_x(y):
    return 1 / 201 * (-500 * y - 812889)


def horizontal_equation_3_y(x):
    return -0.46445497630331756 * x + -1898.7962085308056


def horizontal_equation_3_x(y):
    return 1 / 98 * (-211 * y - 400646)


def horizontal_equation_4_y(x):
    return -0.5090634441087614 * x + -2173.567975830816


def horizontal_equation_4_x(y):
    return -2 / 337 * (331 * y + 719451)


def horizontal_equation_5_y(x):
    return -0.7067901234567902 * x + -2819.6388888888887


def horizontal_equation_5_x(y):
    return -9 / 229 * (36 * y + 101507)


def get_conversion_tax(x, y):
    x_tax = 0
    y_tax = 0
    if x >= vertical_equation_1_x(y):
        if x <= vertical_equation_2_x(y):
            if y >= horizontal_equation_1_y(x):
                if y <= horizontal_equation_2_y(x):
                    x_tax = 13.8
                    y_tax = 17.6
                if y > horizontal_equation_2_y(x) & y <= horizontal_equation_3_y(x):
                    x_tax = 13.8534062288478
                    y_tax = 7.77662211910784
                if y > horizontal_equation_3_y(x) & y <= horizontal_equation_4_y(x):
                    x_tax = 10.9307358597075
                    y_tax = 9, 22370449148347
                if y > horizontal_equation_4_y(x) & y <= horizontal_equation_5_y(x):
                    x_tax = 11.1578287602909
                    y_tax = 10.7634309422517

        if x > vertical_equation_2_x(y) & x <= vertical_equation_3_x(y):
            if y >= horizontal_equation_1_y(x):
                if y <= horizontal_equation_2_y(x):
                    x_tax = 13.7
                    y_tax = 15.7
                if y > horizontal_equation_2_y(x) & y <= horizontal_equation_3_y(x):
                    x_tax = 8.69944666756153
                    y_tax = 12.6199400713572
                if y > horizontal_equation_3_y(x) & y <= horizontal_equation_4_y(x):
                    x_tax = 9.20485083268829
                    y_tax = 10.0130731695277
                if y > horizontal_equation_4_y(x) & y <= horizontal_equation_5_y(x):
                    x_tax = 9.58772194898971
                    y_tax = 10.8169383581764
    return x_tax, y_tax


def get_distances(x1, x2, y1, y2):
    x_dist = math.dist([x1], [x2])
    y_dist = math.dist([y1], [y2])
    points_dist = math.dist([x1, y1], [x2, y2])

    return x_dist, y_dist, points_dist


def get_distance_tax(x1, x2, y1, y2):
    tax_point_x_1, tax_point_y_1 = get_conversion_tax(x1, y1)
    tax_point_x_2, tax_point_y_2 = get_conversion_tax(x2, y2)

    tax_point_x = (tax_point_x_1 + tax_point_x_2) / 2
    tax_point_y = (tax_point_y_1 + tax_point_y_2) / 2

    return tax_point_x, tax_point_y


def create_csv(x: list, y: list, cartesian: list, csv_name: str):
    x_label = 'x distance'
    y_label = 'y distance'
    cartesian_label = 'cartesian distance'
    header_list = [x_label, y_label]
    if cartesian is not None:
        header_list.append(cartesian_label)
    with open(csv_name, 'w', encoding='UTF8', newline='') as f:
        dw = csv.DictWriter(f, delimiter=',', fieldnames=header_list)
        dw.writeheader()

        i = 0
        while i < len(x):
            if cartesian:
                dw.writerow({x_label: x[i], y_label: y[i], cartesian_label: cartesian[i]})
            else:
                dw.writerow({x_label: x[i], y_label: y[i]})
            i += 1


class ConvertUnits:
    def __init__(self, source, object_name, os_name):
        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        parent_path = os.path.dirname(path)
        if os_name == "Windows":
            # D:\git\\vessel-impact-detection\\
            self.interpolated_centroid_file = parent_path + '\\reports\\' + source + '\\object-' + object_name + '\\spline-xy-graph.csv'
            self.distances_file = parent_path + '\\results\\' + source + '-object-' + object_name + '-distances.csv'
            self.real_distances_file = parent_path + '\\results\\' + source + '-object-' + object_name + '-real-distances.csv'

        else:
            self.interpolated_centroid_file = 'reports/' + source + '/object-' + object_name + '/spline-tx-graph.csv'

        self.objects_to_track = []
        self.source = source

    def execute(self):
        temp = None
        x_dist_list = []
        y_dist_list = []
        points_dist_list = []

        real_x_dist_list = []
        real_y_dist_list = []

        coord_list = []

        with open(self.interpolated_centroid_file, encoding='UTF8') as f:
            reader = csv.DictReader(f)
            result = sorted(reader, key=lambda d: (int(d['frames'])))

            for a in result:
                coord_list.append([float(a['x']), float(a['y'])-2160])
                if temp is None:
                    temp = a
                else:
                    temp_x = float(temp['x'])
                    temp_y = float(temp['y'])
                    a_x = float(a['x'])
                    a_y = float(a['y'])

                    x_dist, y_dist, points_dist = get_distances(temp_x, temp_y, a_x, a_y)

                    x_dist_list.append(x_dist)
                    y_dist_list.append(y_dist)
                    points_dist_list.append(points_dist)

                    tax_point_x, tax_point_y = get_distance_tax(temp_x, temp_y, a_x, a_y)

                    real_x_dist_list.append(x_dist * tax_point_x)
                    real_y_dist_list.append(y_dist * tax_point_y)

                    temp = a

        pontos_reais = [[-6.9, -8.8], [6.9, -8.8], [6.9, 8.8], [-6.9, 8.8]]  # referencial real
        pontos_foto = [[2076, 1336-2160], [2206, 1251-2160], [2001, 1160-2160], [1868, 1234-2160]]  # referencial foto

        tran = Transforma(pontos_foto=pontos_foto, pontos_reais=pontos_reais)
        print(tran.execute(coord_list))

        create_csv(x_dist_list, y_dist_list, points_dist_list, self.distances_file)
        create_csv(real_x_dist_list, real_y_dist_list, None, self.real_distances_file)

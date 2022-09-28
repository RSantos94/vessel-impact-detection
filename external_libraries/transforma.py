# transforma.py
# J.Marcelino
# 2022-09-07/08
# R. Santos
# 2022-09-09
import os

import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def plotplac(plac, pontos, name, is_realidade: bool):
    if is_realidade:
        plt.axis("scaled")
        #plt.axis([0, 1, 0, 1])
    else:
        plt.axis([0, 3840, 0, 2160])

    plac.append(plac[0])
    xy = np.array(plac)
    plt.plot(xy[:, 0], xy[:, 1], "-")
    xy = np.array(pontos)
    plt.plot(xy[:, 0], xy[:, 1], ".")
    titulo = name.replace(".png", "")
    if is_realidade:
        plt.title("Coordenadas reais")
    else:
        plt.title("Coordenadas imagem")
    #plt.axis("scaled")
    #ax = plt.gca()
    #ax.set_ylim(ax.get_ylim()[::-1])  # invert the axis
    #ax.xaxis.tick_top()
    plt.savefig(name)
    plt.clf()
    #plt.show()


def interpola(pqsieta, p2, Ns):
    qsi = pqsieta[0]
    eta = pqsieta[1]
    xy = np.array(p2)
    x = calcN(Ns[0], qsi, eta) * xy[0, 0] + calcN(Ns[1], qsi, eta) * xy[1, 0] + calcN(Ns[2], qsi, eta) * xy[
        2, 0] + calcN(Ns[3], qsi, eta) * xy[3, 0]
    y = calcN(Ns[0], qsi, eta) * xy[0, 1] + calcN(Ns[1], qsi, eta) * xy[1, 1] + calcN(Ns[2], qsi, eta) * xy[
        2, 1] + calcN(Ns[3], qsi, eta) * xy[3, 1]
    return x, y


def calcN(N, qsi, eta):
    return N[0] + N[1] * qsi + N[2] * eta + N[3] * qsi * eta


def fN(x, y):  # cada polinómio
    return [1, x, y, x * y]


def calculaN(xy):
    vN = []
    for pt in xy:  # define o polinómio associado a cada ponto
        vN.append(fN(pt[0], pt[1]))
    vN = np.array(vN)
    vN1 = np.linalg.inv(vN)
    # define as funcões para darem 1 no ponto nodal e 0 nos restantes
    Ni = []
    for i in range(4):
        zeroum = np.array([0, 0, 0, 0])
        zeroum[i] = 1
        Ni.append(vN1.dot(zeroum))

    return Ni


# transformação de coordenadas


class Transforma:

    def __init__(self, pontos_foto: list, pontos_reais: list, height: int, width: int, source: str, os_name: str, object_name):
        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        parent_path = os.path.dirname(path)

        if os_name == "Windows":
            # D:\git\\vessel-impact-detection\\
            self.picture_coordinates_graph = parent_path + '\\reports\\' + source + '\\object-' + object_name + '\\na_foto.png'
            self.real_coordinates_graph = parent_path + '\\reports\\' + source + '\\object-' + object_name + '\\na_realidade.png'

        else:
            self.picture_coordinates_graph = 'reports/' + source + '/object-' + object_name + '/na_foto.png'
            self.real_coordinates_graph = 'reports/' + source + '/object-' + object_name + '/na_realidade.png'

        self.pontos_reais = pontos_reais  # referencial real
        self.pontos_foto = pontos_foto  # referencial foto

        if pontos_reais is None and pontos_foto is None:
            self.pontos_reais = [[-100, -100], [100, -100], [100, 100], [-100, 100]]  # referencial real
            self.pontos_foto = [[50, 10], [200, 50], [180, 90], [0, 40]]  # referencial foto

        # calculo das funcões de interpolação
        self.Ns = calculaN(pontos_foto)
        self.height = height
        self.width = width

    def execute(self, coor: list):
        # calcular na realidade
        xyr = []
        for p in coor:
            xyr.append(interpola(p, self.pontos_reais, self.Ns))

        plotplac(self.pontos_foto, coor, self.picture_coordinates_graph, False)
        plotplac(self.pontos_reais, xyr, self.real_coordinates_graph, True)

        return xyr

    def example(self):
        # # definição de uma forma geométrica no espaço da foto
        # # por exemplo um circulo
        # r=30
        # xc=180
        # yc=90
        # xy=[]

        # for i in range(360):
        # xy.append([xc+r*math.cos(i),yc+r*math.sin(i)])

        x1 = (50 + 0) / 2
        x2 = (200 + 180) / 2

        xy = []
        for i in range(100):
            xi = x1 + (x2 - x1) / 100 * i
            yi = 10 * math.sin(xi * 3.14 / 180 * 4) + i
            xy.append([xi, yi])

        # calcular na realidade
        xyr = []
        for p in xy:
            xyr.append(interpola(p, self.pontos_reais, self.Ns))

        plotplac(self.pontos_foto, xy, self.picture_coordinates_graph, False)
        plotplac(self.pontos_reais, xyr, self.real_coordinates_graph, True)

# source: https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d


from introcs import Point, Point2, Point3


def project(p, mat1):
    x = mat1[0][0] * p.x + mat1[0][1] * p.y + mat1[0][2] * p.z + mat1[0][3] * 1
    y = mat1[1][0] * p.x + mat1[1][1] * p.y + mat1[1][2] * p.z + mat1[1][3] * 1
    w = mat1[3][0] * p.x + mat1[3][1] * p.y + mat1[3][2] * p.z + mat1[3][3] * 1
    return Point(720 * (x / w + 1) / 2., 576 - 576 * (y / w + 1) / 2.)


# The squared distance between two points a and b
def norm2(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    return dx * dx + dy * dy


def evaluate(mat1, r0, r1, r2, r3, i0, i1, i2, i3):
    c0 = project(r0, mat1)
    c1 = project(r1, mat1)
    c2 = project(r2, mat1)
    c3 = project(r3, mat1)
    return norm2(i0, c0) + norm2(i1, c1) + norm2(i2, c2) + norm2(i3, c3)


def perturb(mat1, amount):
    from copy import deepcopy
    from random import randrange, uniform
    mat2 = deepcopy(mat1)
    mat2[randrange(4)][randrange(4)] += uniform(-amount, amount)
    return mat2


def approximate(mat1, amount, r0, r1, r2, r3, i0, i1, i2, i3, n=100000):
    est = evaluate(mat1, r0, r1, r2, r3, i0, i1, i2, i3)

    for i in range(n):
        mat2 = perturb(mat1, amount)
        est2 = evaluate(mat2, r0, r1, r2, r3, i0, i1, i2, i3)
        if est2 < est:
            mat1 = mat2
            est = est2

    return mat1, est


def transpose(m):
    return [
        [m[0][0], m[1][0], m[2][0], m[3][0]],
        [m[0][1], m[1][1], m[2][1], m[3][1]],
        [m[0][2], m[1][2], m[2][2], m[3][2]],
        [m[0][3], m[1][3], m[2][3], m[3][3]],
    ]


if __name__ == '__main__':
    # Known 2D coordinates of our rectangle
    i0 = Point2(318, 247)
    i1 = Point2(326, 312)
    i2 = Point2(418, 241)
    i3 = Point2(452, 303)

    # 3D coordinates corresponding to i0, i1, i2, i3
    r0 = Point3(0, 0, 0)
    r1 = Point3(0, 0, 1)
    r2 = Point3(1, 0, 0)
    r3 = Point3(1, 0, 1)

    mat = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]

    for i in range(100):
        mat, est = approximate(mat, 1, r0, r1, r2, r3, i0, i1, i2, i3)
        mat, est = approximate(mat, .1, r0, r1, r2, r3, i0, i1, i2, i3)

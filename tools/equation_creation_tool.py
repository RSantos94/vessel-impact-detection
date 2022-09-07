if __name__ == '__main__':
    point_1 = input("Point 1 coordinates: (x1,y2)")
    point_2 = input("Point 2 coordinates: (x2, y2)")

    point_1_list = point_1.split(',')
    point_2_list = point_2.split(',')

    x1 = int(point_1_list[0])
    y1 = int(point_1_list[1])
    x2 = int(point_2_list[0])
    y2 = int(point_2_list[1])

    m = (y2 - y1) / (x2 - x1)

    b = m * x2 - y2

    print("y = " + str(m) + "*x + " + str(b))

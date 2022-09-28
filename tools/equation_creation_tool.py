if __name__ == '__main__':
    gimp = input("Coordinates from GIMP? (y/n)")
    if gimp == 'y':
        resolution = input("Picture resolution: (widthxheight)")
        resolution_list = resolution.split('x')
        point_1 = input("Point 1 coordinates: (x1,y2)")
        point_2 = input("Point 2 coordinates: (x2, y2)")

        point_1_list = point_1.split(',')
        point_2_list = point_2.split(',')

        x1 = int(point_1_list[0])
        y1 = abs(int(point_1_list[1]) - int(resolution_list[1]))
        x2 = int(point_2_list[0])
        y2 = abs(int(point_2_list[1]) - int(resolution_list[1]))
    else:
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

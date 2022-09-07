import math
import platform

from tools.Background_subtraction_KNN import BackgroundSubtractionKNN

if __name__ == '__main__':

    code = None
    while code != 'q':
        pixels = input("Pixel pair coordinates [(x1,y2)(x2,y2)] (q to exit): ")

        code = pixels

        first = pixels.split(')(')
        array = []
        for pixel in first:
            new_pixel1 = pixel.replace('(', '')
            new_pixel2 = new_pixel1.replace(')', '')
            array.append(new_pixel2)
        print(array)
        pixel1 = array[0].split(',')
        pixel2 = array[1].split(',')
        x1 = float(pixel1[0])
        y1 = float(pixel1[1])
        x2 = float(pixel2[0])
        y2 = float(pixel2[1])
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        print('Distance: ' + str(dist))


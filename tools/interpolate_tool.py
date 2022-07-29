import numpy as np

from external_libraries.spline import get_natural_cubic_spline_model


def spline(x=None, y=None, frames=None):
    nodes = max(frames) - min(frames)

    spline_x = get_natural_cubic_spline_model(x=frames, y=x, minval=min(frames), maxval=max(frames),
                                              n_knots=int(nodes / 2))
    spline_y = get_natural_cubic_spline_model(x=frames, y=y, minval=min(frames), maxval=max(frames),
                                              n_knots=int(nodes / 2))

    all_frames = np.arange(min(frames), max(frames), 1)
    x_est = spline_x.predict(all_frames)
    y_est = spline_y.predict(all_frames)


    return x_est, y_est

if __name__ == '__main__':
    coordinates_text = input("Coordinates: (x1,y2;x2,y2;...)")
    coor_list = coordinates_text.split(';')
    count = 0
    x_list = []
    y_list = []
    time_list = []
    for coor_text in coor_list:
        count = count + 1
        coor_list = coor_text.split(',')
        x_list.append(int(coor_list[0]))
        y_list.append(int(coor_list[1]))
        time_list.append(int(count))

    x_est, y_est = spline(np.array(x_list), np.array(y_list), np.array(time_list))

    print('x list: ' + str(x_est.tolist()))
    print('y list: ' + str(y_est.tolist()))
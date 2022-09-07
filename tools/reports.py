import csv
import os
import platform

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image as mpimg


def spline_report(x, y, frames, splined_x, splined_y, source, current):
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    parent_path = os.path.dirname(path)
    os_name = platform.system()

    if os_name == "Windows":
        folder = parent_path + '\\reports\\' + source + '\\object-' + current
        if not os.path.exists(folder):
            os.makedirs(folder)
        spline_report_name = folder + '\\spline-report.html'
        spline_report_stock_xy_name = folder + '\\stock-xy-graph.png'
        spline_report_stock_tx_name = folder + '\\stock-tx-graph.png'
        spline_report_stock_ty_name = folder + '\\stock-ty-graph.png'
        spline_report_spline_xy_name = folder + '\\spline-xy-graph.png'
        spline_report_spline_tx_name = folder + '\\spline-tx-graph.png'
        spline_report_spline_ty_name = folder + '\\spline-ty-graph.png'
        spline_report_combined_xy_name = folder + '\\combined-xy-graph.png'
        spline_report_combined_tx_name = folder + '\\combined-tx-graph.png'
        spline_report_combined_ty_name = folder + '\\combined-ty-graph.png'
    else:
        folder = 'reports/' + source + '/object-' + current
        if not os.path.exists(folder):
            os.makedirs(folder)
        spline_report_name = folder + '/spline-report.html'
        spline_report_stock_xy_name = folder + '/stock-xy-graph.png'
        spline_report_stock_tx_name = folder + '/stock-tx-graph.png'
        spline_report_stock_ty_name = folder + '/stock-ty-graph.png'
        spline_report_spline_xy_name = folder + '/spline-xy-graph.png'
        spline_report_spline_tx_name = folder + '/spline-tx-graph.png'
        spline_report_spline_ty_name = folder + '/spline-ty-graph.png'
        spline_report_combined_xy_name = folder + '/combined-xy-graph.png'
        spline_report_combined_tx_name = folder + '/combined-tx-graph.png'
        spline_report_combined_ty_name = folder + '/combined-ty-graph.png'

    # Create graphs
    create_graph(x, y, 'x', 'y', spline_report_stock_xy_name)
    create_graph(frames, x, 'frames', 'x', spline_report_stock_tx_name)
    create_graph(frames, y, 'frames', 'y', spline_report_stock_ty_name)

    all_frames = np.arange(min(frames), max(frames), 1)
    create_graph(splined_x, splined_y, 'x', 'y', spline_report_spline_xy_name)
    create_graph(all_frames, splined_x, 'frames', 'x', spline_report_spline_tx_name)
    create_graph(all_frames, splined_y, 'frames', 'y', spline_report_spline_ty_name)

    create_csv(all_frames, splined_x, splined_y, 'frames', 'x', 'y', spline_report_spline_xy_name)
    create_graph_on_picture(splined_x, splined_y, spline_report_spline_xy_name)

    create_combined_graph(x, y, splined_x, splined_y, 'x', 'y', 'recorded', 'splinned', spline_report_combined_xy_name)
    create_combined_graph(frames, x, all_frames, splined_x, 'frames', 'x', 'recorded', 'splinned',
                          spline_report_combined_tx_name)
    create_combined_graph(frames, y, all_frames, splined_y, 'frames', 'y', 'recorded', 'splinned',
                          spline_report_combined_ty_name)

    # Create HTML text
    spline_report_title_title = 'Spline Report ' + source
    spline_report_stock_title = 'Provided coordinates graph'
    spline_report_stock_xy_title = 'Provided XY coordinates graph'
    spline_report_stock_tx_title = 'Provided TX coordinates graph'
    spline_report_stock_ty_title = 'Provided TY coordinates graph'
    spline_report_spline_title = 'Spline coordinates graph'
    spline_report_spline_xy_title = 'Spline XY coordinates graph'
    spline_report_spline_tx_title = 'Spline TX coordinates graph'
    spline_report_spline_ty_title = 'Spline TY coordinates graph'
    spline_report_combined_title = 'Combined coordinates graph'
    spline_report_combined_xy_title = 'Combined XY coordinates graph'
    spline_report_combined_tx_title = 'Combined TX coordinates graph'
    spline_report_combined_ty_title = 'Combined TY coordinates graph'
    text = 'Lorem Ipsum'

    html = f'''
        <html>
            <head>
                <title>{spline_report_title_title}</title>
            </head>
            <body>
                <h1>{spline_report_stock_title}</h1>
                
                
                <h2>{spline_report_stock_xy_title}</h2>
                <p>{text}</p>
                <img src={spline_report_stock_xy_name} width="700">
                
                <h2>{spline_report_stock_tx_title}</h2>
                <p>{text}</p>
                <img src={spline_report_stock_tx_name} width="700">
                
                <h2>{spline_report_stock_ty_title}</h2>
                <p>{text}</p>
                <img src={spline_report_stock_ty_name} width="700">
                
                <h1>{spline_report_spline_title}</h1>
                
                <h2>{spline_report_spline_xy_title}</h2>
                <p>{text}</p>
                <img src={spline_report_spline_xy_name} width="700">
                
                <h2>{spline_report_spline_tx_title}</h2>
                <p>{text}</p>
                <img src={spline_report_spline_tx_name} width="700">
                
                <h2>{spline_report_spline_ty_title}</h2>
                <p>{text}</p>
                <img src={spline_report_spline_ty_name} width="700">
                
                <h1>{spline_report_combined_title}</h1>
                
                <h2>{spline_report_combined_xy_title}</h2>
                <p>{text}</p>
                <img src={spline_report_combined_xy_name} width="700">
                
                <h2>{spline_report_combined_tx_title}</h2>
                <p>{text}</p>
                <img src={spline_report_combined_tx_name} width="700">
                
                <h2>{spline_report_combined_ty_title}</h2>
                <p>{text}</p>
                <img src={spline_report_combined_ty_name} width="700">
            </body>
        </html>
        '''
    # Write the html string as an HTML file
    with open(spline_report_name, 'w') as f:
        f.write(html)


def derivate_report(x_1d, x_2d, y_1d, y_2d, frames, source, current):
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    os_name = platform.system()

    if os_name == "Windows":
        folder = path + '\\reports\\' + source + '\\object-' + current
        if not os.path.exists(folder):
            os.makedirs(folder)
        spline_report_name = folder + '\\derivative-report.html'
        first_derivative_graph_xy_name = folder + '\\first-derivative-xy-graph.png'
        first_derivative_graph_tx_name = folder + '\\first-derivative-tx-graph.png'
        first_derivative_graph_ty_name = folder + '\\first-derivative-ty-graph.png'
        second_derivative_graph_xy_name = folder + '\\second-derivative-xy-graph.png'
        second_derivative_graph_tx_name = folder + '\\second-derivative-tx-graph.png'
        second_derivative_graph_ty_name = folder + '\\second-derivative-ty-graph.png'
        combined_derivative_graph_tx_name = folder + '\\combined-derivative-tx-graph.png'
        combined_derivative_graph_ty_name = folder + '\\combined-derivative-ty-graph.png'

    else:
        folder = 'reports/' + source + '/object-' + current
        if not os.path.exists(folder):
            os.makedirs(folder)
        spline_report_name = folder + '/derivative-report.html'
        first_derivative_graph_xy_name = folder + '/first-derivative-xy-graph.png'
        first_derivative_graph_tx_name = folder + '/first-derivative-tx-graph.png'
        first_derivative_graph_ty_name = folder + '/first-derivative-ty-graph.png'
        second_derivative_graph_xy_name = folder + '/second-derivative-xy-graph.png'
        second_derivative_graph_tx_name = folder + '/second-derivative-tx-graph.png'
        second_derivative_graph_ty_name = folder + '/second-derivative-ty-graph.png'
        combined_derivative_graph_tx_name = folder + '/combined-derivative-tx-graph.png'
        combined_derivative_graph_ty_name = folder + '/combined-derivative-ty-graph.png'

    # Create graphs
    # create_graph(x_1d, y_1d, 'x', 'y', first_derivative_graph_xy_name)
    create_graph(frames, x_1d, 'frames', 'x', first_derivative_graph_tx_name)
    create_graph(frames, y_1d, 'frames', 'y', first_derivative_graph_ty_name)
    # create_graph(x_2d, y_2d, 'x', 'y', second_derivative_graph_xy_name)
    create_graph(frames, x_2d, 'frames', 'x', second_derivative_graph_tx_name)
    create_graph(frames, y_2d, 'frames', 'y', second_derivative_graph_ty_name)
    create_combined_graph(frames, x_1d, frames, x_2d, 'frames', 'x', "1st derivate", "2nd derivate",
                          combined_derivative_graph_tx_name)
    create_combined_graph(frames, y_1d, frames, y_2d, 'frames', 'y', "1st derivate", "2nd derivate",
                          combined_derivative_graph_ty_name)

    # Create HTML text
    derivate_report_title_title = 'Derivate Report ' + source
    first_derivate_report_spline_title = 'Splined first derivate graph'
    first_derivate_report_spline_xy_title = 'Splined XY first derivate graph'
    first_derivate_report_spline_tx_title = 'Splined TX first derivate graph'
    first_derivate_report_spline_ty_title = 'Splined TY first derivate graph'
    second_derivate_report_spline_title = 'Splined second derivate graph'
    second_derivate_report_spline_xy_title = 'Splined XY second derivate graph'
    second_derivate_report_spline_tx_title = 'Splined TX second derivate graph'
    second_derivate_report_spline_ty_title = 'Splined TY second derivate graph'
    combined_derivate_report_spline_title = 'Combined derivative graphs'
    combined_derivate_report_spline_tx_title = 'Splined TX combined derivate graph'
    combined_derivate_report_spline_ty_title = 'Splined TY combined derivate graph'

    text = 'Lorem Ipsum'

    html = f'''
        <html>
            <head>
                <title>{derivate_report_title_title}</title>
            </head>
            <body>
                <h1>{first_derivate_report_spline_title}</h1>


                <!-- <h2>{first_derivate_report_spline_xy_title}</h2>
                <p>{text}</p>
                <img src={first_derivative_graph_xy_name} width="700"> -->

                <h2>{first_derivate_report_spline_tx_title}</h2>
                <p>{text}</p>
                <img src={first_derivative_graph_tx_name} width="700">

                <h2>{first_derivate_report_spline_ty_title}</h2>
                <p>{text}</p>
                <img src={first_derivative_graph_ty_name} width="700">
                
                
                <h1>{second_derivate_report_spline_title}</h1>


                <!-- <h2>{second_derivate_report_spline_xy_title}</h2>
                <p>{text}</p>
                <img src={second_derivative_graph_xy_name} width="700"> -->

                <h2>{second_derivate_report_spline_tx_title}</h2>
                <p>{text}</p>
                <img src={second_derivative_graph_tx_name} width="700">

                <h2>{second_derivate_report_spline_ty_title}</h2>
                <p>{text}</p>
                <img src={second_derivative_graph_ty_name} width="700">
                
                <h1>{combined_derivate_report_spline_title}</h1>

                
                <h2>{combined_derivate_report_spline_tx_title}</h2>
                <p>{text}</p>
                <img src={combined_derivative_graph_tx_name} width="700">

                <h2>{combined_derivate_report_spline_ty_title}</h2>
                <p>{text}</p>
                <img src={combined_derivative_graph_ty_name} width="700">
                
            </body>
        </html>
        '''
    # Write the html string as an HTML file
    with open(spline_report_name, 'w') as f:
        f.write(html)


def accelerometer_report(x_acceleration_list, y_acceleration_list, z_acceleration_list, gyro_x_list, gyro_y_list,
                         gyro_z_list, timestamp_list, report_location):
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    os_name = platform.system()

    if os_name == "Windows":

        if not os.path.exists(report_location):
            os.makedirs(report_location)
        acceleration_report_name = report_location + '\\spline-report.html'
        acceleration_report_accel_tx_name = report_location + '\\acceleration-tx-graph.png'
        acceleration_report_accel_ty_name = report_location + '\\acceleration-ty-graph.png'
        acceleration_report_accel_tz_name = report_location + '\\acceleration-tz-graph.png'
        acceleration_report_gyro_tx_name = report_location + '\\gyro-tx-graph.png'
        acceleration_report_gyro_ty_name = report_location + '\\gyro-ty-graph.png'
        acceleration_report_gyro_tz_name = report_location + '\\gyro-tz-graph.png'
        # acceleration_report_combined_xy_name = report_location + '\\combined-xy-graph.png'
        # acceleration_report_combined_tx_name = report_location + '\\combined-tx-graph.png'
        # acceleration_report_combined_ty_name = report_location + '\\combined-ty-graph.png'
    else:

        if not os.path.exists(report_location):
            os.makedirs(report_location)
        acceleration_report_name = report_location + '/accelerometer-report.html'
        acceleration_report_accel_tx_name = report_location + '/acceleration-tx-graph.png'
        acceleration_report_accel_ty_name = report_location + '/acceleration-ty-graph.png'
        acceleration_report_accel_tz_name = report_location + '/acceleration-tz-graph.png'
        acceleration_report_gyro_tx_name = report_location + '/gyro-tx-graph.png'
        acceleration_report_gyro_ty_name = report_location + '/gyro-ty-graph.png'
        acceleration_report_gyro_tz_name = report_location + '/gyro-tz-graph.png'
        # acceleration_report_combined_xy_name = report_location + '/combined-xy-graph.png'
        # acceleration_report_combined_tx_name = report_location + '/combined-tx-graph.png'
        # acceleration_report_combined_ty_name = report_location + '/combined-ty-graph.png'

    # Create graphs
    create_graph(timestamp_list, x_acceleration_list, 'time (ms)', 'x', acceleration_report_accel_tx_name)
    create_graph(timestamp_list, y_acceleration_list, 'time (ms)', 'y', acceleration_report_accel_ty_name)
    create_graph(timestamp_list, z_acceleration_list, 'time (ms)', 'z', acceleration_report_accel_tz_name)

    # all_frames = np.arange(min(frames), max(frames), 1)
    create_graph(timestamp_list, gyro_x_list, 'time (ms)', 'x', acceleration_report_gyro_tx_name)
    create_graph(timestamp_list, gyro_y_list, 'time (ms)', 'y', acceleration_report_gyro_ty_name)
    create_graph(timestamp_list, gyro_z_list, 'time (ms)', 'z', acceleration_report_gyro_tz_name)

    # Create HTML text
    acceleration_report_title_title = 'Accelerometer Report'
    acceleration_report_accel_title = 'Acceleration graph'
    acceleration_report_accel_tx_title = 'TX acceleration graph'
    acceleration_report_accel_ty_title = 'TY acceleration graph'
    acceleration_report_accel_tz_title = 'TZ acceleration graph'
    acceleration_report_gyro_title = 'Gyro graph'
    acceleration_report_gyro_tx_title = 'TX Gyro graph'
    acceleration_report_gyro_ty_title = 'Gyro TY Gyro graph'
    acceleration_report_gyro_tz_title = 'Gyro TZ Gyro graph'
    # spline_report_combined_title = 'Combined coordinates graph'
    # spline_report_combined_xy_title = 'Combined XY coordinates graph'
    # spline_report_combined_tx_title = 'Combined TX coordinates graph'
    # spline_report_combined_ty_title = 'Combined TY coordinates graph'
    text = 'Lorem Ipsum'

    html = f'''
        <html>
            <head>
                <title>{acceleration_report_title_title}</title>
            </head>
            <body>
                <h1>{acceleration_report_accel_title}</h1>
                

                <h2>{acceleration_report_accel_tx_title}</h2>
                <p>{text}</p>
                <img src={acceleration_report_accel_tx_name} width="700">

                <h2>{acceleration_report_accel_ty_title}</h2>
                <p>{text}</p>
                <img src={acceleration_report_accel_ty_name} width="700">
                
                <h2>{acceleration_report_accel_tz_title}</h2>
                <p>{text}</p>
                <img src={acceleration_report_accel_tz_name} width="700">
                
                

                <h1>{acceleration_report_gyro_title}</h1>
                

                <h2>{acceleration_report_gyro_tx_title}</h2>
                <p>{text}</p>
                <img src={acceleration_report_gyro_tx_name} width="700">

                <h2>{acceleration_report_gyro_ty_title}</h2>
                <p>{text}</p>
                <img src={acceleration_report_gyro_ty_name} width="700">
                
                <h2>{acceleration_report_gyro_tz_title}</h2>
                <p>{text}</p>
                <img src={acceleration_report_gyro_tz_name} width="700">

                
            </body>
        </html>
        '''
    # Write the html string as an HTML file
    with open(acceleration_report_name, 'w') as f:
        f.write(html)


def create_graph(x, y, x_label, y_label, name):
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(name)
    plt.show()


def create_combined_graph(f1_x, f1_y, f2_x, f2_y, x_label, y_label, f1_name, f2_name, name):
    plt.plot(f1_x, f1_y, label=f1_name)
    plt.plot(f2_x, f2_y, label=f2_name)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig(name)
    plt.show()


def create_csv(frames, x, y, frames_label, x_label, y_label, name):
    csv_name = name[:-3] + "csv"

    header_list = [frames_label, x_label, y_label]
    with open(csv_name, 'w', encoding='UTF8', newline='') as f:
        dw = csv.DictWriter(f, delimiter=',', fieldnames=header_list)
        dw.writeheader()

        new_frames = frames.tolist()
        new_x = x.tolist()
        new_y = y.tolist()

        i = 0
        while i < len(new_x):
            dw.writerow({frames_label: new_frames[i], x_label: new_x[i], y_label: new_y[i]})
            i += 1


def create_graph_on_picture(x, y, name):
    new_x = []
    new_y = []
    #for i in x:
    #    new_x.append(abs(3840-i))
    new_x = x
    #for i in x:
    #    new_y.append(abs(2160-i))

    new_y = y

    picture_name = name[:-4] + "-with-picture.png"
    image = mpimg.imread("D:\\git\\vessel-impact-detection\\screenshot_files\\GH010731_cut_mixed.png")

    plt.imshow(image)

    height, width = image.shape[:2]

    plt.axis([0, width, 0, height])
    plt.plot(new_x, new_y)
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])  # invert the axis
    ax.xaxis.tick_top()
    #plt.gca().invert_yaxis()
    #plt.ylim(max(plt.ylim()), min(plt.ylim()))
    plt.savefig(picture_name)
    plt.show()


class Reports:
    pass

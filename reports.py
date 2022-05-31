import matplotlib.pyplot as plt
import os
import platform

import matplotlib.pyplot as plt


def spline_report(x, y, frames, splined_x, splined_y, source, current):
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    os_name = platform.system()

    if os_name == "Windows":
        folder = path + '\\reports\\' + source + '\\object-' + current
        if not os.path.exists(folder):
            os.makedirs(folder)
        spline_report_name = folder + '\\report.html'
        spline_report_stock_xy_name = folder + '\\stock-xy-graph.png'
        spline_report_stock_tx_name = folder + '\\stock-tx-graph.png'
        spline_report_stock_ty_name = folder + '\\stock-ty-graph.png'
        spline_report_spline_xy_name = folder + '\\spline-xy-graph.png'
        spline_report_spline_tx_name = folder + '\\spline-tx-graph.png'
        spline_report_spline_ty_name = folder + '\\spline-ty-graph.png'
    else:
        folder = 'reports/' + source + '/object-' + current
        if not os.path.exists(folder):
            os.makedirs(folder)
        spline_report_name = folder + '/report.html'
        spline_report_stock_xy_name = folder + '/stock-xy-graph.png'
        spline_report_stock_tx_name = folder + '/stock-tx-graph.png'
        spline_report_stock_ty_name = folder + '/stock-ty-graph.png'
        spline_report_spline_xy_name = folder + '/spline-xy-graph.png'
        spline_report_spline_tx_name = folder + '/spline-tx-graph.png'
        spline_report_spline_ty_name = folder + '/spline-ty-graph.png'

    # Create graphs
    create_graph(x, y, 'x', 'y', spline_report_stock_xy_name)
    create_graph(frames, x, 'frames', 'x', spline_report_stock_tx_name)
    create_graph(frames, y, 'frames', 'y', spline_report_stock_ty_name)
    create_graph(splined_x, splined_y, 'x', 'y', spline_report_spline_xy_name)
    create_graph(frames, splined_x, 'frames', 'x', spline_report_spline_tx_name)
    create_graph(frames, splined_y, 'frames', 'y', spline_report_spline_ty_name)

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
            </body>
        </html>
        '''
    # Write the html string as an HTML file
    with open(spline_report_name, 'w') as f:
        f.write(html)


def create_graph(x, y, x_label, y_label, name):
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(name)
    plt.show()


class Reports:
    pass

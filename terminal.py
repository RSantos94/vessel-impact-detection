import platform

from tools.Background_subtraction_KNN import BackgroundSubtractionKNN
from tools.calculate_physics import CalculatePhysics
from tools.convert_units import ConvertUnits
from tools.interpolate_centroids import InterpolateCentroids

outputFrame = None
bs1 = None
bs2 = None
bsz3 = None
cap1 = None
cap2 = None


def create_bs(source_name: str, compute_window_size: (int, int), os_name: str):
    return BackgroundSubtractionKNN(source_name, compute_window_size, os_name)


def run(background_subtractor: BackgroundSubtractionKNN, is_test: bool):
    background_subtractor.create_centroids_file()
    return background_subtractor.subtractor(is_test)


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)

    # stereo = True

    # window_size = (640, 360)
    # window_size = (1280, 720)
    window_size = (1980, 1080)
    # window_size = (3840, 2160)

    # bs.create_centroids_file()

    # objects_to_track = None
    os_name = platform.system()

    test = input("Test (y/n)[default n]?:")
    if test == 'y':
        source = input("Video 1 or 2:")
        if source == '1':
            source_name = 'GH010731_cut'  # lnec gopro
            # source_name = 'GH010949-cut'
        elif source == '2':
            source_name = 'PXL_20220311_123649450-cut'

        window_size1 = (1980, 1080)
        #window_size1 = (3840, 2160)
        bs1 = create_bs(source_name, window_size1, os_name)

        run(bs1, is_test=True)
    else:
        # stereo = input("Stereo (y/n)[default n]?:")

        stereo = 'n'

        if stereo == 'y':
            source1 = input("Video file 1 name:")
            source2 = input("Video file 2 name:")

            # source1 = 'MVI_2438'  # lnec camara
            # source2 = 'GH010731_cut'  # lnec gopro
            # source1 = 'GH010946_1' # teste piscina 1
            # source2 = 'PXL_20220308_141209924_1' # teste piscina 1
            source1 = 'GH010949-cut'  # teste piscina 2
            source2 = 'PXL_20220311_123649450-cut'  # teste piscina 2
            # source1 = 'GH010954_1'  # teste piscina tupperware 1
            # source2 = 'PXL_20220319_165746871_1'  # teste piscina tupperware 1

            # window_size1 = (1280, 720)
            window_size1 = (1980, 1080)
            window_size2 = (1980, 1080)

            # frame = []

            bs1 = create_bs(source1, window_size1, os_name)
            bs2 = create_bs(source2, window_size2, os_name)

            # sp = StereoProcessing(source1, source2)

            # if sp.has_points_file(source1) is not True:
            # bs1.get_screenshot()
            # bs2.frames = bs1.frames

            # if sp.has_points_file(source2) is not True:
            # bs2.get_screenshot()

            # if sp.has_points_file(source1) is not True and sp.has_points_file(source2) is not True:
            # input("Create corresponding points file at config/{source}-points.txt and press enter")

            # bs1.create_undistorted_video_file()
            # bs2.create_undistorted_video_file()

            # run(bs1, is_test=False)
            # run(bs2, is_test=False)

            objects_to_track1 = []
            objects_to_track2 = []

            text1 = input("Object ids to track from first camera (separated by comma):")
            text2 = input("Object ids to track from second camera (separated by comma):")

            arr1 = text1.split(',')
            for x in arr1:
                if x != '':
                    objects_to_track1.append(x)

            arr2 = text2.split(',')
            for x in arr2:
                if x != '':
                    objects_to_track2.append(x)

            ic1 = InterpolateCentroids(source1, os_name)
            ic1.objects_to_track1 = objects_to_track1
            ic1.execute()
            ic2 = InterpolateCentroids(source2, os_name)
            ic2.objects_to_track2 = objects_to_track2
            ic2.execute()

            # sp.objects_to_track1 = objects_to_track1
            # sp.objects_to_track2 = objects_to_track2
            # sp.configure_points(source1, source2)
            # sp.execute()

        else:
            source = input("Video file name:")

            # teste 0006
            source = 'GH010727_impact_1'  # lnec gopro # ponto 2
            # source = 'GH010727_impact_2'  # lnec gopro # ponto 4
            # source = 'GH010727_impact_3'  # lnec gopro # ponto 6/7(mais o 7) (7 falha calculos)
            # source = 'GH010727_impact_4'  # lnec gopro # ponto 5
            # source = 'GH010727_impact_5'  # lnec gopro # ponto 7
            # source = 'GH010727_impact_6'  # lnec gopro # ponto 5
            # source = 'GH010727_impact_7'  # lnec gopro # ponto 6
            # source = 'GH010727_impact_8'  # lnec gopro # ponto 5
            # source = 'GH010727_impact_9'  # lnec gopro # ponto 5
            # source = 'GH010727_impact_10'  # lnec gopro # ponto 7

            #teste 0010
            # source = 'MVI_2438'  # lnec camara
            # source = 'GH010731_cut'  # lnec gopro
            # source = 'GH010731_impact_1'  # lnec gopro # ponto 4
            # source = 'GH010731_impact_2'  # lnec gopro # ponto 3
            # source = 'GH010731_impact_3'  # lnec gopro # ponto 2
            # source = 'GH010731_impact_4'  # lnec gopro # ponto 4
            # source = 'GH010731_impact_5'  # lnec gopro # ponto 6
            # source = 'GH010731_impact_6'  # lnec gopro # ponto 5
            # source = 'GH010731_impact_7'  # lnec gopro # ponto 5
            # source = 'GH010731_impact_8'  # lnec gopro # ponto 4
            # source = 'GH010731_impact_9'  # lnec gopro # ponto 6 (fraco)
            # source = 'GH010731_impact_10'  # lnec gopro # ponto 4
            # source = 'GH010731_impact_11'  # lnec gopro # ponto 8

            # source = 'GH010946_1' # teste piscina 1
            # source = 'PXL_20220308_141209924_1' # teste piscina 1
            # source = 'GH010949-cut'  # teste piscina 2
            # source = 'PXL_20220311_123649450-cut'  # teste piscina 2
            # source = 'GH010954_1'  # teste piscina tupperware 1
            # source = 'PXL_20220319_165746871_1'  # teste piscina tupperware 1

            #window_size = (1280, 720)
            window_size = (1980, 1080)
            # window_size = (3840, 2160)

            # frame = []

            bs = create_bs(source, window_size, os_name)

            #error = run(bs, is_test=False)
            error = None

            if error is not None:
                print(error)
                quit()

            objects_to_track = []

            text = input("Object id to track:")
            #46
            arr1 = text.split(',')
            for x in arr1:
                if x != '':
                    objects_to_track.append(x)

            ic = InterpolateCentroids(source, os_name)
            ic.objects_to_track = objects_to_track
            ic.execute()

            cu = ConvertUnits(source, objects_to_track[0], os_name)
            coordinates, frame_rate, time_list = cu.execute()

            mass = input("Vessel mass (in Kg):")

            physics = CalculatePhysics(coordinates, frame_rate, time_list, float(mass), source, objects_to_track[0])
            acceleration, force = physics.execute()

            print("Max acceleration: " + str(acceleration) + " m^2/s^2")
            print("Max force: " + str(force) + " Kg*m^2/s^2 (N m)")

            # sp.objects_to_track1 = objects_to_track1
            # sp.objects_to_track2 = objects_to_track2
            # sp.configure_points(source1, source2)
            # sp.execute()

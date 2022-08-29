import platform

from tools.Background_subtraction_KNN import BackgroundSubtractionKNN

if __name__ == '__main__':

    window_size = (1980, 1080)
    source_name = input("Video file name (stored in the video_files folder: ")
    source_name = 'GX011307'
    source_name = 'GH010731_cut'
    os_name = platform.system()
    bs = BackgroundSubtractionKNN(source_name, window_size, os_name)
    bs.get_screenshot_tool()
    # bs.subtractor(True)
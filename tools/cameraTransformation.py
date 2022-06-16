import cameratransform as ct
import numpy as np

import sys


class CameraTransformation:

    def __init__(self, source_name):
        self.config_file = 'config/' + source_name + '.txt'
        self.camera = None

    def configure(self):
        try:
            is_landmarks = False
            f = open(self.config_file, "r")
            landmarks = []
            for x in f:
                #x = x.replace("\n", "")
                if not is_landmarks:
                    arr = x.split(':')
                    if arr[0] == 'Camera f':
                        camera_f = arr[1].strip()
                    elif arr[0] == 'Camera focal length':
                        camera_focal_lenght = arr[1].strip()
                    elif arr[0] == 'Camera sensor size':
                        sensor = arr[1].split(',')
                        camera_sensor_x = sensor[0].strip()
                        camera_sensor_y = sensor[1].strip()
                    elif arr[0] == 'Camera image size':
                        image = arr[1].split(',')
                        camera_image_x = image[0].strip()
                        camera_image_y = image[1].strip()
                    elif arr[0] == 'Camera elevation(m)':
                        elevation = arr[1].strip()
                    elif arr[0] == 'Camera tilt(deg)':
                        tilt = arr[1].strip()
                    elif arr[0] == 'Camera position x (m)':
                        location_x = arr[1].strip()
                    elif arr[0] == 'Camera position y (m)':
                        location_y = arr[1].strip()
                    elif arr[0] == 'Camera heading(deg)':
                        heading = arr[1].strip()
                    elif arr[0] == 'GPS Precision':
                        precision = arr[1].split(',')
                        latitude_precision = precision[0].strip()
                        longitude_precision = precision[1].strip()
                        height_precision = precision[2].strip()
                    elif arr[0] == 'Landmarks':
                        is_landmarks = True
                else:
                    if any(ext in x for ext in
                           ['Camera f', 'Camera sensor size', 'Camera image size', 'Camera elevation(m)',
                            'Camera tilt(deg)', 'Camera location', 'Camera heading(deg)']):
                        is_landmarks = False
                    else:
                        landmarks.append(x)

            self.camera = ct.Camera(ct.RectilinearProjection(focallength_mm=float(camera_focal_lenght),
                                                        sensor=(float(camera_sensor_x), float(camera_sensor_y)),
                                                        image=(int(camera_image_x), int(camera_image_y))))
            if elevation is not None:
                self.camera.elevation_m = float(elevation)
            if tilt is not None:
                self.camera.tilt_deg = int(tilt)
            if heading is not None:
                self.camera.heading_deg=int(heading)
            if location_x is not None:
                self.camera.pos_x_m=float(location_x)

            #self.camera = self.set_coord(landmarks, location, self.camera, latitude_precision, longitude_precision, height_precision)

        except FileNotFoundError:
            print('O ficheiro ' + self.config_file + ' não existe!')
            sys.exit(0)

    def set_coord(self, landmarks, location, camera, latitude_precision, longitude_precision, height_precision):
        gps_coord = [(s[0], s[1]) for s in map(lambda a: a.split('&')[:2], landmarks)]
        pixel_coord = map(lambda a: a.split('&')[2:], landmarks)

        camera.setGPSpos(location)

        lm_points_px = np.array(pixel_coord)
        lm_points_gps = ct.gpsFromString(gps_coord)
        lm_points_space = camera.spaceFromGPS(lm_points_gps)

        camera.addLandmarkInformation(lm_points_px, lm_points_space, [latitude_precision, longitude_precision, height_precision])

        return camera

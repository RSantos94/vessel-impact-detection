import cameratransform as ct
import numpy as np


class CameraTransformation:

    def __init__(self, source_name):
        self.config_file = 'config/' + source_name + '.txt'
        self.camera = None

    def configure(self):
        is_landmarks = False
        f = open(self.config_file, "r")
        landmarks = []
        for x in f:
            if not is_landmarks:
                arr = x.split(':')
                if arr[0] == 'Camera f':
                    camera_f = arr[1]
                elif arr[0] == 'Camera sensor size':
                    sensor = arr[1].split(',')
                    camera_sensor_x = sensor[0]
                    camera_sensor_y = sensor[1]
                elif arr[0] == 'Camera image size':
                    image = arr[1].split(',')
                    camera_image_x = image[0]
                    camera_image_y = image[1]
                elif arr[0] == 'Camera elevation(m)':
                    elevation = arr[1]
                elif arr[0] == 'Camera tilt(deg)':
                    tilt = arr[1]
                elif arr[0] == 'Camera location':
                    location = arr[1]
                elif arr[0] == 'Camera heading(deg)':
                    heading = arr[1]
                elif arr[0] == 'GPS Precision':
                    precision = arr[1].split(',')
                    latitude_precision = precision[0]
                    longitude_precision = precision[1]
                    height_precision = precision[2]
                elif arr[0] == 'Landmarks':
                    is_landmarks = True
                print(arr[0])
            else:
                if any(ext in x for ext in
                       ['Camera f', 'Camera sensor size', 'Camera image size', 'Camera elevation(m)',
                        'Camera tilt(deg)', 'Camera location', 'Camera heading(deg)']):
                    is_landmarks = False
                else:
                    landmarks.append(x)

        gps_coord = [(s[0], s[1]) for s in map(lambda a: a.split('&')[:2], landmarks)]
        pixel_coord = map(lambda a: a.split('&')[2:], landmarks)
        camera = ct.Camera(ct.RectilinearProjection(focallength_mm=float(camera_f),
                                                    sensor=(float(camera_sensor_x), float(camera_sensor_y)),
                                                    image=(int(camera_image_x), int(camera_image_y))),
                           ct.SpatialOrientation(elevation_m=int(elevation),
                                                 tilt_deg=int(tilt), heading_deg=int(heading)))
        camera.setGPSpos(location)

        lm_points_px = np.array(pixel_coord)
        lm_points_gps = ct.gpsFromString(gps_coord)
        lm_points_space = camera.spaceFromGPS(lm_points_gps)

        camera.addLandmarkInformation(lm_points_px, lm_points_space,
                                      [latitude_precision, longitude_precision, height_precision])

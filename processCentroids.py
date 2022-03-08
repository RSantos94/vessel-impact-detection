import csv
import numpy as np

from scipy.spatial import distance

from cameraTransformation import CameraTransformation

class ProcessCentroids:

    def __init__(self, source_name, objects_to_track):
        self.centroid_file = 'results/' + source_name + '-centroids.csv'
        self.objects_to_track = objects_to_track

        #self.ct = CameraTransformation(source_name)
        #self.ct.configure()

    def execute(self):
        with open(self.centroid_file, encoding='UTF8') as f:
            reader = csv.DictReader(f)
            result = sorted(reader, key=lambda d: int(d['Object ID']))

            object_id = None
            prev_x = None
            prev_y = None
            dist = 0.0

            if self.objects_to_track is not None and isinstance(self.objects_to_track, list):
                centroids = [a for a in result if a['Object ID'] in self.objects_to_track]
            else:
                centroids = result

            for row in centroids:
                if object_id is None:
                    object_id = row['Object ID']
                    prev_x = float(row['x'])
                    prev_y = float(row['y'])
                    continue

                if object_id == row['Object ID']:
                    a = np.array((prev_x, prev_y))
                    b = np.array((float(row['x']), float(row['y'])))
                    #print(np.linalg.norm(a - b))
                    dist = dist + np.linalg.norm(a - b)

                else:
                    print('Object ' + object_id + ' total distance is: ' + str(dist))
                    object_id = row['Object ID']
                    prev_x = float(row['x'])
                    prev_y = float(row['y'])
                    dist = 0.0
                #print(row)
                #if row['Object ID'] == '18':
                   # print(row)

            print('Object ' + object_id + ' total distance is: ' + str(dist))
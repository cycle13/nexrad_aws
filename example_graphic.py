import os
from aws_nexrad import create_radar_graphic

for f in os.listdir('test_data'):
    radar_file = 'test_data/{}'.format(f)
    print 'Creating radar plot: {}'.format(f)
    create_radar_graphic(radar_file, 'reflectivity', 0, 'pyart_NWSRef')

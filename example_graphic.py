from aws_nexrad import create_radar_graphic

f = 'test_data/KDMX20080525_173706_V03.gz'
create_radar_graphic(f, 'reflectivity', 0, 'pyart_NWSRef')

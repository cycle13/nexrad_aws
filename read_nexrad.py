import boto
import matplotlib.pyplot as plt
import pyart.graph
import pyart.io
import tempfile

# read a volume scan file on S3.
s3conn = boto.connect_s3()
bucket = s3conn.get_bucket('noaa-nexrad-level2')
rs = bucket.list('2008/05/25/KDMX')
for key in rs:
    if key.name.endswith('.gz'):
        print key.name
        s3key = bucket.get_key(key.name)

        # download to a local file, and read it
        localfile = tempfile.NamedTemporaryFile()
        s3key.get_contents_to_filename(localfile.name)
        radar = pyart.io.read_nexrad_archive(localfile.name)

        display = pyart.graph.RadarMapDisplay(radar)

        display.plot_ppi_map('reflectivity', 0, cmap='pyart_NWSRef',
                             min_lon=-97.0, max_lon=-90.0,
                             min_lat=40.0, max_lat=45.0,
                             projection='lcc', resolution='h',
                             lat_0=radar.latitude['data'][0],
                             lon_0=radar.longitude['data'][0])

        display_file = display.generate_filename('reflectivity', 0, ext='png')

        plt.savefig(display_file)

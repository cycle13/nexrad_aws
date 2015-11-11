import boto
import matplotlib.pyplot as plt
import pyart.graph
import pyart.io


def download_volume_scans(radar_id, year, month, day):
    """
    Download all the available volume scans from aws nexrad archive
    for the given radar identifier and day of interest.
    """

    s3conn = boto.connect_s3()
    bucket = s3conn.get_bucket('noaa-nexrad-level2')
    bucket_list = bucket.list('{}/{}/{}/{}'.format(year, month, day, radar_id))
    for key in bucket_list:
        if key.name.endswith('.gz'):
            s3key = bucket.get_key(key.name)

            # download to a local file, and read it
            localfile = s3key.name.split('/')[-1]
            print 'Downloading: {}\nSaving to: {}'.format(key.name, localfile)
            s3key.get_contents_to_filename(localfile)


def create_radar_graphic(radarfile, field, sweep, cmap):
    """
    Create an image file from the specified radarfile
    """

    radar = pyart.io.read_nexrad_archive(radarfile)
    display = pyart.graph.RadarMapDisplay(radar)

    # set projection bounds based on radar location
    lat_0 = radar.latitude['data'][0]
    lon_0 = radar.longitude['data'][0]
    min_lon = lon_0 - 3.0
    max_lon = lon_0 + 3.0
    min_lat = lat_0 - 3.0
    max_lat = lat_0 + 3.0

    display.plot_ppi_map(field, sweep, cmap=cmap,
                         projection='lcc', resolution='h',
                         min_lon=min_lon, max_lon=max_lon,
                         min_lat=min_lat, max_lat=max_lat,
                         lat_0=lat_0, lon_0=lon_0)

    plt.savefig('{}.png'.format(radarfile.split('/')[-1].split('.')[0]))

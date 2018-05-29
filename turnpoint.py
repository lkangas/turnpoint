import numpy as np

# "02406795E" -> 24.11325
# "6044718N" -> 60.7453
def coord(coord_string):
    degrees = coord_string[:-6]
    minutes = coord_string[-6:-1]
    return float(degrees) + float(minutes)/1000/60

# distance between two coordinates, equirectangular approximation (for <1 km)
def dist(point1, point2):

    lat1, lon1 = point1
    lat2, lon2 = point2
    R = 6371e3
    x = (lon2-lon1) * np.cos((lat1+lat2)/2)
    y = lat2-lat1

    x = np.deg2rad(x)
    y = np.deg2rad(y)

    return R * np.hypot(x,y)

def read_cup(filename):
    turnpoint_headers = 1

    with open(filename, 'r') as f:
        skipped = 0
        names = []
        latitudes = []
        longitudes = []

        for line in f:
            if skipped < turnpoint_headers:
                skipped += 1
                continue
        
            columns = line.strip().split(',')

            try:
                name = columns[0]
                latitude_string = columns[3].replace('.', '') # "60.44718N" -> "6044718N" (to same format as in .igc file)
                longitude_string = columns[4].replace('.', '') 
            except:
                continue # broken line

            names.append(name.replace('"', '')) # strip unnecessary quotes from .cup CSV
            latitudes.append(coord(latitude_string))
            longitudes.append(coord(longitude_string))
    
        return names, latitudes, longitudes

def read_igc(filename=None, content=None):
    
    igc_latitudes = []
    igc_longitudes = []

    if filename:
        with open(filename, 'r') as f:
            igc_content = f.readlines()
            
    if content:
        igc_content = content.split('\n')

    for line in igc_content:
        if len(line) and line[0] == 'B':
            latitude_string = line[7:15]
            longitude_string = line[15:24]

            igc_latitudes.append(coord(latitude_string))
            igc_longitudes.append(coord(longitude_string))

    track = np.column_stack((igc_latitudes, igc_longitudes))
    return track


def turnpoints_in_track(track, turnpoints):
    visited = []

    for tp_name, tp_lat, tp_lon in zip(*turnpoints):
        
        tp_coords = (tp_lat, tp_lon)
    
        limit = 360.0 / 40000 * 3
        lat_within = track[ np.abs(track[:,0] - tp_lat) < limit ]
        both_within = lat_within[ np.abs(lat_within[:,1] - tp_lon) < limit]
    
        if len(both_within):
            for fix_coords in both_within:
                distance = dist(fix_coords, tp_coords)
                if distance < 1000:
                    visited.append(tp_name)
                    break
    return visited


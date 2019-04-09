import pandas as pd
import numpy as np


# strip latitude and longitude separately
def get_lat_lon(coordinates, route=False):
    if route:
        data = [gps.strip(" []") for gps in coordinates.strip('[]').split(',')]
        lon_lat = pd.DataFrame(np.array(data).astype(np.float).reshape(-1, 2))
        return lon_lat[0], lon_lat[1], lon_lat.values
    else:
        lon_lat = pd.DataFrame(coordinates.str.strip('[]').str.split(',', expand=True))
        latitude = pd.to_numeric(lon_lat[0])
        longitude = pd.to_numeric(lon_lat[1])
        return latitude, longitude, lon_lat.values.astype(np.float)


# get snap to road index
def get_iteration(n):
    i = int((n - 1) / 100) + 1
    if ((n - 1)/ (i * 100 - i)) > 1:
        i = i + 1
    return i


def snap_index(n):
    index = []
    i = get_iteration(n)
    for j in range(1, i + 1):
        if j == i:
            index.append(n - 1)
        else:
            index.append(100 * j - j)
    return sorted(index)

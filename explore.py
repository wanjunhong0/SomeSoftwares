import pandas as pd
from tqdm import tqdm
import gmplot
import mpu
import os

file_path = r"D:\Code\Traffic\data_all\shuttle_feature.csv"
if not os.path.isfile(file_path):
    # data_path = r'D:\Code\Traffic\data\shuttle.csv'
    data_path = r'D:\Code\Traffic\data_all\shuttle_all.csv'
    # data_path = r'D:\Code\Traffic\data_history\shuttle_history.csv'
    df = pd.read_csv(data_path)
    df.gps_time = pd.to_datetime(df.gps_time)  # convert datetime
    # df = df[df.upload == 1]   # select running shuttle
    print('unique number of license plate: {0}'.format(df.device_index.nunique()))

    # sort data by license plate and time
    sort_plate_map = dict(zip(list(df.device_index.unique()), range(df.device_index.nunique())))
    df['sort_plate'] = df.device_index.map(sort_plate_map)
    df = df.sort_values(by=['sort_plate', 'gps_time'])
    df = df.reset_index(drop=True)

    # calculate distance in km
    coordinates = list(map(list, zip(df.latitude.tolist(), df.longitude.tolist())))
    dist = [0] * len(coordinates)
    for i in tqdm(range(len(coordinates))):
        if i == 0:
            dist[i] = 0
        else:
            dist[i] = round(mpu.haversine_distance(coordinates[i], coordinates[i-1]), 6)
    # zero at each start of every plate number
    separate_index = [0] * df.device_index.nunique()
    for i in tqdm(range(df.device_index.nunique())):
        separate_index[i] = df[df.device_index == df.device_index.unique()[i]].index.min()
    for i in separate_index:
        dist[i] = 0
    df['dist'] = dist


    # output
    df.to_csv(file_path, index=False)

df = pd.read_csv(file_path)
# select active shuttle, (total_dist < 50km) considered inactive
total_dist = df.groupby(['device_index']).dist.sum()
active_shuttle = list(total_dist[total_dist > 1000].index)
df = df[df.device_index.isin(active_shuttle)]
print('unique number of active license plate: {0}'.format(df.device_index.nunique()))

# sort data by license plate and time
sort_plate_map = dict(zip(list(df.device_index.unique()), range(df.device_index.nunique())))
df['sort_plate'] = df.device_index.map(sort_plate_map)
df = df.sort_values(by=['sort_plate', 'gps_time'])
df = df.reset_index(drop=True)

# calculate time gap
time = pd.to_datetime(df[df.dist != 0].gps_time)
time_gap = [0] * len(time)
for i, j in tqdm(enumerate(range(len(time)), list(time.index))):
    if j == 0:
        time_gap[i] = 0
    else:
        time_gap[i] = (time.iloc[j] - time.iloc[j - 1]).total_seconds()
# zero at each start of every plate number
for i in separate_index:
    time_gap[i] = 0
df['time_gap'] = time_gap

#





# google map
if not os.path.isdir('./plot'):
    os.mkdir('./plot')
    for i in tqdm(df.device_index.unique()):
        gmap = gmplot.GoogleMapPlotter(df.latitude.mean(), df.longitude.mean(), 13,
                                       apikey='AIzaSyBOX2s8xecA0Q6JCsJzGqb4pzfEy4H1ypg')
        gmap.heatmap(df[df.device_index == i].latitude, df[df.device_index == i].longitude, opacity=0.9)
        output_path = './plot' + str(sort_plate_map[i]) + i + '.html'
        gmap.draw(output_path)































# shuttle in station or not
# Zhoushan Putuo Long-distance Passenger Transport Center
# station_coordinates = (29.963616, 122.290536)
# coordinates = list(map(list, zip(df.latitude.tolist(), df.longitude.tolist())))
# dist_station = [0] * len(coordinates)
# for i in tqdm(range(len(coordinates))):
#     dist_station[i] = round(mpu.haversine_distance(coordinates[i], station_coordinates), 4)
# df['dist_station'] = dist_station
# dist_station_min = df.groupby(['device_index']).dist_station.min()
# in_station_shuttle = list(dist_station_min[dist_station_min < 1].index)
# df = df[df.device_index.isin(in_station_shuttle)]
# print('unique number of in-station active license plate: {0}'.format(df.device_index.nunique()))
# in_station_count = df[df.dist_station < 1].groupby(['sort_plate']).dist.count().sort_values()


































# create time gap for separate route period, -1 means end of the record for each license plate
# df['time_gap'] = 0
#
# for i in tqdm(range(df.shape[0])):
#     if i == df.shape[0] - 1:
#         df.time_gap = -1
#     else:
#         df.time_gap = (df.gps_time.iloc[i + 1] - df.gps_time.iloc[i]).total_seconds()





# if df.sort_plate[i+1] - df.sort_plate[i] != 0:
#     df.time_gap = -1












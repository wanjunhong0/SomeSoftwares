import pandas as pd
import gmplot
from sklearn.cluster import DBSCAN
import numpy as np
from utils import get_lat_lon
import os
from tqdm import tqdm


# read data and select total dist greater than 100km
df = pd.read_csv('./data/route.csv')
df = df[df.dist > 50]

# get latitude and longitude
start_lat, start_lon, start = get_lat_lon(df.start)
end_lat, end_lon, end = get_lat_lon(df.end)

# clustering start and end coordinates
clustering_dist = 1    # in km
earth_radian = 6371.0088     # in km
eps = clustering_dist/earth_radian
start_cluster = DBSCAN(eps=eps, min_samples=5, metric='haversine', algorithm='ball_tree').fit(np.radians(start))
print('Number of start clusters: {}'.format(len(set(start_cluster.labels_))))
end_cluster = DBSCAN(eps=eps, min_samples=5, metric='haversine', algorithm='ball_tree').fit(np.radians(end))
print('Number of end clusters: {}'.format(len(set(end_cluster.labels_))))
df['start_cluster'] = start_cluster.labels_
df['end_cluster'] = end_cluster.labels_


# create index for the route of same start and end cluster
df = df[(df.start_cluster != -1) & (df.end_cluster != -1)]
route_cluster = DBSCAN(eps=0.0001, min_samples=10).fit(df[['start_cluster', 'end_cluster']].values)
print('Number of route clusters: {}'.format(len(set(route_cluster.labels_))))
df['route_cluster'] = route_cluster.labels_
df = df[df.route_cluster != -1]
df = df.sort_values(by=['route_cluster'])
df = df.reset_index(drop=True)

# output
df.to_csv('./data/route_cluster.csv', index=False)







# plot start and end coordinates on Google Maps
station_coordinates = (29.963616, 122.290536)     # Zhoushan Putuo Long-distance Passenger Transport Center
if not os.path.isdir('./plot_route'):
    os.mkdir('./plot_route')
    for cluster in tqdm(range(df.route_cluster.nunique())):
        gmap = gmplot.GoogleMapPlotter(station_coordinates[0], station_coordinates[1], 13,
                                       apikey='AIzaSyBOX2s8xecA0Q6JCsJzGqb4pzfEy4H1ypg')
        gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
        data = df[df.route_cluster == cluster]
        start_lat, start_lon, _ = get_lat_lon(data.start)
        end_lat, end_lon, _ = get_lat_lon(data.end)
        gmap.marker(start_lat.mean(), start_lon.mean(), 'blue', title='Start')
        gmap.marker(end_lat.mean(), end_lon.mean(), 'red', title='End')
        lat_all = []
        lon_all = []
        for i in range(data.shape[0]):
            lat, lon, _ = get_lat_lon(data.gps_route.iloc[i], route=True)
            lat_all = np.concatenate((lat_all, lat), axis=0)
            lon_all = np.concatenate((lon_all, lon), axis=0)
        gmap.heatmap(lat_all, lon_all, opacity=1, radius=15)
        gmap.draw('./plot_route/route_cluster_' + str(cluster) + '.html')



# if not os.path.isfile('./route plot/start.html'):
#     gmap = gmplot.GoogleMapPlotter(start_lat.mean(), start_lon.mean(), 13, apikey='AIzaSyBOX2s8xecA0Q6JCsJzGqb4pzfEy4H1ypg')
#     gmap.heatmap(start_lat, start_lon, opacity=1, radius=20)
#     gmap.draw('./route plot/start.html')
# if not os.path.isfile('./route plot/end.html'):
#     gmap = gmplot.GoogleMapPlotter(end_lat.mean(), end_lon.mean(), 13, apikey='AIzaSyBOX2s8xecA0Q6JCsJzGqb4pzfEy4H1ypg')
#     gmap.heatmap(end_lat, end_lon, opacity=1, radius=20)
#     gmap.draw('./route plot/end.html')
















import numpy as np
import pandas as pd
import utils, re

def fcs(my_location):
	
	df_stations = pd.read_csv('stops.txt')

	# find station with minimum distance to the specified location
	distances = np.sqrt((my_location[0]-df_stations['stop_lat'])**2 + (my_location[1]-df_stations['stop_lon'])**2)
	closest_station = df_stations.loc[np.argmin(distances),'stop_name']


	idx = df_stations.index[df_stations['stop_name'] == closest_station].tolist()
	lst = df_stations.loc[idx,'stop_id']


	df_stop_times = pd.read_csv('stop_times.txt')

	closest_lines = df_stop_times.query('stop_id in @lst')

	closest_trains = [x.split('..')[0] for x in closest_lines['trip_id']]
	closest_trains = list(set([x.split('_')[-1] for x in closest_trains]))

	# closest_station = utils.remove_ordinal(closest_station)

	return closest_station, closest_trains

import numpy as np
import pandas as pd
import utils, re

def fcs(my_location):
	df_stations = pd.read_csv('info_subway_stations.csv', dtype=str)
	df_stations = df_stations[['NAME','the_geom','LINE']]


	df_stations['the_geom'] = df_stations['the_geom'].str[7:].str.rstrip(')')
	#print(df_stations)


	station_coordinates = df_stations.the_geom.str.split(expand=True)
	station_coordinates.columns = [['Lat', 'Long']]
	#print(station_coordinates)

	min = 100000
	for i in range(len(station_coordinates.index)):
		prod = np.sqrt((my_location[0]-float(station_coordinates.iloc[i,0]))**2 + (my_location[1]-float(station_coordinates.iloc[i,1]))**2)
		if (prod < min):
			min = prod
			min_index = i

	closest_station = str(df_stations.iloc[min_index,0])
	
	idx = df_stations.index[df_stations['NAME'] == closest_station].tolist()
	
	closest_lines = ''
	for i in idx:
		#print(df_stations.iloc[i,2])
		line = (str(df_stations.iloc[i,2])+" ").replace("-"," ").replace(' Express', '')
		closest_lines = closest_lines + line

	closest_lines = ''.join(set(closest_lines))
	closest_lines = closest_lines.replace(" ", "")
	#closest_lines = str(df_stations.iloc[min_index,2]).replace("-"," ").replace('Express', '')

	closest_station = utils.remove_ordinal(closest_station)
	return closest_station, closest_lines

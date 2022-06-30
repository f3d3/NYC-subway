import google.transit.gtfs_realtime_pb2 as gtfs_realtime_pb2
import time
from datetime import datetime,timezone
from pytz import timezone as tz

# importing the requests library 
import requests

import pandas as pd 
import numpy as np
import os
import re

from protobuf_to_dict import protobuf_to_dict


def closest(lst, K): 
	return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))] 


def findDestination(trip_id1, trip_id2, input_train, boolean_direction):

	df_trips = pd.read_csv('trips.txt')

	if (type(input_train)!=bool) and (type(boolean_direction)!=bool):
		df_trips = df_trips.query("route_id==@input_train[0] and direction_id==@boolean_direction")[['trip_id','trip_headsign']]

	df_trips.drop_duplicates(keep='first', inplace=True)
	#print(df_trips)


	trip_array = []
	for index, row in df_trips.iterrows():
		trip_id_static = row['trip_id']
		try:
			found = re.search('_(.+?)_', trip_id_static).group(1)
			trip_array.append(int(found))
		except AttributeError:
			raise Exception
	closest_trip1 = closest(trip_array, int(trip_id1))
	closest_trip2 = closest(trip_array, int(trip_id2))

	for index, row in df_trips.iterrows():
		trip_id_static = row['trip_id']
		try:
			found = re.search('_(.+?)_', trip_id_static).group(1)
			if (str(closest_trip1) in found):
				finaldestination1 = row['trip_headsign']
				direction1 = row['trip_id'][-4]
			if (str(closest_trip2) in found):				
				finaldestination2 = row['trip_headsign']
				direction2 = row['trip_id'][-4]
		except AttributeError:
			raise Exception
	return finaldestination1, finaldestination2, direction1, direction2


def main(input_station, input_train, input_direction):

	APIKey="ymFcaLS9JBabZieClasw2XzdXnedgfE8QxBTUED0"

	subwayDict =	{
		"BDFM"   : "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",  # B,D,F,M
		"ACEH"   : "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",   # A,C,E,H
		"1234567": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",       # 1,2,3,4,5,6,7
		"G"      : "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",     # G
		"NQRW"   : "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",  # N,Q,R,W
		"JZ"     : "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz",    # J,Z
		"L"      : "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",     # L
		"SIR"    : "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si"     # SIR (Staten Island Railway)
	}

	trainsToShow = 2

	# if no train has been choosen, iterate over all train feeds, otherwise pick the correct one to save time
	if type(input_train)==bool and type(input_direction)==bool:
		feedsToCheck = subwayDict.values()
	else:
		feedsToCheck = [value for key, value in subwayDict.items() if input_train.lower() in key.lower()]

	# request parameters
	headers = {'x-api-key': APIKey}
	
	if (input_direction == 'U'):
		direction = 'N'
		boolean_direction = 0
	elif (input_direction == 'D'):
		direction = 'S'
		boolean_direction = 1
	elif (not input_direction):
		direction = False
		boolean_direction = False
	else:
		raise Exception

	df_stations = pd.read_csv('stops.txt')

	df_stations = df_stations[df_stations['stop_name']==input_station]['stop_id']

	if type(direction)!=bool:
		stations = [ word for word in df_stations.values if len(word) >= 4 and word.endswith(direction) ]
	else:
		stations = [ word for word in df_stations.values if len(word) >= 4]


	row_list = []
	
	for i in feedsToCheck:

		# Get the train data from the MTA
		try:
			response = requests.get(i, headers=headers, timeout=30)
		except:
			return 'fail'

		# Parse the protocol buffer that is returned
		feed = gtfs_realtime_pb2.FeedMessage()

		try:
			feed.ParseFromString(response.content)
		except:
			return 'fail'

 		# # Get a list of all the train data
		# subway_feed = protobuf_to_dict(feed)  # subway_feed is a dictionary
		# realtime_data = subway_feed['entity']  # train_data is a list
		# realtime_data_df = pd.json_normalize(realtime_data)

		# if (type(direction)==bool and (not input_train[0])) or (trainname==input_train[0]):
		# 	realtime_data_df = realtime_data_df[pd.notna(realtime_data_df['trip_update.trip.trip_id']) & pd.notna(realtime_data_df['trip_update.trip.route_id'])]

		# realtime_data_df = realtime_data_df.dropna(axis='columns', how='all')
		
		# #realtime_data_df.set_index(['id','trip_update.trip.trip_id','trip_update.trip.start_time','trip_update.trip.start_date','trip_update.trip.route_id']).trip_update.stop_time_update.apply(pd.Series).stack().reset_index(['id','trip_update.trip.trip_id','trip_update.trip.start_time','trip_update.trip.start_date','trip_update.trip.route_id'], name='trip_update.stop_time_update')
		# names = ['id','trip_update.trip.trip_id','trip_update.trip.start_time','trip_update.trip.start_date','trip_update.trip.route_id']
		# idx = pd.MultiIndex.from_tuples(realtime_data_df[names].values.tolist(), names=names)
		# realtime_data_df2 = pd.DataFrame(realtime_data_df.trip_update.stop_time_update.tolist(), idx).stack().reset_index(names, name='trip_update.stop_time_update')

		for ent in feed.entity:
			if ent.HasField('trip_update'):
				if ent.trip_update.trip.HasField('route_id'):
					trainname = ent.trip_update.trip.route_id
					if (type(input_train)==bool and type(direction)==bool) or (type(input_train)!=bool and trainname==input_train):
						for j in range(0, len(ent.trip_update.stop_time_update)):
							if ent.trip_update.stop_time_update[j].stop_id in stations:
								trip_id = ent.trip_update.trip.trip_id
								station_codename = ent.trip_update.stop_time_update[j].stop_id
								station_arrival_time = ent.trip_update.stop_time_update[j].arrival.time
								row_list.append({'Trip_ID':trip_id, 'Train': trainname, 'Station': station_codename, 'Time': station_arrival_time})


	df = pd.DataFrame(row_list)

	if type(direction)!=bool:
		print("\nUTC Time: " + str(datetime.now(timezone.utc).strftime("%H:%M:%S")) + " -- Nearest station: " + str(input_station) + " -- Train choosen: " + input_train[0]+"\n\n")
	else:
		print("\nUTC Time: " + str(datetime.now(timezone.utc).strftime("%H:%M:%S")) + " -- Nearest station: " + str(input_station) + "\n\n")

	# only keep the choosen number of trains with scheduled arrival in the next hour
	offset = 3600
	t = int(time.time())
	df_final = df[(t <= df['Time'].astype(int)) & (df['Time'].astype(int) <= t+offset)].sort_values('Time')
	df_final = df_final[0:trainsToShow]

	trains = [x.split('_')[0] for x in df_final['Trip_ID']]

	destination1, destination2, direction1, direction2 = findDestination(trains[0], trains[1], input_train, boolean_direction)

	scheduled_minute = []
	waiting_time = []
	for i in range (0,trainsToShow):
		scheduled_minute.append(int(datetime.utcfromtimestamp(int(df_final['Time'].values[i])).strftime("%M")))
		waiting_time.append(scheduled_minute[i]-int(datetime.now(timezone.utc).strftime("%M")))

	# waiting_time = [i + 60 if i < 0 else i for i in waiting_time] ### Why should there be negative values?

	print("*** Upcoming Trains ***\n")
	for i in range (0,trainsToShow):
		print("Train " + df_final['Train'].values[i] + " - " + str(waiting_time[i]) + " min\n")

	#waiting 30s before updating the timings
	#time.sleep(30.0 - ((time.time() - starttime) % 30.0))

	return df_final['Train'].values[0], destination1, str(waiting_time[0]) + " min", direction1, df_final['Train'].values[1], destination2, str(waiting_time[1]) + " min", direction2

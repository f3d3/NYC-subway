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


def findDestination(trip_id1, trip_id2, input_train, flag):

	df_trips = pd.read_csv('trips.txt')
	df_trips = df_trips.query("route_id==@input_train[0] and direction_id==@flag")[['trip_id','trip_headsign']]
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
			if (str(closest_trip2) in found):				
				finaldestination2 = row['trip_headsign']
		except AttributeError:
			raise Exception
	return finaldestination1, finaldestination2


def main(input_station, input_train, direction):

	#os.system('cls' if os.name == 'nt' else 'clear')


#	api_key = 'ymFcaLS9JBabZieClasw2XzdXnedgfE8QxBTUED0'
	APIKey="ymFcaLS9JBabZieClasw2XzdXnedgfE8QxBTUED0"
	
	# Subway Lines
	BDFMfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm'  # B,D,F,M
	ACEHfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace'  # A,C,E,H
	OneTwoThreefeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'  # 1,2,3,4,5,6,7
	Gfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g'  # G
	NQRWfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw'  # N,Q,R,W
	JZfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz'  # J,Z
	Lfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l' # L
	SIRfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si' # SIR (Staten Island Railway)

	#Add your feeds here
	feedsToCheck = [BDFMfeed, ACEHfeed, OneTwoThreefeed, Gfeed, NQRWfeed, JZfeed, Lfeed, SIRfeed]
	feedScores = dict.fromkeys(feedsToCheck, 0)
	
	uptownTimes = []
	downtownTimes = []
	uptownTrainIDs = []
	downtownTrainIDs = []
	route_id = ""

	# Request parameters
	headers = {'x-api-key': APIKey}



	# f = feedsToCheck[0]
	# # Get the train data from the MTA
	# try:
	# 	response = requests.get(f, headers=headers, timeout=30)
	# except:
	# 	return 'fail'

	# # Parse the protocol buffer that is returned
	# feed = gtfs_realtime_pb2.FeedMessage()

	# try:
	# 	feed.ParseFromString(response.content)
	# except:
	# 	return 'fail'
	# # Get a list of all the train data
	# subway_feed = protobuf_to_dict(feed)  # subway_feed is a dictionary
	# realtime_data = subway_feed['entity']  # train_data is a list


	
	if (direction == 'U'):
		direction = 'N'
		flag = 0
	elif (direction == 'D'):
		direction = 'S'
		flag = 1
	else:
		raise Exception

	df_stations = pd.read_csv('stops.txt')

	df_stations = df_stations[df_stations['stop_name'].str.contains(input_station)]['stop_id']
	#df_stations = df_stations.query("stop_name=='{0}'".format(input_station))['stop_id']

	df_stations.columns = ['index', 'stop_id']
	stations = [ word for word in df_stations.values if len(word) >= 4 ]
	stations = [ word for word in stations if word.endswith(direction) ]


	# NQRWfeednum = '16' # Feed number for N,Q,R,W trains
	# BDFMfeednum = '21' # Feed number for B,D,F,M trains
	# S123456feednum = '1' # Feed number for S,1,2,3,4,5,6 trains
	# ACEHfeednum = '26' # Feed number for A,C,E,H trains
	# Lfeednum = '2' # Feed number for the L train
	# Gfeednum = '31' # Feed number for the G train
	# JZfeednum = '36' # Feed number for the JZ trains
	# Sevenfeednum = '51' # Feed number for the 7 train
	# SIRfeednum = '11' # Feed number for the Staten Island Railway

	# # List of feeds (in order) that we'll check for arrival times.
	# # The order of this list will be optimized based on the
	# # feeds most likely to have the trains in which we are interested
	# feedsToCheck = [NQRWfeednum, BDFMfeednum, S123456feednum, ACEHfeednum,
	# 				Lfeednum, Gfeednum, JZfeednum, Sevenfeednum, SIRfeednum]

	row_list = []

	
	time_format = "%H:%M:%S"
	#os.system('cls' if os.name == 'nt' else 'clear')
	starttime=time.time()
	
#	while True:

	for i in feedsToCheck:

		# URL = "http://datamine.mta.info/mta_esi.php?key=" + api_key + "&feed_id="+str(i)
	  
		# data = requests.get(url = URL, allow_redirects=True) 

		# feed = gtfs_realtime_pb2.FeedMessage()
		# feed.ParseFromString(data.content)

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


		
		for ent in feed.entity:
			if ent.HasField('trip_update'):
				if ent.trip_update.trip.HasField('route_id'):
					trip_id= ent.trip_update.trip.trip_id
					trainname = ent.trip_update.trip.route_id
					if (trainname==input_train[0]):
						for j in range(0, len(ent.trip_update.stop_time_update)):
							station_codename = ent.trip_update.stop_time_update[j].stop_id
							station_arrival_time = ent.trip_update.stop_time_update[j].arrival.time

							dict1 = {}
							dict1.update({'Trip_ID':trip_id, 'Train': trainname, 'Station': station_codename, 'Time': station_arrival_time}) 
							row_list.append(dict1)


	columns = {'Trip_ID', 'Train', 'Station', 'Time'} 
	df = pd.DataFrame(row_list, columns=columns)

	#os.system('cls' if os.name == 'nt' else 'clear')
	print("\nUTC Time: " + str(datetime.now(timezone.utc).strftime("%H:%M:%S")) + " -- Nearest station: " + str(input_station) + " -- Train choosen: " + input_train[0]+"\n\n")

	#print(stations)
	df_final = df.loc[df['Station'].isin(stations)]

	offset = 120 * 60 #minuti*secondi
	t = int(time.time())
	df_final = df_final[(t <= df_final['Time'].astype(int)) & (df_final['Time'].astype(int) <= t+offset)]

	

	''' ALL UPCOMING TRAINS '''
	#df_final.drop_duplicates(subset='Train', keep='first', inplace=True)
	''' SELECTED UPCOMING TRAINS '''
	df_final.drop_duplicates(subset='Time', keep='first', inplace=True)
	df_final = df_final.loc[df_final['Train'].isin(input_train)]

	df_final = df_final[['Trip_ID','Train','Station','Time']].sort_values('Time')
	#print(df_final)
	#print('\n')


	trip_id1 = df_final.iloc[0, 0][0:6]
	trip_id2 = df_final.iloc[1, 0][0:6]
	destination1, destination2 = findDestination(trip_id1, trip_id2, input_train, flag)




	min1=int(datetime.utcfromtimestamp(int(df_final.iloc[0, 3])).strftime("%M"))
	min2=int(datetime.utcfromtimestamp(int(df_final.iloc[1, 3])).strftime("%M"))

	waiting_time_1 = min1-int(datetime.now(timezone.utc).strftime("%M"))
	waiting_time_2 = min2-int(datetime.now(timezone.utc).strftime("%M"))

	if (waiting_time_1 < 0):
		waiting_time_1 = waiting_time_1 + 60
	if (waiting_time_2 < 0):
		waiting_time_2 = waiting_time_2 + 60


	print("*** Upcoming Trains ***\n")
	print("Train " + df_final.iloc[0, 1] + " - " + str(waiting_time_1) + " min")
	print("Train " + df_final.iloc[1, 1] + " - " + str(waiting_time_2) + " min\n")

	#waiting 30s before updating the timings
	#time.sleep(30.0 - ((time.time() - starttime) % 30.0))

	#return "Train " + df_final.iloc[0, 1] + " - " + str(waiting_time_1) + " min", "Train " + df_final.iloc[1, 1] + " - " + str(waiting_time_2) + " min"
	return df_final.iloc[0, 1], destination1, str(waiting_time_1) + " min", df_final.iloc[1, 1], destination2, str(waiting_time_2) + " min"

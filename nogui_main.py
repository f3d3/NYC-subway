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


def closest(lst, K): 
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))] 


def findDestination(trip_id1, trip_id2, input_train, flag):

	df_trips = pd.read_csv('trips.txt')
	df_trips = df_trips.query("route_id==@input_train[0] and direction_id==@flag")[['trip_id','trip_headsign']]
	df_trips.drop_duplicates(keep='first', inplace=True)
	print(df_trips)


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


os.system('cls' if os.name == 'nt' else 'clear')


api_key = '958022fc00135cc9a67106f8587e3b5a'

input_station = input("Enter station: ")
input_train = input("Enter train: ")
input_train = [input_train]

direction = input("Uptown or downtown? [U/D] ")

if (direction=='U'):
	ud = '(Uptown)'
else:
	ud = '(Downtown)'

if (direction == 'U'):
	direction = 'N'
	flag = 0
elif (direction == 'D'):
	direction = 'S'
	flag = 1
else:
	raise Exception


df_stations = pd.read_csv('stops.txt')
df_stations = df_stations.query("stop_name=='{0}'".format(input_station))['stop_id']
df_stations.columns = ['index', 'stop_id']
stations = [ word for word in df_stations.values if len(word) >= 4 ]
stations = [ word for word in stations if word.endswith(direction) ]

time_format = "%H:%M:%S"
feeds_list = [1,26,16,21,2,11,31,36,51]

row_list = []

#os.system('cls' if os.name == 'nt' else 'clear')
starttime=time.time()
#	while True:
for i in feeds_list:

	URL = "http://datamine.mta.info/mta_esi.php?key=" + api_key + "&feed_id="+str(i)
  
	data = requests.get(url = URL, allow_redirects=True) 

	feed = gtfs_realtime_pb2.FeedMessage()
	feed.ParseFromString(data.content)

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
print("\nUTC Time: " + str(datetime.now(timezone.utc).strftime("%H:%M:%S")) + " -- Station choosen: " + str(input_station) + " -- Train choosen: " + input_train[0]+"\n\n")

#print(stations)
df_final = df.loc[df['Station'].isin(stations)]

offset = 60 * 60 #minuti*secondi
t = int(time.time())
df_final = df_final[(t <= df_final['Time'].astype(int)) & (df_final['Time'].astype(int) <= t+offset)]



''' ALL UPCOMING TRAINS '''
#df_final.drop_duplicates(subset='Train', keep='first', inplace=True)
''' SELECTED UPCOMING TRAINS '''
df_final.drop_duplicates(subset='Time', keep='first', inplace=True)
df_final = df_final.loc[df_final['Train'].isin(input_train)]

df_final = df_final[['Trip_ID','Train','Station','Time']].sort_values('Time')
print(df_final)
print('\n')


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


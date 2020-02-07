import google.transit.gtfs_realtime_pb2 as gtfs_realtime_pb2
import time
from datetime import datetime,timezone
from pytz import timezone as tz

# importing the requests library 
import requests

import pandas as pd 
import numpy as np
import os

os.system('cls' if os.name == 'nt' else 'clear')


#def datetime_from_utc_to_local(utc_datetime):
#    now_timestamp = time.time()
#    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
#    return utc_datetime + offset


#def time_conv(posix_time=None, now_time=None, time_format=None):
#  if posix_time:
#  	return datetime.utcfromtimestamp(posix_time).strftime(time_format)
#  return now_time.strftime(time_format)


api_key = '958022fc00135cc9a67106f8587e3b5a'


#input_station = 'Times Sq - 42 St'
#input_train = ['Q']
input_station = input("Enter station: ")
input_train = input("Enter train: ")
input_train = [input_train]
direction = input("Uptown or downtown? [U/D] ")
direction = 'N' if direction == 'U' else 'S'

df_stations = pd.read_csv('stops.txt')
df_stations = df_stations.query("stop_name=='{0}'".format(input_station))['stop_id']
df_stations.columns = ['index', 'stop_id']
#print(df_stations.values)
stations = [ word for word in df_stations.values if len(word) >= 4 ]
stations = [ word for word in stations if word.endswith(direction) ]



time_format = "%H:%M:%S"
feeds_list = [1,26,16,21,2,11,31,36,51]


row_list = []
count = 0


os.system('cls' if os.name == 'nt' else 'clear')
starttime=time.time()
while True:
	for i in feeds_list:
		#print(i)
		# api-endpoint 
		URL = "http://datamine.mta.info/mta_esi.php?key=" + api_key + "&feed_id="+str(i)
	  
		# sending get request and saving the response as response object 
		data = requests.get(url = URL, allow_redirects=True) 

		feed = gtfs_realtime_pb2.FeedMessage()
		feed.ParseFromString(data.content)

		#print(feed.entity)
		for ent in feed.entity:
			if ent.HasField('trip_update'):
				#print(ent.trip_update)
				if ent.trip_update.trip.HasField('route_id'):
					#print(ent.trip_update.trip)
					trainname = ent.trip_update.trip.route_id
					#print(input_train[0])
					if (trainname==input_train[0]):
						for j in range(0, len(ent.trip_update.stop_time_update)):
							station_codename = ent.trip_update.stop_time_update[j].stop_id
							station_arrival_time = ent.trip_update.stop_time_update[j].arrival.time
							#print(str(count) + " " + trainname + " " + station_codename + " " + str(station_arrival_time))
							count=count+1

							dict1 = {}
							dict1.update({'Train': trainname, 'Station': station_codename, 'Time': station_arrival_time}) 
							row_list.append(dict1)
			
							#print("Total_items: "+str(len(feed.entity))+ " // Trip_update: "+ str(sum([1 for ent in feed.entity if ent.HasField('trip_update')])))



	columns = {'Train', 'Station', 'Time'} 
	df = pd.DataFrame(row_list, columns=columns)
	#print(df)
    
	os.system('cls' if os.name == 'nt' else 'clear')
	print("\nUTC Time: " + str(datetime.now(timezone.utc).strftime("%H:%M:%S")) + " -- Station choosen: " + str(input_station) + " -- Train choosen: " + input_train[0]+"\n\n")

	print(stations)
	df_final = df.loc[df['Station'].isin(stations)]

	#time = time_conv(posix_time=1579464840, time_format=time_format)
	#print(time)

	#current_time = time_conv(now_time=datetime.now(tz('Europe/Rome')),time_format=time_format)
	#print (current_time)

	offset = 60 * 60 #minuti*secondi
	t = int(time.time())
	df_final = df_final[(t <= df_final['Time'].astype(int)) & (df_final['Time'].astype(int) <= t+offset)]


	''' ALL UPCOMING TRAINS '''
	#df_final.drop_duplicates(subset='Train', keep='first', inplace=True)
	''' SELECTED UPCOMING TRAINS '''
	df_final.drop_duplicates(subset='Time', keep='first', inplace=True)
	df_final = df_final.loc[df_final['Train'].isin(input_train)]

	df_final = df_final[['Train','Station','Time']].sort_values('Time')
	print(df_final)
	#print('\n')


	#utc1 = datetime_from_utc_to_local(datetime.fromtimestamp(int(df_final.iloc[0, 2])))
	#utc2 = datetime_from_utc_to_local(datetime.fromtimestamp(int(df_final.iloc[1, 2])))

	#pred_time_1 = time_conv(posix_time=int(df_final.iloc[0, 2]),time_format=time_format)
	#pred_time_2 = time_conv(posix_time=int(df_final.iloc[1, 2]),time_format=time_format)
	#print("Train " + df_final.iloc[0, 0] + " - " + pred_time_1 + " min\n")
	#print("Train " + df_final.iloc[1, 0] + " - " + pred_time_2 + " min\n")


	min1=int(datetime.utcfromtimestamp(int(df_final.iloc[0, 2])).strftime("%M"))
	min2=int(datetime.utcfromtimestamp(int(df_final.iloc[1, 2])).strftime("%M"))

	waiting_time_1 = min1-int(datetime.now(timezone.utc).strftime("%M"))
	waiting_time_2 = min2-int(datetime.now(timezone.utc).strftime("%M"))

	if (waiting_time_1 < 0):
		waiting_time_1 = waiting_time_1 + 60
	if (waiting_time_2 < 0):
		waiting_time_2 = waiting_time_2 + 60

	print("*** Upcoming Trains ***\n")
	print("Train " + df_final.iloc[0, 0] + " - " + str(waiting_time_1) + " min")
	print("Train " + df_final.iloc[1, 0] + " - " + str(waiting_time_2) + " min\n")


    #waiting 30s before updating the timings
	time.sleep(30.0 - ((time.time() - starttime) % 30.0))
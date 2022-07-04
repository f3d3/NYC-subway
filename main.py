import tkinter as tk
import tkinter.ttk
import os, time, re, sys
import test_NYC_subway as nycsub
import weather
import utils
import find_station_train
from PIL import Image
from PIL import ImageTk
from datetime import datetime

class MainApplication(tk.Frame):

	def __init__(self, parent, closest_station, choosen_line, direction):
		tk.Frame.__init__(self, parent)


		''' to adapt the window content		'''
		self.grid_columnconfigure(0, weight=1) # as did this
		self.grid_rowconfigure(0, weight=1) # this needed to be added

		parent.columnconfigure(0, weight = 1)
		parent.columnconfigure(1, weight = 1)
		parent.columnconfigure(2, weight = 1)
		parent.columnconfigure(3, weight = 1)
		parent.columnconfigure(4, weight = 1)
		parent.columnconfigure(5, weight = 1)
		parent.rowconfigure(0, weight = 0)
		parent.rowconfigure(1, weight = 0)
		parent.rowconfigure(2, weight = 0)
		parent.rowconfigure(3, weight = 0)
		parent.rowconfigure(4, weight = 0)


		self.closest_station = closest_station
		self. choosen_line = choosen_line
		self.direction = direction

		if type(direction)!=bool:
			if (direction=='U'):
				self.ud = '(Uptown)'
			else:
				self.ud = '(Downtown)'
		else:
			self.ud = '(TBD)'


		self.destination1 = tk.Label(parent, 
					font=("Lato Heavy", 30),
					justify=tk.LEFT,
					padx=10, 
					text='')

		self.direction1 = tk.Label(parent, 
					font=("Lato Heavy", 30),
					justify=tk.LEFT,
					padx=10, 
					text='')

		self.minutes1 = tk.Label(parent, 
					font=("Lato Black", 50),
					justify=tk.RIGHT,
					padx=10, 
					text='')

		self.destination2 = tk.Label(parent, 
					font=("Lato Heavy", 30),
					justify=tk.RIGHT,
					padx=10, 
					text='')

		self.direction2 = tk.Label(parent, 
					font=("Lato Heavy", 30),
					justify=tk.LEFT,
					padx=10, 
					text='')

		self.minutes2 = tk.Label(parent, 
					font=("Lato Black", 50),
					justify=tk.LEFT,
					padx=10, 
					text='')

		self.time = tk.Label(parent, 
					font=("Lato Heavy", 35),
					justify=tk.LEFT,
					padx=10, 
					text='')

		self.temperature = tk.Label(parent, 
					font=("Lato Heavy", 50),
					justify=tk.LEFT,
					padx=10, 
					text='')

		self.date = tk.Label(parent, 
					font=("Lato Heavy", 35),
					justify=tk.RIGHT,
					padx=10, 
					text='')


		self.img1 = tk.Label(parent, image = '')
		self.img1.grid(row = 0, column = 0, columnspan = 1, rowspan = 2, pady = 10)

		self.destination1.grid(row = 0, column = 1, columnspan = 4, sticky = tk.W) 
		self.direction1.grid(row = 1, column = 1, columnspan = 4, sticky = tk.W)  
		self.minutes1.grid(row = 0, column = 5, columnspan = 1, rowspan = 2, pady = 10)  

		self.img2 = tk.Label(parent, image = '')
		self.img2.grid(row = 2, column = 0, columnspan = 1, rowspan = 2, padx = 30, pady = 10)

		self.destination2.grid(row = 2, column = 1, columnspan = 4, sticky = tk.W) 
		self.direction2.grid(row = 3, column = 1, columnspan = 4, sticky = tk.W)  
		self.minutes2.grid(row = 2, column = 5, columnspan = 1, rowspan = 2, padx = 30, pady = 10)  

		self.time.grid(row = 4, column = 0, columnspan = 1, sticky = 'sw') 
		
		self.weather_icon = tk.Label(parent, image='')
		#self.temp_icon.config(height=150, width=150)
		self.weather_icon.grid(row = 4, column = 1, columnspan = 2, pady = 10, sticky = 'se')

		self.temperature.grid(row = 4, column = 3, columnspan = 2, sticky = 'sw') 		
		
		self.date.grid(row = 4, column = 5, columnspan = 1, sticky = 'se') 
		

		tk.ttk.Separator(parent, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=6, sticky='sew')

		self.update_layout(direction)



	def update_layout(self,direction):

		delay = 60000 #60 seconds

		#try:
		#	train1, dest1, min1, dir1, train2, dest2, min2, dir2 = nycsub.main(self.closest_station, self.choosen_line, self.direction)
		#except:
		#	sys.exit('The ' + choosen_line + ' train is not serving this station right now.')
		train1, dest1, min1, dir1, train2, dest2, min2, dir2 = nycsub.main(self.closest_station, self.choosen_line, self.direction)
		
		#dest1 = utils.toLongName(dest1)
		#dest2 = utils.toLongName(dest2)

		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path1 = "images/trains/"+train1.lower()+".png"
		rel_path2 = "images/trains/"+train2.lower()+".png"
		abs_file_path1 = os.path.join(script_dir, rel_path1)
		abs_file_path2 = os.path.join(script_dir, rel_path2)

		img1 = tk.PhotoImage(file=abs_file_path1)
		self.img1.configure(image = img1)
		self.img1.image = img1

		img2 = tk.PhotoImage(file=abs_file_path2)
		self.img2.configure(image = img2)
		self.img2.image = img2


		self.destination1.configure(text=dest1)
		if (type(direction)==bool):
			if dir1=='N':
				self.direction1.configure(text='(Uptown)')
			elif dir1=='S':
				self.direction1.configure(text='(Downtown)')
		else:
			self.direction1.configure(text=self.ud)
		self.minutes1.configure(text=min1)


		self.destination2.configure(text=dest2)
		if (type(direction)==bool):
			if dir2=='N':
				self.direction2.configure(text='(Uptown)')
			elif dir2=='S':
				self.direction2.configure(text='(Downtown)')
		else:
			self.direction2.configure(text=self.ud)
		self.minutes2.configure(text=min2)

		self.time.configure(text=datetime.now().strftime('%H:%M'))

		owm = weather.OpenWeatherMap()
		owm.get_city('New+York+City')
		temperature = float(owm.get('temp'))

		self.temperature.configure(text='%.1f °C' % temperature)

		img3 = Image.open(owm.get_icon_data())
		img3 = img3.resize((60,60), Image.ANTIALIAS)
		img3 =  ImageTk.PhotoImage(img3)
		self.weather_icon.configure(image = img3)
		self.weather_icon.image = img3

		self.date.configure(text=datetime.today().strftime('%d/%m'))

		self.after(delay,  self.update_layout)


	
if __name__ == "__main__":

	choice_location = input("- Press 1 to choose station\n- Press 2 to use the default one\n\n")	
	
	if choice_location == '1':

		station = input("- Write location name.\n\n")	

		trains = find_station_train.findTrains(station)

	elif choice_location == '2':

		my_location = 'Union Square, New York, NY 10019, United States of America'

		#Caching system to reduce the number of coordinates requests
		if (os.path.isfile('cache.txt') and os.stat("cache.txt").st_size != 0):
			f = open("cache.txt")
			line = f.read().splitlines()
			address = line[0]
			if (address == my_location):
				coordinates = [float(line[1]), float(line[2])]
			else:
				f = open("cache.txt", 'w+')
				coordinates = utils.coordinates(my_location)
				f.writelines([my_location+'\n', str(coordinates[0])+'\n', str(coordinates[1])])
			f.close()
		else:
			coordinates = utils.coordinates(my_location)
			f = open("cache.txt", 'w+')
			f.writelines([my_location+'\n', str(coordinates[0])+'\n', str(coordinates[1])])
			f.close()

		station, trains = find_station_train.findClosestStationTrains(coordinates)


	choice = input("- Press 1 to choose train and direction\n- Press 2 to see upcoming trains\n\n")	
	if (choice == '1'):
		choosen_line = input('Choose line between: '+ ' '.join(sorted(trains)) + '\n')
		direction = input("Uptown or downtown? [U/D]"+ '\n')
	elif (choice == '2'):
		choosen_line = False
		direction = False


	window = tk.Tk()
	window.title("NYC Subway")
	window.configure(background='white')
	#window.geometry('1000x450+0+0')


	MainApplication(window, station, choosen_line, direction)

	for c in window.winfo_children():

		if not isinstance(c, tk.ttk.Separator):
			c.configure(background=window['background'])

	window.mainloop()

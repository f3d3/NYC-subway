from tkinter import *
import os, time, re, sys
import test_NYC_subway as nycsub
import weather as w
import utils








#btns_frame = Frame(window, width = 312, height = 272.5, bg = "grey")
#btns_frame.pack()

'''
#Create & Configure frame 
frame=Frame(window)
frame.grid(row=0, column=0, sticky=N+S+E+W)
frame.rowconfigure(0, weight = 1)
frame.rowconfigure(1, weight = 1)
frame.rowconfigure(2, weight = 1)
frame.rowconfigure(3, weight = 1)
frame.columnconfigure(0, weight = 1)
frame.columnconfigure(1, weight = 1)
frame.columnconfigure(2, weight = 1)
'''


delay = 30000
#starttime=time.time()
def update(window, closest_station, choosen_line, direction):

	'''
	#If a lines belonging to closest_lines isn't available (might be a night-only service), then try with the others
	i = 0
	success = False
	#print(len(closest_lines.replace(" ","")))
	while (not success and i in range(0,len(closest_lines))):
		try:
			train1, dest1, min1, train2, dest2, min2 = nycsub.main(closest_station, [closest_lines[i]], direction)
			success = True
		except:
			i = i + 1
			pass
	'''

	if (direction=='U'):
		ud = '(Uptown)'
	else:
		ud = '(Downtown)'

	try:
		train1, dest1, min1, train2, dest2, min2 = nycsub.main(closest_station, [choosen_line], direction)
	except:
		sys.exit('The ' + choosen_line + ' train is not serving this station right now.')

	#train1, dest1, min1, train2, dest2, min2 = nycsub.main(closest_station, [choosen_line], direction)

	dest1 = utils.toLongName(dest1)
	dest2 = utils.toLongName(dest2)

	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path1 = "images/trains/"+train1.lower()+".png"
	rel_path2 = "images/trains/"+train2.lower()+".png"
	abs_file_path1 = os.path.join(script_dir, rel_path1)
	abs_file_path2 = os.path.join(script_dir, rel_path2)

    
	logo1 = PhotoImage(file=abs_file_path1)
	logo2 = PhotoImage(file=abs_file_path2)


	#lbl1 = Label(window, bg="white", text=str1, font=("Arial Bold", 30), anchor="w").grid(sticky = W, column=0,row=0)
	#lbl2 = Label(window, bg="white", text=str2, font=("Arial Bold", 30), anchor="w").grid(sticky = W, column=0,row=1)

	img1 = Label(bg="white", image=logo1)
	img1.image = logo1

	d1 = Label(window, 
				bg="white",
				font=("Lato Heavy", 30),
	            justify=LEFT,
	            padx=10, 
	            text=dest1)

	dir1 = Label(window, 
				bg="white",
				font=("Lato Heavy", 30),
	            justify=LEFT,
	            padx=10, 
	            text=ud)

	m1 = Label(window, 
				bg="white",
				font=("Lato Black", 50),
	            justify=LEFT,
	            padx=10, 
	            text=min1)

	img2 = Label(bg="white", image=logo2)
	img2.image = logo2

	d2 = Label(window, 
				bg="white",
				font=("Lato Heavy", 30),
	            justify=LEFT,
	            padx=10, 
	            text=dest2)

	dir2 = Label(window, 
				bg="white",
				font=("Lato Heavy", 30),
	            justify=LEFT,
	            padx=10, 
	            text=ud)

	m2 = Label(window, 
				bg="white",
				font=("Lato Black", 50),
	            justify=LEFT,
	            padx=10, 
	            text=min2)


	Label(window, image = logo1, bg="white").grid(row = 0, column = 0, 
       columnspan = 1, rowspan = 2, padx = 30, pady = 10)

	d1.grid(row = 0, column = 1, sticky = W) 
	dir1.grid(row = 1, column = 1, sticky = W)  
	m1.grid(row = 0, column = 2, columnspan = 1, rowspan = 2, padx = 30, pady = 10)  

	Label(window, image = logo2, bg="white").grid(row = 2, column = 0, 
       columnspan = 1, rowspan = 2, padx = 30, pady = 10)

	d2.grid(row = 2, column = 1, sticky = W) 
	dir2.grid(row = 3, column = 1, sticky = W)  
	m2.grid(row = 2, column = 2, columnspan = 1, rowspan = 2, padx = 30, pady = 10)  



	owm = w.OpenWeatherMap()
	owm.get_city('New+York+City')
	temperature = owm.get('temp')
	weather_image=PhotoImage(file=owm.get_icon_data())
	temp_icon = Label(window, image=weather_image, bg="white")
	temp_icon.config(height=150, width=150)
	temp_icon.grid(row = 4, padx = 30, pady = 10)



	

	window.update_idletasks()
	window.after(delay, update, window, closest_station, choosen_line, direction)

def main(closest_station, choosen_line, direction):

	window = Tk()
	window.title("NYC Subway")
	#window.geometry('1000x400')
	window.configure(background='white')
	#window.resizable(0, 0)



	update(window, closest_station, choosen_line, direction)
	window.mainloop()

	
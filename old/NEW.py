from tkinter import *
import os, time, re, sys
import test_NYC_subway as nycsub
import weather as w
import utils

root = Tk()
 
root.title("NYC Subway")
root.geometry('1000x600')
root.configure(background='grey')
root.resizable(0, 0)

top_frame = Frame(root, width = 1000, height = 200, bg = "red")
top_frame.pack(side=TOP)




delay = 30000
def update(closest_station, choosen_line, direction):

	if (direction=='U'):
		ud = '(Uptown)'
	else:
		ud = '(Downtown)'

	try:
		train1, dest1, min1, train2, dest2, min2 = nycsub.main(closest_station, [choosen_line], direction)
	except:
		sys.exit('The ' + choosen_line + ' train is not serving this station right now.')

	dest1 = utils.toLongName(dest1)
	dest2 = utils.toLongName(dest2)

	script_dir = os.path.dirname(__file__)
	rel_path1 = "images/trains/"+train1.lower()+".png"
	rel_path2 = "images/trains/"+train2.lower()+".png"
	abs_file_path1 = os.path.join(script_dir, rel_path1)
	abs_file_path2 = os.path.join(script_dir, rel_path2)

	logo1 = PhotoImage(file=abs_file_path1)
	logo2 = PhotoImage(file=abs_file_path2)


	img1 = Label(top_frame, bg="white", image=logo1)
	img1.image = logo1
	img1.pack(side=TOP)
	top_frame.pack_propagate(False) 

	root.update_idletasks()
	root.after(1000, update(closest_station, choosen_line, direction))

	#top_frame.update_idletasks()
	#top_frame.after(delay, first(closest_station, choosen_line, direction))




def main(closest_station, choosen_line, direction):
	root.after(0, update(closest_station, choosen_line, direction))
	root.mainloop()
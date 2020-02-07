from tkinter import *
import os, time
import test_NYC_subway as nycsub


#input_station = 'Times Sq - 42 St'
#input_train = ['Q']
input_station = input("Enter station: ")
input_train = input("Enter train: ")
input_train = [input_train]
direction = input("Uptown or downtown? [U/D] ")

window = Tk()
 
window.title("NYC Subway")
window.geometry('1000x400')
window.configure(background='white')


delay = 30000
#starttime=time.time()
def update():

	train1, dest1, min1, train2, dest2, min2 = nycsub.main(input_station, input_train, direction)


	script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
	rel_path1 = "images/"+train1.lower()+".png"
	rel_path2 = "images/"+train2.lower()+".png"
	abs_file_path1 = os.path.join(script_dir, rel_path1)
	abs_file_path2 = os.path.join(script_dir, rel_path2)

    
	logo1 = PhotoImage(file=abs_file_path1)
	logo2 = PhotoImage(file=abs_file_path2)


	 
	#lbl1 = Label(window, bg="white", text=str1, font=("Arial Bold", 30), anchor="w").grid(sticky = W, column=0,row=0)
	#lbl2 = Label(window, bg="white", text=str2, font=("Arial Bold", 30), anchor="w").grid(sticky = W, column=0,row=1)

	img1 = Label(window, bg="white", image=logo1)
	img1.configure(image=logo1)
	img1.logo1 = logo1

	d1 = Label(window, 
				bg="white",
				font=("Arial Bold", 30),
	            justify=LEFT,
	            padx=10, 
	            text=dest1)
	m1 = Label(window, 
				bg="white",
				font=("Arial Bold", 30),
	            justify=LEFT,
	            padx=10, 
	            text=min1)

	img2 = Label(window, bg="white", image=logo2)
	img2.configure(image=logo2)
	img2.logo2 = logo2

	d2 = Label(window, 
				bg="white",
				font=("Arial Bold", 30),
	            justify=LEFT,
	            padx=10, 
	            text=dest2)
	m2 = Label(window, 
				bg="white",
				font=("Arial Bold", 30),
	            justify=LEFT,
	            padx=10, 
	            text=min2)


	myFrame = Frame(window, bd=1, relief="sunken")

	myFrame.grid_columnconfigure(0, weight=1)
	myFrame.grid_columnconfigure(1, weight=1)
	myFrame.grid_columnconfigure(2, weight=1)
	myFrame.grid_rowconfigure(0, weight=1)
	myFrame.grid_rowconfigure(1, weight=1)

	img1.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
	d1.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
	m1.grid(row=0, column=2, padx=(10, 10), pady=(10, 10))

	img2.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))
	d2.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))
	m2.grid(row=1, column=2, padx=(10, 10), pady=(10, 10))


	window.update_idletasks()
	window.after(delay, update)

#waiting 30s before updating the timings
#t = time.sleep(30.0 - ((time.time() - starttime) % 30.0))

update()
window.mainloop()

	
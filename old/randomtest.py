from tkinter import * 
import test_NYC_subway as nycsub
import os
import glob
import utils
#import test_gui
#import NEW
import find_closest_station


# Will be called every minute
def callBack(closest_station, choosen_line, direction):
	global uptownMinutes
	global downtownMinutes
	global topImage
	global bottomImage
	global uptownTrain
	global downtownTrain
	global uptownDestination
	global downtownDestination

	if (direction=='U'):
		ud = '(Uptown)'
	else:
		ud = '(Downtown)'

	try:
		uptownTrain, uptownDestination, uptownMinutes, downtownTrain, downtownDestination, downtownMinutes = nycsub.main(closest_station, [choosen_line], direction)
	except:
		sys.exit('The ' + choosen_line + ' train is not serving this station right now.')


	# Set the images to the uptown and downtown trains
	topImage['image'] = images[uptownTrain.lower()]
	bottomImage['image'] = images[downtownTrain.lower()]


	# See 'ya again in a minute
	m.after(30000,callBack)








my_location = 'Central Park North (110 St), New York, NY, USA'
coordinates = utils.coordinates(my_location)
closest_station, closest_lines = find_closest_station.fcs(coordinates)

choosen_line = input('Choose line between: '+ closest_lines.replace("", " ")[1: -1] + '\n')

direction = input("Uptown or downtown? [U/D] ")

closest_station = utils.toShortName(closest_station)
print(closest_station)







# Font
fontName = "Lato Heavy"

# Create main application window
m = Tk()


displayWidth = m.winfo_screenwidth()
displayHeight = m.winfo_screenheight()

# Get display DPI
dpi = int(m.winfo_pixels('1i'))

# Calculate points per pixel
ppx = dpi / 72

# Font size of time text should be 10% of screen height
timeTextFontSize = int((displayHeight * 0.055) * ppx)

# Label font size should be 5% of screen height
labelFontSize = int((displayHeight * 0.02) * ppx)

# Make our background white
m.configure(background='white')

# Target size of images is 37.5% of display height
imageSize = int(displayHeight * 0.375)


uptownDestination = ''
downtownDestination = ''
uptownMinutes = ''
downtownMinutes = ''

# Map train letters to images. Scale the images as necessary. The results
# of scaling the images are not great, it's STRONGLY recommended that you
# create images which are already of the correct size (37.5% of display height).
images = {}

# Grab each PNG in the icons subdirectory
for f in (glob.glob('images/trains%s*.png'%(os.sep))):

	# Index on the basename of the PNG file. For example the "A" train will
	# have its image in the file icons/A.png
	l = os.path.basename(os.path.splitext(f)[0])
	images[l] = PhotoImage(file=f)

	# If the image is not square, we're just not going to deal with it.
	if (images[l].height() != images[l].width()):
		raise Exception("Image icons%s%s.png is not square"%(os.sep,l))

	# Are we scaling down?
	if ((images[l].height() > imageSize)):
		scale = int(1 / (imageSize/images[l].width()))
		images[l] = images[l].subsample(scale, scale)

	# Are we scaling up?
	if ((images[l].height() < imageSize)):
		scale = int(imageSize/images[l].width())
		images[l] = images[l].zoom(scale, scale)


# Uptown platform name
Label(m,
	  font=(fontName,labelFontSize),
	  text=uptownDestination).grid(row=0,
								   column=0,
								   columnspan=2,
								   sticky=W)
# Uptown train image
topImage = Label(m)

topImage.grid(row=1, column=0)

# Label which displays uptown arrival times
uptownMinutes = StringVar()
topText = Label(m,
				font=(fontName, timeTextFontSize),
				textvariable=uptownMinutes)
topText.grid(row=1, column=1, sticky=W)

# Draw horizontal line seperating uptown/downtown times
lineMargin = 20
c = Canvas(m,width=displayWidth,
		   height=lineMargin,
		   bd=0,
		   highlightthickness=0,
		   relief='ridge')
c.grid(row=2, column=0,columnspan=2, sticky="ew")
c.create_line(0,lineMargin,displayWidth,lineMargin,width=3)


# Downtown platform name
Label(m,
	  font=(fontName,labelFontSize),
	  text=downtownDestination).grid(row=3,
									 column=0,
									 columnspan=2,
									 sticky=W)

# Downtown train image
bottomImage = Label(m)
bottomImage.grid(row=4, column=0)

# Label which displays downtown arrival times
bottomString = StringVar()
bottomText = Label(m,
				   font=(fontName,timeTextFontSize),
				   textvariable=downtownMinutes)
bottomText.grid(row=4, column=1, sticky=W)

# Make all widgets have the same bg color as the main window
for c in m.winfo_children():
	c.configure(background=m['background'])


# Kick off the callback
callBack(closest_station, choosen_line, direction)

# Run the UI
m.mainloop()
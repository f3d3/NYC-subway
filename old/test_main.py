import utils
import test_gui
#import NEW
import find_closest_station



my_location = 'Canal Street, New York, NY, USA'
coordinates = utils.coordinates(my_location)
closest_station, closest_lines = find_closest_station.fcs(coordinates)

choosen_line = input('Choose line between: '+ closest_lines.replace("", " ")[1: -1] + '\n')


direction = input("Uptown or downtown? [U/D] ")

print(utils.toShortName(closest_station))
test_gui.main(utils.toShortName(closest_station), choosen_line, direction)

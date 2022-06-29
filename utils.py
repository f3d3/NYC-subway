import numpy as np
import re
from geopy import Nominatim

def coordinates(address):
	nom = Nominatim(user_agent="f3d3.96@live.it")
	location = nom.geocode(address)
	coordinates = np.array([location.longitude, location.latitude])
	return coordinates
	#return location.longitude, location.latitude


def string_found(string1, string2):
   if re.search(r"\b" + re.escape(string1) + r"\b", string2):
      return True
   return False


def make_ordinal(n):
	'''
	Convert an integer into its ordinal representation::

		make_ordinal(0)   => '0th'
		make_ordinal(3)   => '3rd'
		make_ordinal(122) => '122nd'
		make_ordinal(213) => '213th'
	'''
	n = int(n)
	suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
	if 11 <= (n % 100) <= 13:
		suffix = 'th'
	return str(n) + suffix


def remove_ordinal(string):
	'''
	Convert an ordinal number into its integer representation inside a string::
	'''
	found = re.search(r'\d{2,3}[a-zA-Z]{2,3}',string)

	if found:
		to_change = found.group(0)
		stripped = to_change[:-2]
		string = string.replace(to_change, stripped)

	return string



def toLongName(direction):
	#AVENUE
	if string_found('Av', direction):
		direction = direction.replace('Av', 'Avenue')
	#AVENUES
	if string_found('Avs', direction):
		direction = direction.replace('Avs', 'Avenues')
	#STREET
	if string_found('St', direction):
		direction = direction.replace('St', 'Street')
	#BOULEVARD
	if string_found('Blvd', direction):
		direction = direction.replace('Blvd', 'Boulevard')
	#HEIGHTS
	if string_found('Hts', direction):
		direction = direction.replace('Hts', 'Heigths')
	#PARKWAY
	if string_found('Pkwy', direction):
		direction = direction.replace('Pkwy', 'Parkway')
	#ROAD
	if string_found('Rd', direction):
		direction = direction.replace('Rd', 'Road')
	#SQUARE
	if string_found('Sq', direction):
		direction = direction.replace('Sq', 'Square')
	#YARDS
	if string_found('Yds', direction):
		direction = direction.replace('Yds', 'Yards')
	#NUMBER
	direction = re.sub(r'\d+' , lambda m: make_ordinal(m.group()), direction)
	return direction





#I NEED TO REMOVE TH/ST... AND REPLACE AVE, STREET, ... 
def toShortName(direction):
	#AVENUE
	if string_found('Ave', direction):
		direction = direction.replace('Ave', 'Av')
	#AVENUES
	if string_found('Aves', direction):
		direction = direction.replace('Aves', 'Avs')
	return direction








import requests, os, base64

class OpenWeatherMap:
	APPID = '2a8522a215f76a435f8630d086d9f1e8'

	def __init__(self):
		self.url = "http://api.openweathermap.org/data/2.5/weather?appid={appid}&q={city}&units=metric"
		self.json = {}

	def get_city(self, city):
		url = self.url.format(appid=OpenWeatherMap.APPID, city=city)
		self.json = requests.get(url).json()
		return self.json

	def get(self, key):
		return self.json['main'][key]

	def get_icon_data(self):
		icon_id = self.json['weather'][0]['icon']

		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "images/weather/"+icon_id+".png"
		abs_file_path = os.path.join(script_dir, rel_path)

		return abs_file_path
import tkinter as tk
import requests, base64, os

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

		with open(abs_file_path, "rb") as image_file:
			return base64.b64encode(image_file.read())


class OWIconLabel(tk.Label):
	def __init__(self, parent, **kwargs):
		weather_icon = kwargs.pop('weather_icon', None)
		if weather_icon is not None:
			self.photo = tk.PhotoImage(data=weather_icon)
			kwargs['image'] = self.photo

		super().__init__(parent, **kwargs)


class App(tk.Tk):

	def __init__(self):
		super().__init__()
		self.geometry("500x500+0+0")
		self.configure(bg='white')

		owm = OpenWeatherMap()
		owm.get_city('New+York+City')

		temperature = owm.get('temp')

		temp_icon = OWIconLabel(self, weather_icon=owm.get_icon_data(), bg="white")
		temp_icon.grid(row=0, column=0)

		self.temp = tk.Label(self,
							 text='{} deg celcius'.format(temperature),
							 font=("Helvetica", 15), bg='black', fg='white')
		self.temp.grid(row=1, column=0)


if __name__ == '__main__':
	App().mainloop()
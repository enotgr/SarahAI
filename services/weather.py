import requests

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import get_suffix

class Weather:
  def get_weather(self, city: str):
    if not city:
      return None

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

    res = ''

    try:
      weather_data = requests.get(url).json()
      weather = weather_data['weather'][0]['description']

      temperature = round(weather_data['main']['temp'])
      temperature_feels = round(weather_data['main']['feels_like'])

      temperature_degrees_word = get_suffix(temperature, ['градус', 'градуса', 'градусов'])
      temperature_feels_degrees_word = get_suffix(temperature_feels, ['градус', 'градуса', 'градусов'])
      res = f'Сейчас в городе {city.title()} {weather}. Температура {temperature} {temperature_degrees_word} Цельсия. Ощущается как {temperature_feels} {temperature_feels_degrees_word}'
    except:
      res = 'Запрос не удался.'
    return res

weather = Weather()

import requests
from pprint import pprint
import json

with open('weather_id.txt','r') as file_id:
    weather_id = str(file_id.read())


print("Enter a city")
city = str(input())

url = '''http://api.openweathermap.org/data/2.5/weather?q={},IT&APPID=%s'''.format(city)%weather_id

res = requests.get(url)

data = res.json()

if data['cod'] == '404':
    print("city not found")

#print(data)
print(data['weather'][0]['description'])

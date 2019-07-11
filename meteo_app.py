from flask  import Flask, render_template, request, flash, jsonify, url_for
import requests
import json
import os

weather_app = Flask(__name__)

#Legge il file dove sta il token di OpenWeatherMap
with open('weather_id.txt','r') as file_id:
    weather_id = str(file_id.read())

#Dizionario in cui sono memorizzzati i codici le olettere iniziali di ogni paese
country_dict = {
'Italy':'IT',
'United Kingdom':'UK',
'Germany':'DE',
'U.S.A':'US',
'France':'FR',
'Russia':'RU',
'Spain':'ES'
}

@app.route('/')
def index():
    return render_template("weather_template.html")

@app.route('/get_weather',methods=['POST'])
def get_city():

    #Prende i dati in input dalle form
    city_name_input = request.form['city_input']
    country_name = request.form['country_input']
    country_code = country_dict[country_name]

    #richiesta all'url di OpenWeatherMap con il nome della città e il paese
    url = '''http://api.openweathermap.org/data/2.5/weather?q='''+ city_name_input + ','+ country_code + '''&APPID='''+ weather_id + '''&units=metric'''

    res = requests.get(url)
    #dati in formato json
    data = res.json() 
    data_code_response = data['cod']

    #Sistema il nome della città in input
    city_name = city_name_input.capitalize()

    if request.method == 'POST':
        if  data_code_response == '404':
            message = "City\t" + str(city_name) + "\t not found"
            return render_template("weather_template.html",message_error = message)
        
        if data_code_response == 200:
            #Dati meteo della giornata corrente
            weather_description = data['weather'][0]['description']
            weather_temp = data['main']['temp']  
            weather_humidity = data['main']['humidity']
            weather_pressure = data['main']['pressure']
            weather_windspeed = data['wind']['speed']

        return render_template("weather_template.html", 
            city_name = city_name,
            weather_description = weather_description,
            weather_temp = weather_temp, 
            weather_humidity = weather_humidity,
            weather_pressure = weather_pressure,
            weather_windspeed = weather_windspeed )

    return render_template("weather_template.html")

#updates css when changed
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

    
if __name__ == '__main__':
    app.run(debug=True)
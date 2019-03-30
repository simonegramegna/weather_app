from flask  import Flask, render_template, request, flash, jsonify, url_for
#from flask_bootstrap import Bootstrap
#from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Form, validators
from wtforms.validators import DataRequired, Length
import requests
import json
import os

app = Flask(__name__)

#reads a file with OpenWeatherapi token
with open('weather_id.txt','r') as file_id:
    weather_id = str(file_id.read())

#country_dict
country_dict = {
'Italy':'IT',
'United Kingdom':'UK',
'Germany':'DE',
'U.S.A':'US'
}



@app.route('/')
def index():
    return render_template("weather_template.html")

@app.route('/get_city',methods=['POST'])
def get_city():

    #gets data form the two text forms
    city_name = request.form['city_input']
    country_name = request.form['country_input']
    country_code = country_dict[country_name]
    
    url = '''http://api.openweathermap.org/data/2.5/weather?q='''+ city_name + ','+ country_code + '''&APPID='''+ weather_id + '''&units=metric'''

    res = requests.get(url)
    data = res.json()
    data_code_response = data['cod']
    
    if  data_code_response == '404':
        message = "City\t" + str(city_name) + "\t not found"
        return render_template("weather_template.html",message_error = message)
        
    if data_code_response == 200:
        #gets weather data
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

@app.route('/get_ip',methods=['GET'])
def get_client_ip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

#updates css when changed
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

    
if __name__ == '__main__':
    app.run(debug=True)

from flask  import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField, Form
#from wtforms.validators import DataRequired, Length
import requests
import json

app = Flask(__name__)

#reads a file with OpenWeatherapi token
with open('weather_id.txt','r') as file_id:
    weather_id = str(file_id.read())

#country_dict
country_dict = {'Italy':'IT','United Kingdom':'UK','Germany':'DE','U.S.A':'US'}
 
@app.route('/')
def index():
    return render_template("home.html")

@app.route('/get_city',methods=['POST'])
def get_city():
    city_name = request.form['city_input']
    country_name = request.form['country_input']
    country_code = country_dict[country_name]
    
    
    
    url = '''http://api.openweathermap.org/data/2.5/weather?q='''+ city_name + ','+ country_code + '''&APPID='''+ weather_id

    res = requests.get(url)
    data = res.json()
    
    if data['cod'] == '404':
        message = "City\t" + str(city_name) + "\t not found"
        return render_template("home.html",message_error = message)
    else:
        weather_data_description = data['weather'][0]['description']
        weather_data_response = "Weather today in \t "+ str(city_name) +"\tis\t" + str(weather_data_description)
        return render_template("home.html",weather_data = weather_data_response)

    return render_template("home.html")
  
if __name__ == '__main__':
    app.run(debug=True)

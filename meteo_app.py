from flask  import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField, Form
#from wtforms.validators import DataRequired, Length
import requests
import json

app = Flask(__name__)



with open('weather_id.txt','r') as file_id:
    weather_id = str(file_id.read())
 




@app.route('/')
def index():
    return render_template("home.html")

@app.route('/get_city',methods=['POST'])
def get_city():
    city_name = request.form['city_input']
    url = '''http://api.openweathermap.org/data/2.5/weather?q={},IT&APPID=%s'''.format(city_name)%weather_id
    res = requests.get(url)
    data = res.json()
    message = ""
    weather_data = ""
    if data['cod'] == '200':
        message = "City not found"
    else:
        weather_data = data['weather'][0]['description']
    
    #weather_data = data#['weather'][0]['description']
    #print(data['weather'][0]['description'])
    

    


    
    return render_template("home.html",message_error = message, meteo_data = weather_data)
  
  
if __name__ == '__main__':
    app.run(debug=True)

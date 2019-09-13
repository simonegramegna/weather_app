from flask  import Flask, render_template,request, flash, jsonify, url_for
import requests
import os

app = Flask(__name__)

#Legge il file dove sta il token di OpenWeatherMap
with open('weather_id.txt','r') as file_id:
    weather_id = str(file_id.read())

@app.route('/')
def index():
    return render_template("weather_template.html")


@app.route('/weather_today',methods=['POST'])
def get_weather_today():

    city_input = request.form['city_input']

    if request.method == 'POST':

        city =  city_input.capitalize()

        url = '''http://api.openweathermap.org/data/2.5/weather?q='''+ city + '''&APPID=''' + weather_id + '''&units=metric'''

        res = requests.get(url)
        #dati in formato json
        data = res.json()

        data_code = str(data['cod'])
        
        if data_code  == '404':

            city = "The city \t "+ city + '\t not found'

            return jsonify({ 'response' : data_code, 
                             'city': city })

        else:
            
            return jsonify({
                'response' : data_code,
                'condition_code': int(data['weather'][0]['id']),
                'weather_description' : data['weather'][0]['description'],
                'weather_temp_min' : data['main']['temp_min'],
                'weather_temp_max' : data['main']['temp_max'],
                'city': city })

        
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
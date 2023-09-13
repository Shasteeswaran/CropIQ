import tkinter as tk
import requests
import time
import geocoder

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('location.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the user's latitude and longitude based on their IP address
    location = geocoder.ip('me')
    lat, lon = location.latlng

    api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=0603f3c802faa6f37f121b62b356fc3a"
    '''
    canvas = tk.Tk()
    canvas.geometry("600x500")
    canvas.title("Weather App")
    f = ("poppins", 15, "bold")
    t = ("poppins", 35, "bold")
    get_weather_button = tk.Button(canvas, text="Get Weather", command=predict, font=t)
    get_weather_button.pack(pady=20)
    label1 = tk.Label(canvas, font=t)
    label1.pack()
    label2 = tk.Label(canvas, font=f)
    label2.pack()
    canvas.mainloop()'''


    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))


    '''final_info = condition + "\n" + str(temp) + "°C" 
    final_data = "\n"+ "Min Temp: " + str(min_temp) + "°C" + "\n" + "Max Temp: " + str(max_temp) + "°C" +"\n" + "Pressure: " + str(pressure) + "\n" +"Humidity: " + str(humidity) + "\n" +"Wind Speed: " + str(wind) + "\n" + "Sunrise: " + sunrise + "\n" + "Sunset: " + sunset
    label1.config(text = final_info)
    label2.config(text = final_data)'''


    return render_template('location.html', temperature=temp,min_temperature=min_temp,max_temperature=max_temp, humidity=humidity, condition=condition, wind=wind )


if __name__ == '__main__':
    app.run(port = 3000, debug=True)    

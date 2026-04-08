import requests
from const.keys import open_weather_key

def getWeather(location: str) -> str:
    
    # api calling of weather
    api = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={open_weather_key}&units=metric")
    
    data = api.json()

    #return the data
    return data

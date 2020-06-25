from math import floor

from colorama import Fore, init
import requests
from datetime import datetime
from . import models

init()


def get_data():
    # defining the cities where we want to get the weather
    city_list = ["75000", "13000", "69002", "31000", "06000", "44000", "34000", "67000", "33000",
                 "59800", "35000", "51100", "83000", "38000", "59310", "59210", "61200", "78000", "59500"]
    # getting the weather for each previous city for 5 days
    for city in city_list:
        request = "http://api.openweathermap.org/data/2.5/forecast?zip={zip},fr&appid=870aa2e09b50f48983ad62061fabb082"
        request = request.replace("{zip}", city)
        print(request)
        res = requests.post(request)
        # checking ig we get a response from the API
        if res.json().get("cod") == "200" and res.json().get("list"):
            list_data = res.json().get("list")
            needed_data = []
            for cur_time_data in list_data:
                if cur_time_data.get("dt") % (3600 * 24) == 43200:
                    needed_data.append(cur_time_data)
            parse_data(needed_data, res.json().get("city"))


# parsing the data from the db
def parse_data(data, city):
    for curData in data:
        weather = {
            "temp": None,
            "weather": None,
            "city": None,
            "lat": None,
            "long": None,
            "date": None
        }
        # getting temperature in °C
        if curData.get("main"):
            if curData.get("main").get("temp"):
                weather["temp"] = curData.get("main").get("temp") + 273.15

        # getting the type of weather
        if curData.get("weather"):
            if curData.get("weather")[0].get("description"):
                weather["weather"] = curData.get("weather")[0].get("description")

        # getting the name of the city
        if city.get("name"):
            weather["city"] = city.get("name")

        # getting the latitude and the longitude of the city
        if city.get("coord"):
            if city.get("coord").get("lat"):
                weather["lat"] = city.get("coord").get("lat")
            if city.get("coord").get("lon"):
                weather["long"] = city.get("coord").get("lon")

        # getting the time of the weather
        if curData.get("dt"):
            timestamp = curData.get("dt")
            weather["date"] = datetime.fromtimestamp(timestamp)


        # adding the weather to the db
        b = models.Weather(Temperature_Weather=weather['temp'], Weather_Weather=weather['weather'],
                           City_Weather=weather['city'], Latitude_Weather=weather['lat'],
                           Longitude_Weather=weather['long'], Date_Weather=weather['date'])
        b.save()

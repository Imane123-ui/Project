from math import floor

from colorama import Fore, init
import requests
from datetime import datetime
from . import models

init()


def get_data():
    city_list = ["75000", "13000", "69002", "31000", "06000", "44000", "34000", "67000", "33000",
                 "59800", "35000", "51100", "83000", "38000"]
    for city in city_list:
        request = "http://api.openweathermap.org/data/2.5/forecast?zip={zip},fr&appid=870aa2e09b50f48983ad62061fabb082"
        request = request.replace("{zip}", city)
        print(request)
        res = requests.post(request)
        if res.json().get("cod") == "200" and res.json().get("list"):
            list_data = res.json().get("list")
            cur_time = ""
            needed_data = []
            for cur_time_data in list_data:
                if cur_time_data.get("dt") % (3600 * 24) == 43200:
                    needed_data.append(cur_time_data)
            parse_data(needed_data, res.json().get("city"))


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
        if curData.get("main"):
            if curData.get("main").get("temp"):
                weather["temp"] = curData.get("main").get("temp") + 273.15

        if curData.get("weather"):
            if curData.get("weather")[0].get("description"):
                weather["weather"] = curData.get("weather")[0].get("description")

        if city.get("name"):
            weather["city"] = city.get("name")

        if city.get("coord"):
            if city.get("coord").get("lat"):
                weather["lat"] = city.get("coord").get("lat")
            if city.get("coord").get("lon"):
                weather["long"] = city.get("coord").get("lon")
        if curData.get("dt"):
            timestamp = curData.get("dt")
            weather["date"] = datetime.fromtimestamp(timestamp)

        # TODO: add weather to db
        b = models.Weather(Temperature_Weather=weather['temp'], Weather_Weather=weather['weather'],
                           City_Weather=weather['city'], Latitude_Weather=weather['lat'],
                           Longitude_Weather=weather['long'], Date_Weather=weather['date'])
        b.save()

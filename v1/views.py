import ijson
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import requests
from rdflib import Graph
from colorama import Fore, init
from . import poi_api, weather_api

init()
g = Graph()


def index(request):
    isConnected = False
    return render(request, "v1/index.html", locals())


def test(request):
    # fileName = poi_api.download_file()    TODO: uncomment
    # poi_api.parse_file(fileName)          TODO: uncomment
    poi_api.parse_file("dfdd6504-b41b-4e6e-bde8-12937636375d.json")
    # weather_api.get_data()
    return HttpResponse("<h1>titre</h1>")



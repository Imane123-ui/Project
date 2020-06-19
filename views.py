from django.shortcuts import render
from django.http import HttpResponse
from page.models import Place

def place_list(request):
    place=[]
    for p in Place.objects.all():
        place.append(p.Name_Place)
    body = '<br/>'.join(place)
    return HttpResponse(body)
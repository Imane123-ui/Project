from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def index(request):
    isConnected = False
    return render(request, "v1/index.html", locals())

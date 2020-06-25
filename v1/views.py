import ijson
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from rdflib import Graph
from colorama import Fore, init
from . import poi_api
from .advanced_research_form import ResearchForm
from . import models

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import PrefForm
from .models import Profil
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from .account_creation_form import AccountCreation
from .login_form import Login
from .profil_form import EditProfile

init()
g = Graph()


# updates the data bases (places and weathers)
def update(request):
    models.Weather.objects.all().delete()
    models.Place.objects.all().delete()
    weather_api.get_data()
    fileName = poi_api.download_file()  # TODO: uncomment
    poi_api.parse_file(fileName)  # TODO: uncomment
    return render(request, "v1/index.html", locals())


# view used when the advanced research page is called
def research(request):
    if request.method == "POST":
        myForm = ResearchForm(request.POST)
        # when a form is submitted from this page and data are correct, this condition is True
        if myForm.is_valid():
            researchContent = myForm.cleaned_data["researchContent"]
            arrivalDate = myForm.cleaned_data["arrivalDate"]
            leavingDate = myForm.cleaned_data["leavingDate"]
            children = myForm.cleaned_data["children"]
            disabled = myForm.cleaned_data["disabled"]
            wifi = myForm.cleaned_data["wifi"]
            parking = myForm.cleaned_data["parking"]
            latitudeField = myForm.cleaned_data["latitudeField"]
            longitudeField = myForm.cleaned_data["longitudeField"]
            distanceField = myForm.cleaned_data["distanceField"]
            priceField = myForm.cleaned_data["priceField"]
            # case there is no price given
            try:
                priceField = float(priceField)
            except ValueError:
                priceField = sys.float_info.max
            res = models.Place.objects.all()
            # TODO: add conditions
            places = res.filter(
                (Q(Name_Place__icontains=researchContent) | Q(Description_Place__icontains=researchContent))
                & (Q(Price_Place__lte=priceField) | Q(Price_Place__exact="")))
            # matching each matching place to the distance with the user
            resultsPair = []
            for place in places:
                if place.Latitude_Place != "" and place.Longitude_Place != "":
                    dist = distance2points(latitudeField, longitudeField, place.Latitude_Place, place.Longitude_Place)
                    resultsPair.append([dist[0], place, round(dist[0])])

            # keeping only the 10 first results
            resultsPair.sort(key=lambda x: x[0])
            if distanceField:
                idx = 0
                for curPair in resultsPair:
                    while curPair and curPair[0] > float(distanceField):
                        resultsPair.remove(curPair)
                        if len(resultsPair) > idx:
                            curPair = resultsPair[idx]
                        else:
                            curPair = None
                    idx += 1
            resultsPair = resultsPair[:10]

            form = Index()
            return render(request, "v1/Tripsy_resultat.html", locals())
    form = ResearchForm()
    return render(request, "v1/Tripsy_recherche.html", locals())


# View used when the main page of the site is called
def index(request):
    form = Index(request.POST or None)
    # this condition returns True if there is a research from this page and datas are correct
    if form.is_valid():
        researchContent = form.cleaned_data["researchField"]
        latitudeField = form.cleaned_data["latitudeField"]
        longitudeField = form.cleaned_data["longitudeField"]
        res = models.Place.objects.all()
        places = res.filter(Q(Name_Place__icontains=researchContent) | Q(Description_Place__icontains=researchContent))
        # matching places to distances with the user
        resultsPair = []
        for place in places:
            if place.Latitude_Place != "" and place.Longitude_Place != "":
                dist = distance2points(latitudeField, longitudeField, place.Latitude_Place, place.Longitude_Place)
                resultsPair.append([dist[0], place, round(dist[0])])
        resultsPair.sort(key=lambda x: x[0])
        # keeping the 10 first result
        resultsPair = resultsPair[:10]
        return render(request, "v1/Tripsy_resultat.html", locals())
    form = Index()
    return render(request, 'v1/index.html', locals())


# the view is called when a user goes to the connexion page
def connexion(request):
    print("connexion page")
    form = Login(request.POST or None)
    # if the user is already connected, he is redirected to the index page
    if request.user.is_authenticated:
        form = Index()
        return render(request, "v1/index.html", locals())

    # if datas are corrects, then this condition returns True
    if form.is_valid():
        print("form valid")
        user = User.objects.all().filter(email__exact=form.cleaned_data["emailField"])
        # check if a user exists in the db with this email
        if user.count() == 1:
            user = user.first()
            # check if the given password matches the one in the db
            if user.check_password(form.cleaned_data["passwordField"]):
                print("password: ok")
                login(request, user)
                error = False
                return render(request, 'v1/index.html', locals())
        else:
            print(Fore.RED + "error detected" + Fore.RESET)
            error = True
    user = None
    return render(request, 'v1/Tripsy_connexion.html', locals())


# this view is called when a user goes to the registration page
def create_account(request):
    form = AccountCreation(request.POST or None)
    # if all given datas are valid, this condition is True
    if form.is_valid():
        # cheching if both passwords are the same
        if form.cleaned_data['passwordField'] == form.cleaned_data['confirmPasswordField']:
            # checking is there is not already an account in the db using the email
            if User.objects.all().filter(email__iexact=form.cleaned_data['emailField']).count() == 0:
                # adding user to Django's User table
                user = User.objects.create_user(first_name=form.cleaned_data['firstnameField'],
                                                last_name=form.cleaned_data['nameField'],
                                                username=form.cleaned_data['nicknameField'],
                                                email=form.cleaned_data['emailField'],
                                                password=form.cleaned_data['passwordField'])
                # adding others data to our "Profile" table in the db
                profil = Profil(user=user, tel=form.cleaned_data['phoneField'],
                                birthday=form.cleaned_data['birthdayField'],
                                pref1="Aucune", pref2="Aucune", pref3="Aucune", pref4="Aucune")
                profil.save()
                return index(request)
            else:
                error = True
        else:
            error = True

    return render(request, 'v1/Tripsy_creation.html', locals())


# view called when a user clicks the "disconnect" button
def logout(request):
    django_logout(request)
    return render(request, 'v1/index.html')


# view called when a user accesses his profile page
@login_required(login_url='/connexion')
def profil(request):
    formProfile = EditProfile(request.POST or None)
    # this condition is True when the datas in the personal information part are valid
    if formProfile.is_valid():
        # check if the old password is good
        if request.user.check_password(formProfile.cleaned_data["oldPasswordField"]):
            print("old password: ok")
            # if there nickname field is not empty, then we change it in the db
            if formProfile.cleaned_data["nicknameField"]:
                print("name changed: " + formProfile.cleaned_data["nicknameField"])
                request.user.username = formProfile.cleaned_data["nicknameField"]
                request.user.save()
            # if there password field is not empty and new passwords are equal, then we change it in the db
            if formProfile.cleaned_data["newPasswordField"] and formProfile.cleaned_data["newPasswordField"] == \
                    formProfile.cleaned_data["confirmNewPasswordField"]:
                print("password changed: " + formProfile.cleaned_data["newPasswordField"])
                request.user.set_password(formProfile.cleaned_data["newPasswordField"])
                request.user.save()
                return index(request)
    user = request.user
    login(request, user)
    return render(request, 'v1/Tripsy_mes_informations.html', locals())


# the view is called when the user accesses a place's details page
def details(request, id):
    result = models.Place.objects.all().filter(ID_Place__exact=id).first()
    weathers = []
    idx = 0
    # getting the 5 first weathers of this place (it should be impossible to have more than 5 but who knows what
    # could happend...)
    for weather in result.Weather_Place.all():
        if idx < 5:
            weathers.append(weather)
            idx += 1
    return render(request, "v1/Tripsy_details.html", locals())

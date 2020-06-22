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


def test(request):
    # fileName = poi_api.download_file()    TODO: uncomment
    # poi_api.parse_file(fileName)          TODO: uncomment
    poi_api.parse_file("dfdd6504-b41b-4e6e-bde8-12937636375d.json")
    # weather_api.get_data()
    return HttpResponse("<h1>titre</h1>")


def research(request):
    if request.method == "POST":
        myForm = ResearchForm(request.POST)
        if myForm.is_valid():
            researchContent = myForm.cleaned_data["researchContent"]
            arrivalDate = myForm.cleaned_data["arrivalDate"]
            leavingDate = myForm.cleaned_data["leavingDate"]
            children = myForm.cleaned_data["children"]
            disabled = myForm.cleaned_data["disabled"]
            wifi = myForm.cleaned_data["wifi"]
            parking = myForm.cleaned_data["parking"]
            res = models.Place.objects.all()
            # TODO: add conditions
            places = res.filter(Name_Place__icontains=researchContent, Description_Place__icontains=researchContent)
            places = places[:3]
            return render(request, "v1/Tripsy_resultat.html", locals())
    form = ResearchForm()
    return render(request, "v1/Tripsy_recherche.html", locals())


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        connected = True
    else:
        connected = False
    return render(request, 'v1/index.html', locals())


def connexion(request):
    print("connexion page")
    form = Login(request.POST or None)
    if request.user.is_authenticated:
        return render(request, "v1/index.html", locals())
    if form.is_valid():
        print("form valid")
        user = User.objects.all().filter(email__exact=form.cleaned_data["emailField"])
        print(user.count())
        if user.count() == 1:
            user = user.first()
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


def create_account(request):
    form = AccountCreation(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data['firstnameField'])
        if form.cleaned_data['passwordField'] == form.cleaned_data['confirmPasswordField']:
            if User.objects.all().filter(email__iexact=form.cleaned_data['emailField']).count() == 0:
                user = User.objects.create_user(first_name=form.cleaned_data['firstnameField'],
                                                last_name=form.cleaned_data['nameField'],
                                                username=form.cleaned_data['nicknameField'],
                                                email=form.cleaned_data['emailField'],
                                                password=form.cleaned_data['passwordField'])
                profil = Profil(user=user, tel=form.cleaned_data['phoneField'],
                                birthday=form.cleaned_data['birthdayField'],
                                pref1="Aucune", pref2="Aucune", pref3="Aucune", pref4="Aucune")
                profil.save()
                login(request, user)
                return render(request, "v1/index.html", locals())
            else:
                error = True
        else:
            error = True

    return render(request, 'v1/Tripsy_creation.html', locals())


def logout(request):
    django_logout(request)
    return render(request, 'v1/index.html')


@login_required(login_url='/connexion')
def profil(request):
    formProfile = EditProfile(request.POST or None)
    # if form.is_valid():
    #     request.user.profil.pref1 = form.cleaned_data['pref1']
    #     request.user.profil.pref2 = form.cleaned_data['pref2']
    #     request.user.profil.pref3 = form.cleaned_data['pref3']
    #     request.user.profil.pref4 = form.cleaned_data['pref4']
    #     request.user.profil.save()
    if formProfile.is_valid():
        if request.user.check_password(formProfile.cleaned_data["oldPasswordField"]):
            print("old password: ok")
            if formProfile.cleaned_data["nicknameField"]:
                print("name changed: " + formProfile.cleaned_data["nicknameField"])
                request.user.username = formProfile.cleaned_data["nicknameField"]
                request.user.save()
            if formProfile.cleaned_data["newPasswordField"] and formProfile.cleaned_data["newPasswordField"] == formProfile.cleaned_data["confirmNewPasswordField"]:
                print("password changed: " + formProfile.cleaned_data["newPasswordField"])
                request.user.set_password(formProfile.cleaned_data["newPasswordField"])
                request.user.save()
    user = request.user
    login(request, user)
    return render(request, 'v1/Tripsy_mes_informations.html', locals())

from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    ID_Place = models.AutoField(primary_key=True)
    Name_Place = models.CharField(max_length=100, default="")
    Address_Place = models.CharField(max_length=200, default="")
    Latitude_Place = models.CharField(max_length=10, default="")
    Longitude_Place = models.CharField(max_length=10, default="")
    Rating_Place = models.CharField(max_length=10, default="")
    Photo_Place = models.CharField(max_length=500, default="")
    Link_Place = models.CharField(max_length=500, default="")
    Description_Place = models.TextField(max_length=2000, default="")
    Price_Place = models.CharField(max_length=50, default="")
    City_Place = models.CharField(max_length=50, default="")
    Phone_Place = models.CharField(max_length=50, default="")
    Meteo1_Place = models.CharField(max_length=50, default="")
    Meteo2_Place = models.CharField(max_length=50, default="")
    Meteo3_Place = models.CharField(max_length=50, default="")
    Meteo4_Place = models.CharField(max_length=50, default="")
    Meteo5_Place = models.CharField(max_length=50, default="")

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (
        self.ID_Place, self.Name_Place, self.Address_Place, self.Latitude_Place, self.Longitude_Place,
        self.Rating_Place, self.Photo_Place, self.Link_Place, self.Description_Place, self.Price_Place, self.City_Place,
        self.Phone_Place, self.Meteo1_Place, self.Meteo2_Place, self.Meteo3_Place, self.Meteo4_Place, self.Meteo5_Place)


class Category(models.Model):
    ID_Category = models.AutoField(primary_key=True)
    Name_Category = models.CharField(max_length=100)

    def __str__(self):
        return '%s %s' % (self.ID_Category, self.Name_Category)


class Type(models.Model):
    ID_Type = models.AutoField(primary_key=True)
    Name_Type = models.CharField(max_length=100)

    def __str__(self):
        return '%s %s' % (self.ID_Type, self.Name_Type)


    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s' % (
        self.ID_User, self.Name_User, self.Surname_User, self.Birthdate_User, self.Address_User, self.Latitude_User,
        self.Longitude_User, self.City_User, self.Email_User, self.Phone_User, self.Password_User, self.Visited_User)


class Weather(models.Model):
    ID_Weather = models.AutoField(primary_key=True)
    Temperature_Weather = models.IntegerField(blank=True)
    Weather_Weather = models.CharField(max_length=100)
    City_Weather = models.CharField(max_length=100)
    Latitude_Weather = models.CharField(max_length=10, default='')
    Longitude_Weather = models.CharField(max_length=10)
    Date_Weather = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (
        self.ID_Weather, self.Temperature_Weather, self.Weather_Weather, self.City_Weather, self.Latitude_Weather,
        self.Longitude_Weather, self.Date_Weather)


class Hobby(models.Model):
    ID_Hobby = models.AutoField(primary_key=True)
    Name_Hobby = models.CharField(max_length=100)

    def __str__(self):
        return '%s %s' % (self.ID_Hobby, self.Name_Hobby)


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # La liaison OneToOne vers le modèle User
    tel = models.IntegerField(blank=True)
    birthday = models.DateField(blank=True)
    pref1 = models.CharField(blank=True, max_length=50)
    pref2 = models.CharField(blank=True, max_length=50)
    pref3 = models.CharField(blank=True, max_length=50)
    pref4 = models.CharField(blank=True, max_length=50)

from django.db import models

 

class Place(models.Model):
    ID_Place = models.AutoField(primary_key=True)
    Name_Place = models.CharField(max_length=100)
    Address_Place = models.CharField(max_length=200)
    Latitude_Place = models.CharField(max_length=10)
    Longitude_Place = models.CharField(max_length=10)
    Rating_Place = models.CharField(max_length=10)
    Photo_Place = models.CharField(max_length=500)
    Link_Place = models.CharField(max_length=500)
    Description_Place = models.CharField(max_length=2000)
    Price_Place = models.CharField(max_length=50)
    City_Place = models.CharField(max_length=50)
    Phone_Place = models.CharField(max_length=50)
    Meteo1_Place = models.CharField(max_length=50)
    Meteo2_Place = models.CharField(max_length=50)
    Meteo3_Place = models.CharField(max_length=50)
    Meteo4_Place = models.CharField(max_length=50)
    Meteo5_Place = models.CharField(max_length=50)
    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s'%(self.ID_Place, self.Name_Place, self.Address_Place, self.Latitude_Place, self.Longitude_Place, self.Rating_Place, self.Photo_Place, self.Link_Place, self.Description_Place,self.Price_Place, self.City_Place, self.Phone_Place, self.Meteo1_Place, self.Meteo2_Place, self.Meteo3_Place, self.Meteo4_Place, self.Meteo5_Place)

 

class Category(models.Model):
    ID_Category = models.AutoField(primary_key=True)
    Name_Category = models.CharField(max_length=100)
    def __str__(self):
        return '%s %s'%(self.ID_Category, self.Name_Category)

 

class Type(models.Model):
    ID_Type = models.AutoField(primary_key=True)
    Name_Type = models.CharField(max_length=100)
    def __str__(self):
        return '%s %s'%(self.ID_Type, self.Name_Type)

 

class User(models.Model):
    ID_User = models.AutoField(primary_key=True)
    Name_User = models.CharField(max_length=100)
    Surname_User = models.CharField(max_length=100)
    Birthdate_User = models.DateField()
    Address_User = models.CharField(max_length=100)
    Latitude_User = models.CharField(max_length=10)
    Longitude_User= models.CharField(max_length=10)
    City_User = models.CharField(max_length=100)
    Email_User = models.EmailField(max_length=100)
    Phone_User = models.IntegerField()
    Password_User = models.CharField(max_length=50)
    Visited_User = models.CharField(max_length=50)
    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s %s %s'%(self.ID_User, self.Name_User, self.Surname_User, self.Birthdate_User, self.Address_User, self.Latitude_User, self.Longitude_User, self.City_User, self.Email_User, self.Phone_User, self.Password_User, self.Visited_User)

 

class Weather(models.Model):
    ID_Weather = models.AutoField(primary_key=True)
    Temperature_Weather = models.IntegerField()
    Weather_Weather = models.CharField(max_length=100)
    City_Weather = models.CharField(max_length=100)
    Latitude_Weather = models.CharField(max_length=10)
    Longitude_Weather = models.CharField(max_length=10)
    Date_Weather = models.DateField()
    def __str__(self):
        return '%s %s %s %s %s %s %s'%(self.ID_Weather, self.Temperature_Weather, self.Weather_Weather, self.City_Weather, self.Latitude_Weather, self.Longitude_Weather, self.Date_Weather)

 

class Hobby(models.Model):
    ID_Hobby = models.AutoField(primary_key=True)
    Name_Hobby = models.CharField(max_length=100)
    def __str__(self):
        return '%s %s'%(self.ID_Hobby, self.Name_Hobby)

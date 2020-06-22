from django import forms
from django.db import models


class AccountCreation(forms.Form):
    firstnameField = forms.CharField(label=False, widget=forms.TextInput(
        attrs={"placeholder": "Prénom", "class": "champ"}), required=True)

    nameField = forms.CharField(label=False, widget=forms.TextInput(
        attrs={"placeholder": "Nom", "class": "champ"}), required=True)

    nicknameField = forms.CharField(label=False, widget=forms.TextInput(
        attrs={"placeholder": "Nom d'utilisateur", "class": "champ"}), required=True)

    phoneField = forms.CharField(label=False, widget=forms.NumberInput(
        attrs={"placeholder": "Numéro de téléphone", "class": "champ"}), required=True)

    emailField = forms.CharField(label=False, widget=forms.EmailInput(
        attrs={"placeholder": "Adresse e-mail", "class": "champ"}), required=True)

    passwordField = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={"placeholder": "Mot de passe", "class": "champ"}), required=True)

    confirmPasswordField = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={"placeholder": "Confirmez le mot de passe", "class": "champ"}), required=True)

    birthdayField = forms.CharField(label=False, widget=forms.DateInput(
        attrs={"class": "champ", "type": "date"}), required=True)


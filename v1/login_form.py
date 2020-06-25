from django import forms


# form used for the login system
class Login(forms.Form):
    emailField = forms.CharField(widget=forms.TextInput(
        attrs={"class": "champ", "placeholder": "Email"}
    ), required=True)

    passwordField = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Mot de passe", "class": "champ"
    }), required=True)

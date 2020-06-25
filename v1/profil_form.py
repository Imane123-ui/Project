from django import forms


# TODO: create select-options

# setting the profil db with user's data that can't be store in Django's User db
class EditProfile(forms.Form):
    nicknameField = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Nom d'utilisateur", "class": "champ"
    }), required=False)

    oldPasswordField = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Ancien mot de passe (obligatoire)", "class": "champ"
    }), required=True)

    newPasswordField = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Nouveau mot de passe", "class": "champ"
    }), required=False)

    confirmNewPasswordField = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirmez le nouveau mot de passe", "class": "champ"
    }), required=False)

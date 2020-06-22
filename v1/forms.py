from django import forms



class Login(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=25, required=True, widget=forms.PasswordInput)


class PrefForm(forms.Form):
    CHOICES = (('0', 'Aucune'), ('1', 'Animaux autorisés'), ('2', 'Supérette à proximité'), ('3', 'Parking gratuit'),
               ('4', 'Wifi gratuit'), ('5', 'Enfants autorisés'), ('6', 'Accès handicapé'),)
    pref1 = forms.ChoiceField(choices=CHOICES)
    pref2 = forms.ChoiceField(choices=CHOICES)
    pref3 = forms.ChoiceField(choices=CHOICES)
    pref4 = forms.ChoiceField(choices=CHOICES)

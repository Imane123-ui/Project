from django import forms


# form for the main page research and the result research
class Index(forms.Form):
    researchField = forms.CharField(label=False, widget=forms.TextInput(
        attrs={"placeholder": "Chateau de Fontainebleau, Nîme ...", "class": "champ"}), required=True)

    latitudeField = forms.CharField(label=False, widget=forms.HiddenInput(attrs={
        "id": "latitudeField"
    }), required=True)
    longitudeField = forms.CharField(label=False, widget=forms.HiddenInput(attrs={
        "id": "longitudeField"
    }), required=True)

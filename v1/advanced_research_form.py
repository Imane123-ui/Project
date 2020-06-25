from django import forms


# form used for the advanced research
class ResearchForm(forms.Form):
    researchContent = forms.CharField(label=False, widget=forms.TextInput(
        attrs={"placeholder": "Chateau de Fontainebleau, Nîme ...", "class": "champ"}))

    arrivalDate = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], label="test", widget=forms.DateTimeInput(
        attrs={"class": "champ", "type": "date"}
    ), required=False)

    leavingDate = forms.DateTimeField(input_formats=['%d/%m/%Y'], label="test", widget=forms.DateTimeInput(
        attrs={"class": "champ", "type": "date"}
    ), required=False)

    # TODO: change these checkboxes to fit the type of trips
    children = forms.CharField(label="Enfants autorisés", widget=forms.CheckboxInput, required=False)
    disabled = forms.CharField(label="Accès handicapé", widget=forms.CheckboxInput, required=False)
    parking = forms.CharField(label="Parking gratuit", widget=forms.CheckboxInput, required=False)
    wifi = forms.CharField(label="Wifi gratuit", widget=forms.CheckboxInput, required=False)

    distance = forms.CharField(widget=forms.HiddenInput, required=False)
    price = forms.CharField(widget=forms.HiddenInput, required=False)


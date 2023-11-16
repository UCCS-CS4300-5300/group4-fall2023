from django import forms

class StarWarsForm(forms.Form):
    # No need to populate these choices here, they will be dynamically loaded via AJAX
    timeline = forms.ChoiceField(choices=[], required=True)
    character = forms.ChoiceField(choices=[], required=False)
    starship = forms.ChoiceField(choices=[], required=False)

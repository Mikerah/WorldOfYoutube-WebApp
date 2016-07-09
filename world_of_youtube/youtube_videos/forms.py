from django import forms

from .constants import COUNTRIES

class QueryForm(forms.Form):
    country = forms.ChoiceField(choices=COUNTRIES, required=True)
    category = forms.ChoiceField()
    number_of_videos_to_return = forms.IntegerField(max_value=50)
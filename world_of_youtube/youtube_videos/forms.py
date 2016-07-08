from django import forms

class QueryForm(forms.Form):
    country = forms.ChoiceField()
    category = forms.ChoiceField()
    number_of_videos_to_return = forms.IntegerField(max_value=50)
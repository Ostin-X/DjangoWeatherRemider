from django import forms


class CityForm(forms.Form):
    city = forms.CharField(max_length=100, label='Місто', widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(max_length=100, label='Країна', widget=forms.TextInput(attrs={'class': 'form-control'}))
    codename = forms.CharField(max_length=100, label='Кодове ім\'я',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

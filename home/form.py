from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class ShippingForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=20)
    country = CountryField().formfield(widget=CountrySelectWidget())
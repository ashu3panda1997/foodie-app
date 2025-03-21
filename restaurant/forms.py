from django import forms
from .models import Restaurant, FoodItem, Category


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone', 'email', 'opening_hours', 'logo']


class FoodItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a Category")

    class Meta:
        model = FoodItem
        fields = ['restaurant', 'category', 'name', 'price', 'description', 'is_available','image','food_type']


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, USER_ROLES
User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Make email mandatory
   # role = forms.ChoiceField(choices=USER_ROLES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Default Django fields

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .form import UserRegisterForm
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect("homepage")  # Redirect to home page after successful registration
    else:
        form = UserRegisterForm()

    return render(request, "account/register.html", {"form": form})


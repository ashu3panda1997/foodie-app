from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.timezone import now

from restaurant.models import Restaurant
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import random
from .models import OTP

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        print(user)
        # print(user.is_active)
        if user is not None and user.is_active:
            login(request, user)

            if user.is_authenticated:  # Use `user`, not `request.user`
                if hasattr(user, "role"):  # Ensure `role` exists
                    if user.role == "customer":
                        return redirect("homepage")

                    if user.role == "restaurant_owner":
                        try:
                            restaurant = Restaurant.objects.get(owner=user)
                            return redirect("restaurant_page", slug=restaurant.slug)
                        except Restaurant.DoesNotExist:
                            return redirect("homepage")  # Redirect to setup page if no restaurant exists

            return redirect("homepage")  # Default redirect for non-restaurants
        print('1')
        # If authentication fails, show an error message
        messages.error(request, "Invalid credentials, please try again.")

    else:
        form = AuthenticationForm()
        print('else')
    return render(request, "user/login.html", {"form": form})


def send_otp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = get_object_or_404(User, username=username)

        # Generate OTP
        otp_code = str(random.randint(100000, 999999))
        expiry_time = now() + timedelta(minutes=5)  # Set OTP expiry time

        # Store OTP in the database (Update if exists)
        otp_entry = OTP.objects.update_or_create(
            user=user, defaults={"otp": otp_code, "expires_at": expiry_time}
        )

        # Send OTP via email
        try:
            send_mail(
                "Your OTP Code",
                f"Your OTP is {otp_code}. It is valid for 5 minutes.",
                "noreply@yourdomain.com",  # Change this to your email
                [user.email],
                fail_silently=False,
            )
            return JsonResponse({"status": "success", "message": "OTP sent to your email!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Email sending failed: {str(e)}"})

    return JsonResponse({"status": "error", "message": "Invalid request!"})


def verify_otp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        otp_entered = request.POST.get("otp")

        user = get_object_or_404(User, username=username)

        # Get the latest OTP for the user
        otp_record = OTP.objects.filter(user=user).last()

        if otp_record and otp_record.otp == otp_entered:
            # Mark OTP as used (optional)
            otp_record.delete()

            # Log the user in
            login(request, user)

            return JsonResponse({"status": "success", "message": "OTP Verified! Logging in..."})
        else:
            return JsonResponse({"status": "error", "message": "Invalid OTP!"})

    return JsonResponse({"status": "error", "message": "Invalid request!"})

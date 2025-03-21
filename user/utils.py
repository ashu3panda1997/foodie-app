import random
from django.core.mail import send_mail
from django.utils.timezone import now

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = "Your OTP Code"
    message = f"Your OTP is {otp}. Please enter it to log in."
    send_mail(subject, message, "your-email@gmail.com", [email], fail_silently=False)

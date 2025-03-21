from django.contrib import admin
from django.urls import path
from user import views
app_names="user"
urlpatterns = [
    path('',views.login_view,name='login_user'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]
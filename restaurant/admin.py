from django.contrib import admin
from restaurant.models import Restaurant,FoodItem,Category
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(FoodItem)
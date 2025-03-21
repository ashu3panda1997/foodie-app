from django.urls import path
from .views import menu_page,restaurant_page,update_food,add_food_item,delete_food

urlpatterns = [
    path("restaurant/<slug:slug>/", restaurant_page, name="restaurant_page"),
    path('<int:restaurant_id>/menu/', menu_page, name='menu_page'),
    path("restaurant/<slug:restaurant_slug>/update/", update_food, name="update_food"),
    path("restaurant/<slug:restaurant_slug>/add-food/", add_food_item, name="add_food_item"),
    path("delete-food/<int:food_id>/", delete_food, name="delete_food"),

]

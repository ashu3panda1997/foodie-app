from django.urls import path
from .views import menu_page,restaurant_page,update_food,add_food_item,delete_food,manage_orders,update_order_status,delete_order

urlpatterns = [
    path("restaurant/<slug:slug>/", restaurant_page, name="restaurant_page"),
    path('<int:restaurant_id>/menu/', menu_page, name='menu_page'),
    path("restaurant/<slug:restaurant_slug>/update/", update_food, name="update_food"),
    path("restaurant/<slug:restaurant_slug>/add-food/", add_food_item, name="add_food_item"),
    path("delete-food/<int:food_id>/", delete_food, name="delete_food"),
    path("restaurant/<slug:restaurant_slug>/orders/<int:order_id>/delete/", delete_order, name="delete-order"),
    path("restaurant/<slug:restaurant_slug>/orders/<int:order_id>/update/", update_order_status, name="update-order"),
    path("restaurant/<slug:restaurant_slug>/orders/", manage_orders, name="restaurant-orders"),

]

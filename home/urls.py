from django.contrib import admin
from django.urls import path
from home import views
from .views import add_to_cart,cart_view,remove_from_cart,checkout_view,place_order,order_success,order_list,contact_submit
urlpatterns = [
    path('home/',views.homepage,name='homepage'),
    path('menu/<str:category_name>/',views.category_menu,name='category_menu'),
    path("add-to-cart/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_view, name="cart_view"),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('place_order/', place_order, name='place_order'),
    path('order-success/', order_success, name='order_success'),
    path('orders/', order_list, name='orders'),
    path("contact/", contact_submit, name="contact"),
]

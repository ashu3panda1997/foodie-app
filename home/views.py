from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Cart, CartItem, Order, OrderItem,ContactMessage
from django.contrib import messages
from .form import ShippingForm
from django.core.mail import send_mail
from django.conf import settings
from restaurant.models import Restaurant, FoodItem, Category
from collections import defaultdict
from django.contrib.auth import get_user_model

User = get_user_model()


def homepage(request):
    restaurants = Restaurant.objects.all()
    meal_type = Category.objects.values_list('meal_type', flat=True).distinct()
    categories = Category.objects.all()
    restaurant = Restaurant.objects.all()
    print('data:', categories)
    return render(request, 'home/home.html',
                  {'restaurants': restaurants, 'meal_type': meal_type, 'categories': categories,
                   'restaurant': restaurant})


def category_menu(request, category_name):
    category = get_object_or_404(Category, meal_type=category_name)

    # Fetch food items related to this category
    food_items = FoodItem.objects.filter(category=category).select_related('restaurant')

    # Debug: Print fetched food items
    print("Category:", category)
    print("Food Items:", food_items)

    # If no food items exist, print a message
    if not food_items:
        print("No food items found for category:", category)

    # Group food items by restaurant
    grouped_items = defaultdict(list)
    for item in food_items:
        grouped_items[item.restaurant].append(item)  # Convert to string

    # Convert defaultdict to normal dict
    context = {
        "category": category,
        "grouped_items": dict(grouped_items)  # Ensuring it's JSON-serializable
    }

    print("Final Context Data:", context)  # Debugging print

    return render(request, "home/breakfast.html", context)


def add_to_cart(request):
    try:
        item_name = request.GET.get("name")
        item_price = request.GET.get("price")

        if not item_name or not item_price:
            return JsonResponse({"error": "Missing item name or price"}, status=400)

        try:
            item_price = float(item_price)  # Convert price to float
        except ValueError:
            return JsonResponse({"error": "Invalid price format"}, status=400)

        print(f"Adding to cart: {item_name}, Price: {item_price}")  # Debugging logs

        # Get the food item from the database
        food_item = get_object_or_404(FoodItem, name=item_name)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the item is already in the cart
        cart_item = CartItem.objects.filter(cart=cart, food_item=food_item).first()

        if cart_item:
            cart_item.quantity += 1  # Increase quantity
            cart_item.save()
        else:
            # Create new cart item if it doesn't exist
            cart_item = CartItem.objects.create(cart=cart, food_item=food_item, quantity=1)

        # Get updated cart count
        cart_count = CartItem.objects.filter(cart=cart).count()

        return JsonResponse({"message": "Item added to cart", "cart_count": cart_count})

    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging output
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)


def cart_view(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()  # Ensure `items` is a related name
        total_price = sum(item.get_total() for item in cart_items)
    else:
        cart_items = []
        total_price = 0

    # Debugging: Print to console
    print("Cart Items:", cart_items)
    print("Total Price:", total_price)

    return render(request, "home/cart.html", {"cart_items": cart_items, "total_price": total_price})


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1  # Reduce quantity by 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove item from cart if quantity is 1

    return redirect('cart_view')  # Redirect back to cart page


def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    total_price = sum(item.get_total() for item in cart_items)
    form = ShippingForm()
    return render(request, "home/checkout.html", {"cart_items": cart_items, "total_price": total_price, 'form': form})


def order_success(request):
    return render(request, "home/order_success.html")


def place_order(request):
    if request.method == "POST":
        form = ShippingForm(request.POST)
        if form.is_valid():
            full_address = f"{form.cleaned_data['full_name']}, {form.cleaned_data['address']}, {form.cleaned_data['city']}, {form.cleaned_data['state']}, {form.cleaned_data['zip_code']}, {form.cleaned_data['country']}"

        cart = Cart.objects.filter(user=request.user).first()
        cart_items = cart.items.all() if cart else []

        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')

        # Create Order
        order = Order.objects.create(user=request.user, address=full_address,
                                     total_price=sum(item.get_total() for item in cart_items))

        # Send Confirmation mail
        send_order_confirmation_email(order)

        # Move cart items to order items
        for item in cart_items:
            OrderItem.objects.create(order=order, food_item=item.food_item, quantity=item.quantity,
                                     price=item.food_item.price)

        # Clear Cart
        cart_items.delete()

        '''messages.success(request, "Order placed successfully!")'''
        return redirect('order_success')

    return redirect('checkout')


def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Show latest first
    return render(request, "home/order.html", {"orders": orders})


def send_order_confirmation_email(order):
    subject = f"Order Confirmation - {order.id}"
    message = f"Dear {order.user},\n\nThank you for your purchase!\nYour order (ID: {order.id}) has been successfully placed."
    recipient_email = 'ashu1997panda@gmail.com'  # Ensure your Order model has `customer_email`

    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])




def contact_submit(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]

        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been sent successfully!")

        return redirect("contact")
    return render(request, "home/contact.html")

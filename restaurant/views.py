from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, FoodItem, Category
from .forms import RestaurantForm, FoodItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def restaurant_page(request, slug):
    try:
        restaurant = Restaurant.objects.get(slug=slug)
        food_items = FoodItem.objects.filter(restaurant=restaurant)
        categories = Category.objects.all()  # Fetch all categories
        print(categories)
        print(food_items)
        if request.user != restaurant.owner:
            return redirect("homepage")  # Restrict access to only the owner
        return render(request, "restaurant/restaurant_homepage.html",
                      {"restaurant": restaurant, "food_items": food_items,"categories":categories})
    except Restaurant.DoesNotExist:
        return redirect("homepage")

def menu_page(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Fetch food items grouped by category
    categories = Category.objects.filter(foodItem__restaurant=restaurant).distinct()
    food_items_by_category = {category: FoodItem.objects.filter(restaurant=restaurant, category=category) for category
                              in categories}

    return render(request, 'restaurant/food_menu.html', {
        'restaurant': restaurant,
        'food_items_by_category': food_items_by_category,
    })


def update_food(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    food_items = FoodItem.objects.filter(restaurant=restaurant)
    categories = Category.objects.all()  # Fetch all categories
    if request.method == "POST":
        food_id = request.POST.get("food_id")

        food_item = get_object_or_404(FoodItem, id=food_id, restaurant=restaurant)
        form = FoodItemForm(request.POST,request.FILES, instance=food_item)

        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.restaurant = restaurant  # Ensure correct restaurant
            food_item.save()
            return redirect("restaurant_page", slug=restaurant.slug)

        else:
            print("❌ Form is NOT valid! Errors:", form.errors)
            return HttpResponse(f"Form errors: {form.errors}", status=400)
    context = {
        "restaurant": restaurant,
        "food_items": food_items,
        "categories": categories,
    }
    return render(request, "restaurant/restaurant_homepage.html",context)


def add_food_item(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    categories = Category.objects.all()

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)

            # Assign restaurant manually from POST data or fallback to the slug
            food_item.restaurant = restaurant
            food_item.save()

            print("✅ Food item added successfully:", food_item.name)
            return redirect("restaurant_page", slug=restaurant.slug)
        else:
            print("❌ Form is NOT valid! Errors:", form.errors.as_json())
            return HttpResponse(f"Form errors: {form.errors.as_json()}", status=400)

    form = FoodItemForm()
    return render(request, "restaurant/add_food_item.html", {
        "form": form,
        "restaurant": restaurant,
        "categories": categories,
    })


def delete_food(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)

    if request.method == "POST":
        food_item.delete()
        messages.success(request, "Food item deleted successfully!")
        return redirect("restaurant_page", slug=food_item.restaurant.slug)

    return redirect("restaurant/restaurant_homepage.html", slug=food_item.restaurant.slug)
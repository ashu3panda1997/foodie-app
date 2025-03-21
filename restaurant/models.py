from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Restaurant(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)  # Unique identifier for the URL

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate a slug from the name
        super().save(*args, **kwargs)

# Category Model (Veg/Non-Veg & Meal Type)
class Category(models.Model):
    MEAL_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Snacks', 'Snacks'),
        ('Dinner', 'Dinner'),
    ]

    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.meal_type}"


# FoodItem Model (Links to Restaurant & Category)
class FoodItem(models.Model):
    FOOD_TYPE_CHOICES = [
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='food_items')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foodItem')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES, default='Veg')

    def __str__(self):
        return f"{self.restaurant.id}-{self.name} ({self.restaurant.name})"

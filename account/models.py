from django.contrib.auth.models import AbstractUser
from django.db import models

# User Role Choices
USER_ROLES = (
    ('customer', 'Customer'),
    ('restaurant_owner', 'Restaurant Owner'),
    ('admin', 'Admin'),
)


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')

    def is_customer(self):
        return self.role == 'customer'

    def is_restaurant_owner(self):
        return self.role == 'restaurant_owner'

    def is_admin(self):
        return self.role == 'admin'

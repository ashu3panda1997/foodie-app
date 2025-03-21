from django.db import models
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Removed default function

    def save(self, *args, **kwargs):
        """Set expiry time on save."""
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=5)  # Set expiration time dynamically
        super().save(*args, **kwargs)

    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.user.username} - Expires at {self.expires_at}"

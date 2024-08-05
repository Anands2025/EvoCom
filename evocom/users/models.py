from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string


class User(AbstractUser):
    pass

class UserDetails(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('organizer', 'Event Organizer'),
        ('community_admin', 'Community Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    place = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    expiry = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=32)
        if not self.expiry:
            self.expiry = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.expiry > timezone.now()

    def __str__(self):
        return f"Token for {self.user.username} expires at {self.expiry}"

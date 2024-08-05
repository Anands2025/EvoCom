from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cover = models.ImageField(upload_to='community_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_communities', on_delete=models.CASCADE)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='admin_communities', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class UserCommunity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.community.name}"

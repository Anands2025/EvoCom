from django.contrib import admin
from . models import User,UserDetails,PasswordResetToken
# Register your models here.
admin.site.register(User)
admin.site.register(UserDetails)
admin.site.register(PasswordResetToken)
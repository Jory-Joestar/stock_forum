from django.contrib import admin

# Register your models here.
from .models import UserProfile,FollowingStocks
admin.site.register(UserProfile)
admin.site.register(FollowingStocks)
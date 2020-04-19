from django.contrib import admin

# Register your models here.
from forum.models import Plate,Post,Comment,Information
admin.site.register(Plate)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Information)
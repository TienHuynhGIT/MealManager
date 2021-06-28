from django.contrib import admin
from .models import UserProfile, Recipe, Weekday


admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(Weekday)



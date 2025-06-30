from django.contrib import admin

# Register your models here.
from .models import Menu, MenuItem, Category, CustomizationOption

admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(CustomizationOption)
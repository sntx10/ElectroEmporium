from django.contrib import admin

from applications.electronics.models import Category, Electronic

admin.site.register(Category)
admin.site.register(Electronic)
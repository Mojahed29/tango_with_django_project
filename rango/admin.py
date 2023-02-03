from django.contrib import admin

# Register your models here.
from django.contrib import admin
from rango.models import Category, Page
admin.site.register(Category)
admin.site.register(Page)


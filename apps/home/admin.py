from unfold.admin import ModelAdmin
from django.contrib import admin
from apps.home import models


@admin.register(models.Product)
class ProductAdmin(ModelAdmin):
    list_per_page = 20
    list_display = ["description", "brand", "price"]
    search_fields = ["description", "brand"]

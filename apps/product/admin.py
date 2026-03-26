from unfold.admin import ModelAdmin
from django.contrib import admin
from apps.product import models


@admin.register(models.Product)
class ProductAdmin(ModelAdmin):
    list_per_page = 20
    list_display = ["description", "brand", "price", "weight_kg", "category"]
    search_fields = ["description", "brand"]
    list_filter = ["category"]


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_per_page = 20
    list_display = ["name", "average_price_kg"]
    search_fields = ["name"]

from rest_framework import serializers
from apps.product import models


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductCategory
        fields = ["id", "name", "average_price_kg"]


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = ["id", "image", "description", "brand", "price", "weight_kg", "category"]

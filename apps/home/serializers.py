from rest_framework import serializers
from apps.home import models


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ["id", "image", "description", "brand", "price"]

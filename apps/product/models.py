from django.db import models
from apps.product.utils import product_image_path


class ProductCategory(models.Model):

    class CategoryNames(models.TextChoices):
        RICE  = "RICE",  "Arroz"
        BEANS = "BEANS", "Feijão"

    name             = models.CharField(max_length=10, choices=CategoryNames, verbose_name="Nome")
    average_price_kg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Preço médio por kg")

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "categoria de produto"
        verbose_name_plural = "categorias de produtos"


class Product(models.Model):
    image       = models.FileField(null=True, blank=True, upload_to=product_image_path, verbose_name="Imagem")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    brand       = models.CharField(max_length=50, verbose_name="Marca")
    price       = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço")
    weight_kg   = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    category    = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name="Categoria")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "produto"
        verbose_name_plural = "produtos"

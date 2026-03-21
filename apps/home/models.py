from django.db import models
from apps.home.utils import product_image_path


class Product(models.Model):
    image       = models.FileField(upload_to=product_image_path, verbose_name="Imagem")
    description = models.CharField(max_length=100, verbose_name="Descrição")
    brand       = models.CharField(max_length=50, verbose_name="Marca")
    price       = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "produto"
        verbose_name_plural = "produtos"

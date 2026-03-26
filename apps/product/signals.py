from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from apps.product.models import Product


@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
    if instance.image:
        if default_storage.exists(instance.image.path):
            default_storage.delete(instance.image.path)

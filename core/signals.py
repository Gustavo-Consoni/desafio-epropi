from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_migrate


@receiver(post_migrate)
def verify_superuser(sender, **kwargs):
    User = get_user_model()
    if settings.DEBUG and not User.objects.filter(email="admin@admin.com").exists():
        User.objects.create_superuser(username="admin", email="admin@admin.com", password="admin123")

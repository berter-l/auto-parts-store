from django.db.models.signals import post_migrate
from django.dispatch import receiver

from authentication.models import CustomUser


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not CustomUser.objects.filter(email='admin@gmail.com').exists():
        CustomUser.objects.create_superuser(
            email='admin@gmail.com',
            password='1234',
            )
        print("Superuser created.")
    else:
        print("Superuser already exists.")

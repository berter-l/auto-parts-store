import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache

from catalog.models import AutoParts

logger = logging.getLogger('django')


@receiver(post_save, sender=AutoParts)
def auto_parts_save(sender, instance, **kwargs):
    cache.delete_pattern('*product*')


@receiver(post_delete, sender=AutoParts)
def auto_parts_delete(sender, instance, **kwargs):

    cache.delete_pattern('*product*')


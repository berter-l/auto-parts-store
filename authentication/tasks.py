import logging
from celery import Celery
from celery import shared_task
from django.core.management import call_command


logger = logging.getLogger('django_request')


@shared_task
def delete_tokens():
    try:
        call_command('flushexpiredtokens', verbosity=0)
        logger.info("Expired tokens flushed successfully")
    except Exception as e:
        logger.error(f"Error flushing expired tokens: {str(e)}")
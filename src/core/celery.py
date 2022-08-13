from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')

app = Celery('core')

app.config_from_object('core.settings.base', namespace = 'CELERY')

app.autodiscover_tasks()

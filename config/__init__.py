from __future__ import absolute_import, unicode_literals

# Сделаем так, чтобы Celery был загружен при старте Django
# Это помогает гарантировать, что задачи будут обнаружены
from .celery import app as celery_app

__all__ = ('celery_app',)
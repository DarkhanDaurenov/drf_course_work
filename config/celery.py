from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Используем строку здесь для того, чтобы работать с Celery Worker и без
# необходимости сериализовать конфигурационный объект.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в каждом приложении
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoWebsite.settings')

broker = settings.CELERIES["broker"]
backend = settings.CELERIES["backend"]

app = Celery(
    'celery',
    broker=f"amqp://%s:%s@%s:%s/" % (
        broker.get("USER"),
        broker.get("PASSWORD"),
        broker.get("HOST"),
        broker.get("PORT"),
    ),
    backend=backend,
    namespace="CELERY",
)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)

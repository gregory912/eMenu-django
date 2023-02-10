import os

from celery import Celery
from celery.schedules import crontab

from dishes.tasks import task_send_email_dishes_modified_yesterday


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    The function manages the calling of tasks at appropriate times
    """
    sender.add_periodic_task(
        crontab(hour=10, minute=00, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
        task_send_email_dishes_modified_yesterday,
        name="Send an email at 10 about yesterday's modified dishes")

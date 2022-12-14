from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Movie_tickets_booking.settings")

app = Celery(
    "Movie_tickets_booking",
    # broker="amqp://guest:guest@localhost:5672//",
    # backend="redis://localhost",
    include=["Movie_booking_app.tasks"],
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


from celery.schedules import crontab

app.conf.beat_schedule = {
    # Scheduler Name
    "print-message-ten-seconds": {
        # Task Name (Name Specified in Decorator)
        "task": "print_msg_main",
        # Schedule
        "schedule": crontab(
            minute="*/1"
        ),  #!This should be set to 240(4 hrs)(right now it is set to 1 minute)
        # Function Arguments
        "args": ("Hello",),
    }
}

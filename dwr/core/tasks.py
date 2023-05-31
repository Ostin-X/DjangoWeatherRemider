from celery import shared_task
# from django_celery_beat.models import CrontabSchedule, PeriodicTask
from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import Q

from .funcs import update_weather_sub_queryset, send_webhook, send_email
from .models import Subscription


@shared_task
def update_subscriptions_weather_data():
    queryset = Subscription.objects.all()
    update_weather_sub_queryset(queryset)
    return 'Weather data updated'


@shared_task
def check_schedule_subscription_task():
    now = make_aware(datetime.now())  # Get the current time in the same timezone as your `next_run` field
    if due_subscriptions := Subscription.objects.filter(Q(next_run__lt=now) | Q(next_run__isnull=True), is_active=True):
        if webhook_queryset := due_subscriptions.exclude(webhook_url=None):
            send_webhook(webhook_queryset)
        if email_queryset := due_subscriptions.filter(webhook_url=None):
            send_email(email_queryset)

#
# @shared_task
# def send_weather_task(time_period):
#     send_data(time_period)
#     return 'OK'


# my_choices_list = Subscription.MY_CHOICES
# CrontabSchedule.objects.all().delete()
# PeriodicTask.objects.all().delete()

# for choice_value, choice_label in my_choices_list:
#     time_unit = timedelta(seconds=choice_value)  # Convert to timedelta
#     schedule = {'minute': time_unit.seconds % 3600 // 60, 'hour': time_unit.seconds // 3600, 'day_of_week': '*',
#                 'day_of_month': '*', 'month_of_year': '*'}
#
#     crontab_schedule = CrontabSchedule.objects.get_or_create(**schedule)
#
#     periodic_task = PeriodicTask.objects.get_or_create(
#         task='core.tasks.send_weather_task',
#         crontab=crontab_schedule,
#         name=choice_label,
#         args=json.dumps([choice_value]),
#     )

# @shared_task
# def send_1h_email_task():
#     send_data(3600)
#     return 'OK'
#
#
# @shared_task
# def send_3h_email_task():
#     send_data(3)
#     return 'OK'
#
#
# @shared_task
# def send_6h_email_task():
#     send_data(6)
#     return 'OK'
#
#
# @shared_task
# def send_12h_email_task():
#     send_data(12)
#     return 'OK'

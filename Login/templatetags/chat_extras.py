from datetime import datetime, timedelta
import pytz
import django

django.setup()
from django.conf import settings
from django import template

register = template.Library()


@register.filter
def display_time(value):
    # Convert the datetime object to the timezone specified in settings
    value_aware = value.astimezone(pytz.timezone(settings.TIME_ZONE))

    now = datetime.now(pytz.timezone(settings.TIME_ZONE))
    diff = now - value_aware

    if diff < timedelta(minutes=1):
        return "Just now"
    elif diff < timedelta(hours=1):
        return f"{diff.seconds // 60} minutes ago"
    elif diff < timedelta(hours=24):
        return f"{diff.seconds // 3600} hours ago"
    elif diff < timedelta(days=2):
        return "Yesterday"
    else:
        return value_aware.strftime('%b %d, %Y')

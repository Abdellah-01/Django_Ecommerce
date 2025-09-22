# your_app/templatetags/custom_filters.py
from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def human_time(value):
    """
    Converts datetime to human-readable format:
    - <1 hour -> "X minutes ago"
    - <1 day -> "HH:MM AM/PM"
    - 1-2 days -> "Yesterday HH:MM AM/PM"
    - >2 days -> "DD Mon YYYY | HH:MM AM/PM"
    """
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value

    # Less than 1 hour
    if diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minutes ago" if minutes > 0 else "Just now"

    # Less than 1 day
    elif diff < timedelta(days=1):
        return value.strftime("%I:%M %p").lstrip("0")

    # Between 1 and 2 days
    elif diff < timedelta(days=2):
        return f"Yesterday {value.strftime('%I:%M %p').lstrip('0')}"

    # Older than 2 days
    else:
        return value.strftime("%d %b %Y | %I:%M %p").lstrip("0")

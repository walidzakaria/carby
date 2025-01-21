from django import template
from datetime import datetime
import pytz
from decimal import Decimal

register = template.Library()

@register.filter
def get_date(value, include_time=True):
    if not value:
        return ''
    date_obj = datetime.fromisoformat(value)
    egypt_tz = pytz.timezone('Africa/Cairo')
    egypt_time = date_obj.astimezone(egypt_tz)
    formatted_time = egypt_time.strftime(f'{"%H:%M " if include_time else ""}%Y-%m-%d')
    return formatted_time


@register.filter
def format_number(value):
    return f'{Decimal(value):,.2f}'


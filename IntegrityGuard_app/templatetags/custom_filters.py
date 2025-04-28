from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtracts the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value
    
@register.filter
def days_until_month(assigned_date):
    """Calculate days remaining until a month is reached from assigned date."""
    if not assigned_date:
        return 0
    
    # Get current date
    now = datetime.now()
    
    # Calculate one month from assigned date
    one_month_later = assigned_date + timedelta(days=30)
    
    # Calculate days remaining
    days_remaining = (one_month_later - now).days
    
    return max(0, days_remaining)